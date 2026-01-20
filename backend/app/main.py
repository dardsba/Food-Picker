import os
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from sqlmodel import SQLModel, Session, create_engine, select

from .models import User, Recipe

DB_PATH = Path(__file__).resolve().parent.parent / "data.db"
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

app = FastAPI(title="Food Picker API")

# CORS
cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sessions
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# OAuth (Google)
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


@app.get("/api/health")
async def health():
    return {"ok": True}


# --- Auth ---
@app.get("/api/auth/login")
async def auth_login(request: Request):
    redirect_uri = os.getenv("OAUTH_REDIRECT_URL", "http://localhost:8000/api/auth/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/api/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    # Prefer UserInfo; fall back to ID token claims
    userinfo = token.get("userinfo")
    if not userinfo:
        try:
            userinfo = await oauth.google.parse_id_token(request, token)
        except Exception:  # pragma: no cover - network dependent
            userinfo = None
    if not userinfo:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    email = userinfo.get("email")
    name = userinfo.get("name")
    picture = userinfo.get("picture")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(email=email, name=name, picture=picture)
            session.add(user)
            session.commit()
            session.refresh(user)
        else:
            # update basics on login
            changed = False
            if user.name != name:
                user.name = name
                changed = True
            if picture and user.picture != picture:
                user.picture = picture
                changed = True
            if changed:
                session.add(user)
                session.commit()
    request.session["user"] = {"id": user.id, "email": user.email, "name": user.name, "picture": user.picture}

    return RedirectResponse(os.getenv("FRONTEND_AFTER_LOGIN", "/"))


@app.post("/api/auth/logout")
async def auth_logout(request: Request):
    request.session.clear()
    return {"ok": True}


def get_current_user(request: Request) -> User:
    data = request.session.get("user")
    if not data:
        raise HTTPException(status_code=401, detail="Not authenticated")
    with Session(engine) as session:
        user = session.get(User, data["id"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user


@app.get("/api/me")
async def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name, "picture": user.picture}


# --- Recipes ---
@app.get("/api/recipes", response_model=List[Recipe])
async def list_recipes(user: User = Depends(get_current_user)):
    with Session(engine) as session:
        rows = session.exec(select(Recipe).where(Recipe.user_id == user.id).order_by(Recipe.created_at.desc())).all()
        return rows


@app.post("/api/recipes", response_model=Recipe)
async def create_recipe(payload: Recipe, user: User = Depends(get_current_user)):
    recipe = Recipe(**payload.dict(exclude={"id", "user_id", "created_at"}), user_id=user.id)
    with Session(engine) as session:
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return recipe


@app.get("/api/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)
        if not recipe or recipe.user_id != user.id:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe


@app.put("/api/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, payload: Recipe, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)
        if not recipe or recipe.user_id != user.id:
            raise HTTPException(status_code=404, detail="Recipe not found")
        update_data = payload.dict(exclude_unset=True, exclude={"id", "user_id", "created_at"})
        for k, v in update_data.items():
            setattr(recipe, k, v)
        session.add(recipe)
        session.commit()
        session.refresh(recipe)
        return recipe


@app.delete("/api/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, user: User = Depends(get_current_user)):
    with Session(engine) as session:
        recipe = session.get(Recipe, recipe_id)
        if not recipe or recipe.user_id != user.id:
            raise HTTPException(status_code=404, detail="Recipe not found")
        session.delete(recipe)
        session.commit()
        return {"ok": True}


# --- Image upload ---
@app.post("/api/images/upload")
async def upload_image(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    suffix = Path(file.filename).suffix or ".jpg"
    import uuid

    filename = f"{uuid.uuid4().hex}{suffix}"
    dest = UPLOADS_DIR / filename
    content = await file.read()
    dest.write_bytes(content)
    return {"url": f"/uploads/{filename}"}


# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

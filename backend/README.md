# Food Picker Backend (FastAPI)

MVP Python backend providing Google OAuth login, per-user recipes, and image uploads.

## Features
- Google OAuth2 login (Authorization Code) via Authlib
- Session-based auth; `/api/me` returns the current user
- SQLite DB using SQLModel
- CRUD `/api/recipes` scoped to the logged-in user
- Image upload endpoint storing files under `backend/uploads` and serving from `/uploads`

## Quick start (Ubuntu)

```bash
# 1) Clone this repo and open a shell here

# 2) Create virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -r backend/requirements.txt

# 4) Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env and set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET

# 5) Run the server
uvicorn backend.app.main:app --reload --port 8000
```

Server runs at http://localhost:8000

## OAuth setup (Google)
1. Go to Google Cloud Console → APIs & Services → Credentials.
2. Create OAuth client ID of type “Web application”.
3. Authorized redirect URI: `http://localhost:8000/api/auth/callback`
4. Put the client id/secret in `backend/.env`.

Login flow:
- GET `/api/auth/login` → Google consent → returns to `/api/auth/callback` → session is created → redirects to `FRONTEND_AFTER_LOGIN`.

## API sketch
- `GET /api/health` → `{ ok: true }`
- `GET /api/me` → current user (requires login)
- `GET /api/recipes` → list user recipes
- `POST /api/recipes` → create recipe (JSON body)
- `GET /api/recipes/{id}` → get recipe
- `PUT /api/recipes/{id}` → update recipe
- `DELETE /api/recipes/{id}` → delete recipe
- `POST /api/images/upload` (multipart) → `{ url: "/uploads/<file>" }`

## Notes
- This is a simple MVP: SQLite + sessions. For production, move to Postgres, HTTPS, and a persistent object store (e.g., Azure Blob/S3) for images.
- CORS is permissive for local dev; tighten in deployment.

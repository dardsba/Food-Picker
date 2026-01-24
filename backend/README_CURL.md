# Food-Picker — curl snippets

Quick curl examples you can run against a local server at `http://127.0.0.1:8000`.

Notes:
- Use `-i` to include response headers in output.
- Use `-c cookies.txt` to save cookies (login response), and `-b cookies.txt` to send them on subsequent requests.
- The API uses a server-side session cookie (name `session`) for authenticated routes. For OAuth flows use a browser for the redirect steps.

1) Health

```bash
curl -i http://127.0.0.1:8000/api/health
```

2) Start OAuth login (redirects to provider)

This will return a 302 with a `Location` header pointing to the provider. To capture the session cookie set by the callback, perform the flow in a browser or capture cookies with `--cookie-jar`.

```bash
# This shows the redirect (won't complete login in curl)
curl -i http://127.0.0.1:8000/api/auth/login

# If you want to capture cookies from the server set during OAuth callback (not the provider), use a browser and then export cookies to a file named cookies.txt
```

3) Logout (requires session cookie)

```bash
curl -i -X POST http://127.0.0.1:8000/api/auth/logout -b cookies.txt
```

4) Get current user (authenticated)

```bash
curl -i http://127.0.0.1:8000/api/me -b cookies.txt
```

5) List recipes (pagination, filtering, search, sort)

Examples:

```bash
# Basic (page 1, 20 per page)
curl -i "http://127.0.0.1:8000/api/recipes?page=1&per_page=20" -b cookies.txt

# Filter by tag + language, search and sort descending by created_at
curl -i "http://127.0.0.1:8000/api/recipes?page=1&per_page=10&tag=vegan&language=en&q=pasta&sort=-created_at" -b cookies.txt
```

6) Create a recipe (authenticated)

Use the example JSON at `backend/examples/create_recipe_request.json`.

```bash
curl -i -X POST http://127.0.0.1:8000/api/recipes \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d @backend/examples/create_recipe_request.json
```

7) Get / Update / Delete a single recipe

```bash
# Get recipe with id 123
curl -i http://127.0.0.1:8000/api/recipes/123 -b cookies.txt

# Update recipe 123 (use JSON payload file)
curl -i -X PUT http://127.0.0.1:8000/api/recipes/123 \
  -H "Content-Type: application/json" -b cookies.txt -d @path/to/update_payload.json

# Delete recipe 123
curl -i -X DELETE http://127.0.0.1:8000/api/recipes/123 -b cookies.txt
```

8) Upload an image (multipart)

```bash
curl -i -X POST http://127.0.0.1:8000/api/images/upload \
  -F "file=@/full/path/to/image.jpg" -b cookies.txt
```

9) Serve uploaded file

```bash
curl -I http://127.0.0.1:8000/uploads/your-uploaded-file.jpg
```

10) Tips

- If `uvicorn` is running in a different environment, always run curl from a machine that can reach the server (VM host vs guest network settings).
- To run uvicorn accessible to other hosts, start with `--host 0.0.0.0`:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- If you use `fetch` from a browser-based frontend, remember to include credentials:

```js
fetch('/api/recipes', { credentials: 'include' })
```

File references:
- Examples used: `backend/examples/create_recipe_request.json`


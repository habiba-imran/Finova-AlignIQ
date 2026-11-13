# Deployment guide — Vercel (frontend) + Render (backend)

This project deploys as two independent services:

| Part | Stack | Host | Artifact |
|---|---|---|---|
| Frontend | React 19 + TypeScript + Vite + Tailwind | Vercel | Static files in `frontend/dist` |
| Backend | Python 3.12 + FastAPI + Uvicorn | Render | ASGI app `app.main:app` |

There is **no database, Redis, object storage, cron job or authentication** to provision. Nothing is persisted; both services are stateless.

The frontend calls the backend with **relative URLs** (`/api/...`). Therefore the two hosts must be connected with a rewrite/proxy:

```
Browser → https://<app>.vercel.app/api/... → https://<api>.onrender.com/api/...
```

This guide uses a Vercel rewrite. It requires **zero frontend code changes and no CORS configuration**. Direct cross-origin calls would need both.

---

## 0. Before you start

- Push the repository to GitHub/GitLab/Bitbucket; both hosts deploy from Git.
- Keep `.env.local` and real secrets out of Git (already ignored).
- Deploy the **backend first** so you have its URL when configuring Vercel.
- The checked-in configs are:
  - `render.yaml` — Render Blueprint for the backend.
  - `frontend/vercel.json` — Vercel build + `/api` rewrite (**replace the placeholder URL**).

Verified locally: `npm run build` (TypeScript + Vite) and `from app.main import app` both succeed with the pinned versions.

---

## 1. Deploy the backend on Render

### Option A — Blueprint (recommended)

1. In Render: **New → Blueprint**.
2. Select this repository. Render reads `render.yaml`.
3. Apply the service. It creates `finova-aligniq-api` with:
   - Root directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --no-access-log`
   - Health check: `/api/health`
   - Python `3.12.10`, `FINOVA_ENVIRONMENT=production`
4. Wait for the deploy, then copy the service URL, e.g. `https://finova-aligniq-api.onrender.com`.

### Option B — Manual Web Service

1. **New → Web Service** → select the repository.
2. Set:

| Setting | Value |
|---|---|
| Language / Runtime | Python 3 |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT --no-access-log` |
| Health Check Path | `/api/health` |
| Instance Type | Free (see caveats in §5) |

3. Add environment variables:

| Key | Value | Required |
|---|---|---|
| `PYTHON_VERSION` | `3.12.10` | Yes |
| `PYTHONUNBUFFERED` | `1` | Recommended |
| `FINOVA_ENVIRONMENT` | `production` | Yes |
| `FINOVA_GROQ_SYNTHETIC_ENABLED` | `false` | Yes (safe default) |
| `FINOVA_PARSER_GROQ_ENABLED` | `false` | Yes (safe default) |
| `GROQ_API_KEY` | *(secret)* | Only for AI-generated report wording |
| `GROQ_API_KEY_2` | *(secret)* | Only for AI-assisted parsing |

> **Do not** set `FINOVA_ENVIRONMENT=development` in production. AI-assisted parsing is intentionally gated to development + flag + key + exact bundled synthetic text; in production the action stays hidden. The standard parser, review and template reports work with no credentials.

4. Deploy.

### Verify the backend directly

```powershell
$api = 'https://YOUR-SERVICE.onrender.com'
Invoke-RestMethod -Uri "$api/api/health"
```

Expected:

```json
{"status":"ok","service":"finova-aligniq","phase":1}
```

Optional parse smoke test:

```powershell
$body = @{
  raw_text = "# SYNTHETIC`nTooth`tRotation (deg)`n13`t-1.2300 M`n"
  source_claim = 'Unknown'
  synthetic_data_confirmed = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "$api/api/v1/tmt/parse" -Method Post `
  -ContentType 'application/json; charset=utf-8' -Body $body
```

`/docs`, `/redoc` and `/openapi.json` are intentionally disabled — that is expected.

---

## 2. Deploy the frontend on Vercel

1. In Vercel: **Add New → Project** → import the repository.
2. Set:

| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Framework Preset | Vite (auto-detected) |
| Install Command | `npm ci` |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Node.js Version | 22.x (the repo requires `>=22.12.0`) |

3. Configure the API rewrite **before the first production deploy** (otherwise the UI loads but every API call 404s).

### Option A — Dashboard rewrite (no file editing)

Vercel → Project → **Settings → Rewrites** → Add:

| Source | Destination |
|---|---|
| `/api/:path*` | `https://YOUR-SERVICE.onrender.com/api/:path*` |

Use the exact `https://` Render URL from §1.

### Option B — `frontend/vercel.json`

The file is already checked in. Edit the destination:

```json
"destination": "https://YOUR-SERVICE.onrender.com/api/:path*"
```

Replace `YOUR-SERVICE` with your real Render subdomain, commit, and redeploy. Keep the `/api/:path*` prefix on the destination — the backend routes already include `/api`.

4. Deploy and open the Vercel production URL.

### Verify through Vercel

```powershell
Invoke-RestMethod -Uri 'https://YOUR-APP.vercel.app/api/health'
```

If this returns the same health JSON as §1, the rewrite works. Then open the site and run the synthetic example flow: **Load synthetic example → confirm synthetic data → Parse Table → Create draft review → Create final report**.

---

## 3. Environment variables summary

| Service | Variable | Needed | Notes |
|---|---|---|---|
| Render | `PYTHON_VERSION` | Yes | `3.12.10` |
| Render | `FINOVA_ENVIRONMENT` | Yes | `production` |
| Render | `FINOVA_GROQ_SYNTHETIC_ENABLED` | Yes | `false` for a safe public deploy |
| Render | `FINOVA_PARSER_GROQ_ENABLED` | Yes | `false` for a safe public deploy |
| Render | `GROQ_API_KEY` / `GROQ_API_KEY_2` | No | Backend-only. Never expose to the frontend. |
| Vercel | *(none)* | — | The rewrite needs no variables. |

**Never** put `GROQ_*` keys in a `VITE_*` variable or anything under `frontend/`; Vite inlines `VITE_*` values into the public JavaScript bundle.

---

## 4. Files added for deployment

- `render.yaml` — service definition, safe defaults, optional key placeholders.
- `frontend/vercel.json` — build settings and the `/api` rewrite.
- `docs/DEPLOYMENT.md` — this guide.

No application code was changed. The frontend still uses relative `/api/...` URLs; the Vercel rewrite supplies the missing production proxy.

---

## 5. Important runtime notes

### Free-tier cold starts
Render Free web services spin down after ~15 minutes of inactivity. The next request can take 30–60+ seconds. Because Vercel proxies the request, that cold start may surface as a **504** on the first API call. Options:

- Retry once (the service is warm afterwards).
- Keep it warm with a free uptime monitor (e.g. cron-job.org) pinging `https://YOUR-SERVICE.onrender.com/api/health` every 10 minutes.
- Use a paid Render instance for a production demo.
- Or move the backend to a host without aggressive spin-down (Railway, Fly.io, Koyeb, Cloud Run).

### Public endpoint / abuse
The backend has **no authentication and no rate limiting**. Anyone who knows the Render URL can submit synthetic payloads and consume CPU. Keep the Groq keys unset (the paid provider calls stay off), and consider Cloudflare rate limiting or a small API gateway if the demo is public.

### Data boundary
This is a prototype: **not for clinical use, no real patient data**. The app accepts only synthetic-data-confirmed input and keeps no persistence or logs of request bodies (`--no-access-log`). Do not weaken these controls for a deployment.

### Request size
The backend enforces a **1 MiB** request-body limit (HTTP 413 above that). This is comfortably within Vercel's proxy limits.

### Processing model
Parsing/report generation is synchronous CPU work inside the Uvicorn process. One Render instance is sufficient; no worker/queue service is required.

### Ephemeral disk
Render's filesystem is ephemeral. The app does not write to disk, so this is fine. Do not add local file persistence without a database/object store.

### No routing on the frontend
The React app is a single page with no client-side router. No SPA fallback rewrite is required. If routing is added later, add a catch-all rewrite **after** the `/api` rewrite.

### If you later prefer direct API calls
Instead of the Vercel rewrite, you would need to:

1. Add `fastapi.middleware.cors.CORSMiddleware` with an explicit `allow_origins` list (Vercel production + preview domains).
2. Change the three `fetch()` calls in `frontend/src/api/{parse,review,report}.ts` to use a base URL from `import.meta.env.VITE_API_BASE_URL`.
3. Set `VITE_API_BASE_URL` in Vercel.

The rewrite approach is simpler and keeps `credentials: 'omit'`, `redirect: 'error'` and the same-origin privacy posture.

---

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| App loads, API calls fail with 404 | Rewrite missing or points at the wrong host | Check Vercel **Settings → Rewrites**; test `/api/health` on the Vercel domain |
| `/api/health` on Vercel returns 502/504 | Render service asleep or crashed | Open the Render logs; hit the Render URL directly; allow for cold start |
| `redirect: 'error'` errors in the browser | Render URL uses HTTP or redirects | Use the exact `https://...onrender.com` URL, no trailing slash |
| Render build fails importing `app` | Root Directory not `backend`, or start command run elsewhere | Set Root Directory to `backend`; or build from repo root with `pip install -r backend/requirements.txt` and start with `cd backend && uvicorn ...` |
| Render build fails on a Python package | Wrong Python version | Set `PYTHON_VERSION=3.12.10` and redeploy |
| Vercel build fails on TypeScript | Type errors or wrong Node version | Run `npm run build` locally; set Node 22.x |
| AI features missing | Expected in production | `FINOVA_ENVIRONMENT=production` disables them by design |
| 413 error | Input over 1 MiB | Expected engineering limit |

---

## 7. Redeploys and rollbacks

- Both hosts auto-deploy on push to the connected branch. `render.yaml` changes can require a Blueprint sync in Render.
- Vercel keeps immutable deployments: **Deployments → Promote/Rollback**.
- Render keeps previous deploys: **Events → Rollback**.
- If the Render URL changes (service renamed/recreated), update the Vercel rewrite — this is the only cross-service link.

---

## 8. Minimal checklist

- [ ] Repository pushed to Git.
- [ ] Render service created with Root Directory `backend`, Python 3.12.10, health check `/api/health`.
- [ ] `FINOVA_ENVIRONMENT=production`, Groq flags `false`, keys unset.
- [ ] `https://<render>/api/health` returns `{"status":"ok",...}`.
- [ ] Vercel project with Root Directory `frontend`, Vite, Node 22.x.
- [ ] Rewrite `/api/:path*` → `https://<render>/api/:path*`.
- [ ] `https://<vercel>/api/health` returns the same JSON.
- [ ] Synthetic UI flow completes end to end.
- [ ] No secrets in Git or in `VITE_*` variables.

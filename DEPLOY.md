# CrossForge License Server — Render.com (no VPS)

Deploy in ~5 minutes without SSH:

1. Push this folder to GitHub (repo e.g. `crossforge-license-server`).
2. [render.com](https://render.com) → **New → Blueprint** → connect repo.
3. Render reads `render.yaml` and creates the web service + disk.
4. In Render dashboard, set **secret** env vars (Stripe keys).
5. Copy the service URL (e.g. `https://crossforge-license.onrender.com`).
6. Stripe webhook: `POST https://YOUR-SERVICE.onrender.com/v1/stripe/webhook`

## After deploy

Set GitHub repo variable on **crossforge-legal** (Settings → Secrets and variables → Actions → Variables):

- `CROSSFORGE_LICENSE_API` = your Render URL

Rebuild Pages (or re-run workflow) so the billing page points at your server.

Update each snap `snapcraft.yaml`:

```yaml
CROSSFORGE_LICENSE_API: https://YOUR-SERVICE.onrender.com
```

## Local

```bash
./scripts/setup.sh
.venv/bin/uvicorn server.main:app --host 127.0.0.1 --port 8780
```

Without Stripe keys, checkout returns a 30-day dev license for testing.

## Alternatives

- **Fly.io** — see `fly.toml`
- **Railway** — import repo, set start command from `render.yaml`

See `../SNAP_STORE.md` for the full Snap-only publisher guide.

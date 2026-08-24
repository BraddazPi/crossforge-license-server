# CrossForge License Server

Stripe-backed subscription API for CrossForge Builder snaps and desktop installs.

## Legal

- Privacy: https://crossforge.studio/legal/privacy
- Terms: https://crossforge.studio/legal/terms
- Data handled: email, Stripe customer/subscription IDs, opaque license tokens, product SKU
- Privacy contact: privacy@crossforge.studio
- Billing portal: https://billing.crossforge.studio

See `legal/PRIVACY.md` for GDPR details on Stripe integration.

## Run locally

```bash
./scripts/setup.sh
cp .env.example .env   # add Stripe keys when ready
.venv/bin/uvicorn server.main:app --host 127.0.0.1 --port 8780
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Health check |
| POST | `/v1/checkout/session` | Start Stripe Checkout |
| GET | `/v1/entitlement?token=&product=` | Validate subscription |
| POST | `/v1/activate` | Activate pasted license token |
| POST | `/v1/stripe/webhook` | Stripe events |
| GET | `/v1/portal?token=` | Billing portal URL |

## Product SKUs

Must match `PRODUCT_SLUG` in each builder’s `studio/product.py` (legacy `crossforge-*-studio` names).

See `SNAP_STORE.md` in `~/Projects/` for full Snap Store workflow.

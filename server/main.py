"""CrossForge License Server — Stripe subscriptions for Snap-distributed studios."""

from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("CROSSFORGE_LICENSE_DB", str(ROOT / "data" / "licenses.db")))

PRODUCTS = {
    "crossforge-windows-studio": os.environ.get("STRIPE_PRICE_WINDOWS", ""),
    "crossforge-macos-studio": os.environ.get("STRIPE_PRICE_MACOS", ""),
    "crossforge-android-studio": os.environ.get("STRIPE_PRICE_ANDROID", ""),
    "crossforge-bundle": os.environ.get("STRIPE_PRICE_BUNDLE", ""),
}

STRIPE_SECRET = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
PUBLIC_BASE = os.environ.get("CROSSFORGE_PUBLIC_URL", "https://crossforge-license.onrender.com").rstrip("/")
LEGAL_SITE = os.environ.get("CROSSFORGE_LEGAL_SITE", "https://BraddazPi.github.io/crossforge-legal/legal").rstrip("/")
BILLING_SITE = os.environ.get("CROSSFORGE_BILLING_PORTAL", "https://BraddazPi.github.io/crossforge-legal/billing").rstrip("/")


class CheckoutBody(BaseModel):
    product: str
    email: str | None = None
    success_url: str | None = None
    cancel_url: str | None = None


class ActivateBody(BaseModel):
    token: str = Field(min_length=8)
    product: str


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS licenses (
                token TEXT PRIMARY KEY,
                email TEXT,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                product TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'inactive',
                current_period_end TEXT,
                updated_at TEXT NOT NULL
            );
            """
        )


def _issue_token() -> str:
    return f"cf_{uuid.uuid4().hex}"


def _entitlement_for_row(row: sqlite3.Row | None, product: str) -> dict:
    if row is None:
        return {
            "active": False,
            "tier": "expired",
            "product": product,
            "plan": "none",
            "message": "No active subscription for this product.",
        }
    status = row["status"]
    end = row["current_period_end"]
    active = status in {"active", "trialing", "pending"}
    if row["product"] == "crossforge-bundle":
        active = status in {"active", "trialing"}
    if end:
        try:
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
            if end_dt.tzinfo is None:
                end_dt = end_dt.replace(tzinfo=UTC)
            if datetime.now(UTC) > end_dt:
                active = False
        except ValueError:
            pass
    tier = "pro" if active else "expired"
    return {
        "active": active,
        "tier": tier,
        "product": product,
        "plan": "pro_monthly",
        "email": row["email"],
        "expires_at": end,
        "manage_url": f"{PUBLIC_BASE}/v1/portal?token={row['token']}",
        "message": "Subscription active." if active else "Subscription inactive or expired.",
    }


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _init_db()
    yield


app = FastAPI(title="CrossForge License Server", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CROSSFORGE_CORS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "stripe_configured": bool(STRIPE_SECRET)}


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>CrossForge License Server</title></head>
<body style="font-family:system-ui;max-width:640px;margin:2rem auto;line-height:1.5">
<h1>CrossForge License Server</h1>
<p>Subscription API for CrossForge Builder apps.</p>
<ul>
  <li><a href="{LEGAL_SITE}/privacy.html">Privacy Policy</a></li>
  <li><a href="{LEGAL_SITE}/terms.html">Terms of Service</a></li>
  <li><a href="{BILLING_SITE}/index.html">Manage / cancel subscription</a></li>
  <li><a href="/health">Health check</a></li>
  <li><a href="/docs">API docs</a></li>
</ul>
</body></html>"""


@app.get("/billing")
def billing_redirect() -> RedirectResponse:
    return RedirectResponse(url=f"{BILLING_SITE}/index.html", status_code=302)


@app.get("/v1/entitlement")
def entitlement(token: str, product: str) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM licenses WHERE token = ?", (token,)).fetchone()
    ent = _entitlement_for_row(row, product)
    if row and row["product"] == "crossforge-bundle":
        ent["active"] = _entitlement_for_row(row, product)["active"]
    return ent


@app.post("/v1/activate")
def activate(body: ActivateBody) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM licenses WHERE token = ?", (body.token,)).fetchone()
    return _entitlement_for_row(row, body.product)


@app.post("/v1/checkout/session")
def checkout_session(body: CheckoutBody) -> dict:
    price = PRODUCTS.get(body.product)
    if not STRIPE_SECRET:
        token = _issue_token()
        with _connect() as conn:
            conn.execute(
                """
                INSERT INTO licenses (token, email, product, status, current_period_end, updated_at)
                VALUES (?, ?, ?, 'active', ?, ?)
                """,
                (
                    token,
                    body.email or "dev@local",
                    body.product,
                    (datetime.now(UTC) + timedelta(days=30)).isoformat(),
                    datetime.now(UTC).isoformat(),
                ),
            )
            conn.commit()
        return {
            "checkout_url": body.success_url or f"{PUBLIC_BASE}/activated?token={token}",
            "license_token": token,
            "mode": "dev_grant",
        }
    if not price:
        raise HTTPException(400, f"Missing Stripe price for {body.product}")

    import stripe

    stripe.api_key = STRIPE_SECRET
    token = _issue_token()
    success = body.success_url or f"{PUBLIC_BASE}/activated?token={token}"
    cancel = body.cancel_url or f"{PUBLIC_BASE}/cancelled"

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price, "quantity": 1}],
        success_url=success + ("&" if "?" in success else "?") + f"token={token}",
        cancel_url=cancel,
        customer_email=body.email,
        metadata={"crossforge_token": token, "crossforge_product": body.product},
    )

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO licenses (token, email, product, status, updated_at)
            VALUES (?, ?, ?, 'pending', ?)
            """,
            (token, body.email, body.product, datetime.now(UTC).isoformat()),
        )
        conn.commit()

    return {"checkout_url": session.url, "license_token": token, "session_id": session.id}


@app.post("/v1/stripe/webhook")
async def stripe_webhook(request: Request) -> dict:
    if not STRIPE_SECRET:
        raise HTTPException(503, "Stripe not configured")
    import stripe

    stripe.api_key = STRIPE_SECRET
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(400, str(exc)) from exc

    if event["type"] in {"checkout.session.completed", "customer.subscription.updated"}:
        obj = event["data"]["object"]
        token = (obj.get("metadata") or {}).get("crossforge_token")
        sub_id = obj.get("subscription") or obj.get("id")
        customer = obj.get("customer")
        email = obj.get("customer_details", {}).get("email") or obj.get("customer_email")
        product = (obj.get("metadata") or {}).get("crossforge_product", "crossforge-bundle")
        period_end = None
        status = "active"
        if event["type"] == "customer.subscription.updated":
            status = obj.get("status", "active")
            period_end = datetime.fromtimestamp(obj["current_period_end"], UTC).isoformat()
        if token:
            with _connect() as conn:
                conn.execute(
                    """
                    UPDATE licenses SET
                      email = COALESCE(?, email),
                      stripe_customer_id = COALESCE(?, stripe_customer_id),
                      stripe_subscription_id = COALESCE(?, stripe_subscription_id),
                      product = COALESCE(?, product),
                      status = ?,
                      current_period_end = COALESCE(?, current_period_end),
                      updated_at = ?
                    WHERE token = ?
                    """,
                    (
                        email,
                        customer,
                        sub_id,
                        product,
                        status,
                        period_end,
                        datetime.now(UTC).isoformat(),
                        token,
                    ),
                )
                conn.commit()
    return {"received": True}


@app.get("/v1/portal")
def portal(token: str) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM licenses WHERE token = ?", (token,)).fetchone()
    if row is None or not row["stripe_customer_id"] or not STRIPE_SECRET:
        raise HTTPException(404, "No billing profile for this license token")
    import stripe

    stripe.api_key = STRIPE_SECRET
    session = stripe.billing_portal.Session.create(
        customer=row["stripe_customer_id"],
        return_url=os.environ.get("STRIPE_PORTAL_RETURN_URL", BILLING_SITE),
    )
    return {"portal_url": session.url}

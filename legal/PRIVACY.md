# CrossForge Privacy Policy

**Effective date:** 24 August 2026  
**Publisher:** Brad Smith, trading as CrossForge  
**Contact:** braddazpi@gmail.com

This policy describes how CrossForge collects, uses, and protects personal data
when you use CrossForge Builder apps (Windows, macOS, Android), the CrossForge
license server, and related websites.

## What we collect

### Subscription and billing (Stripe)

When you subscribe to CrossForge Pro, we process data through [Stripe](https://stripe.com):

| Data | Purpose | Processor |
|------|---------|-----------|
| Email address | Account identification, receipts, support | Stripe + CrossForge license server |
| Payment method | Subscription billing | Stripe (CrossForge does not store full card numbers) |
| Subscription status | Entitlement checks in the app | CrossForge license server |
| License token | Offline grace and activation | Stored locally on your device and on our server |

Stripe's privacy policy: https://stripe.com/privacy

### License server

Our license API (`crossforge-license.onrender.com`) stores:

- Hashed or opaque license tokens
- Product SKU (Windows / macOS / Android / bundle)
- Subscription tier and expiry
- Email (when provided at checkout)
- Webhook event metadata from Stripe

We do **not** collect your application source code, project files, or AI chat
content through the license server.

### In-app data (local)

CrossForge apps store on **your machine**:

- Project files under `~/Documents/CrossForge/`
- Toolchain caches (.NET, Apple SDK, Android SDK) downloaded per upstream licences
- AI provider API keys in `.env` (if you configure built-in chat)
- Subscription cache under `~/.config/crossforge/` or Snap user data

This local data is not transmitted to CrossForge unless you explicitly use
features that call our license API or third-party AI APIs you configure.

### AI providers (optional)

If you configure OpenAI, Anthropic, Ollama, Cursor, or another provider:

- Requests go **directly** from your machine to that provider (or via your
  external assistant using the local OpenAPI bridge).
- CrossForge does not operate a cloud inference service for your prompts.
- Each provider's privacy policy applies.

### Snap Store

If you install via Snapcraft, Canonical may collect usage and crash data per the
Snap Store terms. See https://ubuntu.com/legal/snap-store-privacy-policy

## Legal bases (GDPR)

| Processing | Basis |
|------------|-------|
| Subscription fulfilment | Contract (Art. 6(1)(b) GDPR) |
| Billing via Stripe | Contract + legal obligation (tax/accounting) |
| Support emails | Legitimate interest / contract |
| Marketing (if any) | Consent |

## Retention

- Subscription records: duration of subscription + statutory retention for invoices
- Support tickets: up to 24 months
- Local trial/subscription cache: until you delete app config

## Your rights

EU/UK users may request access, correction, deletion, restriction, portability, and
objection by emailing braddazpi@gmail.com. You may lodge a complaint with
your supervisory authority.

## International transfers

Stripe and hosting providers may process data outside your country with appropriate
safeguards (Standard Contractual Clauses where applicable).

## Children

CrossForge is not directed at children under 16. We do not knowingly collect data
from children.

## Changes

We will post updates at https://BraddazPi.github.io/crossforge-legal/legal/privacy.html and bump the
effective date.

## Data controller

Brad Smith, trading as CrossForge  
Email: braddazpi@gmail.com  
Support: braddazpi@gmail.com

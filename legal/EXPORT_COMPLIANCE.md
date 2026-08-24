# Export, Encryption, and Store Distribution

CrossForge helps you **build** applications. **Publishing** them to end users
remains your responsibility, including legal compliance for encryption, export
controls, code signing, and app-store policies.

## What CrossForge provides

- Unsigned or debug build artefacts (APK, AAB, `.app` bundles, Windows publish
  folders) depending on template and toolchain
- Local toolchain orchestration on **your** Linux machine
- Documentation and compliance strategies when vendor requirements change

## What you must handle

### Code signing and notarization

| Platform | Your responsibility |
|----------|---------------------|
| **macOS** | Sign and notarize with Apple Developer ID on macOS (or CI you control). CrossForge does not notarize from Linux. |
| **Windows** | Authenticode signing with your certificate if distributing outside dev/test. |
| **Android** | Release keystore, Play App Signing, and Play Developer account for Play Store. |

CrossForge strategy `play_store_user_account` documents that release signing is
user-managed.

### Export administration (EAR / EU dual-use)

If your application uses encryption (HTTPS alone often qualifies as mass-market
encryption in many jurisdictions), you may need:

- US BIS export classification (EAR) self-classification or registration
- EU dual-use regulation assessment where applicable
- App-store encryption questionnaires (Apple, Google)

CrossForge IDE traffic (HTTPS to license server, Stripe, AI APIs) uses standard
TLS. **Your shipped apps** may embed crypto libraries (TLS, SQLite encryption,
etc.) — classify **your** product accordingly.

### App store policies

- **Google Play:** Developer Program Policies, target API levels, data safety form
- **Apple App Store:** App Review Guidelines, privacy nutrition labels
- **Microsoft Store:** Partner Center policies if you publish WinUI/MSIX builds

CrossForge subscriptions do **not** include store accounts or submission on your
behalf.

## Snap distribution of CrossForge itself

CrossForge snaps declare `network` and standard desktop plugs. Canonical reviews
snap metadata including privacy policy URL and support contact (see SNAP_STORE.md).

## Questions

legal@crossforge.studio — general compliance  
support@crossforge.studio — product usage

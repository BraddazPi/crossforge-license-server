# Apple SDK on Linux — User Notice

CrossForge macOS Builder can cross-compile Darwin targets from a Linux host by
using:

1. Open-source host tools (Clang, LLD) via your distribution
2. A Swift.org open-source compiler kit
3. Apple SDK headers and libraries fetched **after you accept Apple's licence**

## What CrossForge does

- Presents Apple's SDK / Xcode licence for **your** acceptance before download
- Fetches SDK components from Apple software-update infrastructure to a **local
  cache on your machine**
- Does **not** ship Apple SDK binaries inside CrossForge installers or snaps
- Offers an alternative path: **user-provided SDK archive** (`APS_SDK_ARCHIVE`)
  obtained on licensed Apple hardware under Apple's terms

## What CrossForge does not do

- Provide legal advice on Apple's Program License Agreement (PLA)
- Guarantee that every cross-compilation workflow is permitted in all jurisdictions
- Perform Apple notarization or code signing (you must use Apple-approved tools
  on macOS for distribution)

## Grey areas and your responsibility

Some interpretations of Apple's PLA restrict SDK use to Apple-branded hardware or
specific development workflows. Cross-compiling macOS apps from Linux may not be
permitted under your Apple developer agreement.

**You must:**

- Maintain a valid Apple Developer account where required for distribution
- Ensure SDK acquisition and use comply with Apple's current terms
- Consult qualified legal counsel if your organisation requires formal clearance

The in-app EULA acceptance gate records **your** consent to proceed with
Apple's licence terms; it is **not** a substitute for professional legal review.

## If Apple terms change

CrossForge includes a compliance adaptation system. When fetch paths or licence
requirements change, the app can switch strategies (CDN fetch, user archive,
C/Objective-C fallback, etc.) via **Settings → Legal** or the
`/api/compliance/*` API.

Support: braddazpi@gmail.com

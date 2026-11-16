# MilitaryInfo

Offline Android reference for US military uniforms, medals, ribbons, badges, devices, and rank insignia, World War I to today. Night style (dark navy and charcoal). No internet permission, no accounts, no tracking. Updates come only from GitHub Releases.

## Data

All content lives in `app/src/main/assets/data/entries.json`. Images go in `app/src/main/assets/images/`.

Every entry carries a proof tag:

- `official`: confirmed by a regulation or the Institute of Heraldry
- `historical`: confirmed by documented history (archives, museum records)
- `unverified`: no source yet

Official and Historical entries must list at least one source. A release should have no Unverified entries.

Check the data before every build:

    python3 tools/validate_data.py            # report problems
    python3 tools/validate_data.py --release  # also fail on any Unverified entry

### Variations

Each entry can list `variants` (finish, gender, uniform, era, colors) and `attachments` (items that hang underneath, such as qualification bars, each with its own variants).

- `finish`: `polished` (shiny) or `subdued` (non-shiny)
- `gender`: `male`, `female`, or `any`
- `era`: `ww1`, `interwar`, `ww2`, `korea`, `vietnam`, `coldwar`, `gulf`, `modern`

## Build and release

GitHub builds the APK. Push a tag that starts with `v` (for example `v0.1.0`). The workflow reads the release title and notes from `RELEASE_NOTES.md`.

Repository secrets used for signing: `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`.

To bump the version, edit `versionCode` and `versionName` in `app/build.gradle.kts`.

The app uses only the Android platform libraries, with no Google services and no AndroidX.

Icons are from Tabler Icons (MIT license, see `TABLER-ICONS-LICENSE.txt`).

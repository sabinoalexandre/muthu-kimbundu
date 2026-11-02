# MUTHU --- Portuguese ↔ Kimbundu Translator

**MUTHU** is a bilingual translation application designed to translate
words, phrases, paragraphs, and longer texts between Portuguese and
Kimbundu.

**Slogan:** "Two languages. One connection."

## Project Overview

MUTHU aims to make communication between Portuguese and Kimbundu more
accessible through a clean interface, a modular architecture, and
carefully managed linguistic resources.

The application also intends to contribute to the preservation and
digital accessibility of the Kimbundu language.

## Features

- Mobile-first, responsive KivyMD interface with a bottom navigation bar.
- Scrollable screens, live search, clear empty states, and keyboard-aware text input.
- Bidirectional translation: Portuguese → Kimbundu and Kimbundu → Portuguese.
- Translation of individual words, expressions, phrases, paragraphs, and
  longer texts.
- Searchable bilingual dictionary.
- Translation history with search, deletion, and clearing.
- Favorites for saved translations and expressions.
- Light and dark themes.
- Clear communication of unsupported expressions and limitations.
- When no entry exists, the original text is returned and clearly marked as
  unmatched instead of being replaced with an error or invented translation.
- The initial local lexicon includes sourced single-word entries and documented
  multiword expressions. It seeds the SQLite dictionary table on startup.

## Technology

- **Python** as the programming language.
- **Kivy** as the application framework.
- **KivyMD** for Material Design components.
- **SQLite** for local persistence.

The interface previews at 360 × 640 (9:16) on desktop and uses the device's
native size on phones. Android packaging is configured with Buildozer; a debug
APK is created locally by following the steps below.

## Getting Started

### Prerequisites

- Python 3.13
- Kivy and KivyMD (see `requirements.txt`)
- A working graphical environment (for desktop)

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy the example configuration and adjust the values as needed:

```bash
cp .env.example .env
```

Available settings:

- `TRANSLATION_PROVIDER`: initial translation strategy (`dictionary` or `machine`).
- `MUTHU_THEME`: application theme (`light` or `dark`).
- `MUTHU_DEFAULT_SOURCE`: default source language (`pt` or `kimbundu`).
- `MUTHU_DEFAULT_TARGET`: default target language (`pt` or `kimbundu`).
- External API credentials: reserved for future providers. No key is
  required at the moment.

### Run

```bash
python main.py
```

### Build and install on Android

Buildozer packages the Kivy app as an Android APK. Build on Linux or macOS;
Windows users can use WSL2. The first build downloads the Android SDK/NDK and
can take a while. Follow Buildozer's [platform-specific installation steps](https://buildozer.readthedocs.io/en/latest/installation/) for the Java and
system packages needed by your Linux/macOS version.

From the project directory, create a build environment and make a debug APK:

```bash
python3.12 -m venv .venv-buildozer
source .venv-buildozer/bin/activate
python -m pip install --upgrade pip buildozer setuptools "cython==0.29.34"
make app
```

The APK will be written to `bin/`. To install it over USB, enable Developer
Options and USB debugging on the phone, connect it, then run:

```bash
buildozer android deploy run
```

You can also copy the APK from `bin/` to the phone and open it there. Android
will ask you to allow installation from that file source. This debug APK is for
direct installation; publishing on Google Play requires a signed release build.
See the [Buildozer quickstart](https://buildozer.readthedocs.io/en/latest/quickstart/)
for the full workflow.

### Test

```bash
python -m pytest
```

## Project Structure

```text
MUTHU/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── assets/
├── src/
│   ├── ui/
│   ├── core/
│   ├── services/
│   ├── providers/
│   ├── database/
│   └── config/
├── data/
├── tests/
└── Makefile
```

## Translation Limitations

- No machine translation service has been verified so far to support
  Kimbundu reliably; the current implementation starts with a local
  dictionary-based provider.
- Dictionary lookups are not contextual sentence translations.
- Results identify themselves as dictionary lookups and keep unverified entries marked.
- Unsupported expressions return the original text with an unmatched status;
  no fabricated translation is shown.
- Uncertain results must never be presented as confirmed translations.

## Linguistic Data and Verification

- Linguistic resources live in `data/` and `data/linguistic_resources/`.
- Dictionary entries carry a verification status (`verified`,
  `unverified`) and a source reference.
- Community contributions remain unverified until reviewed by Kimbundu
  speakers or linguists.

## Development

The project follows a modular architecture with clear separation of
responsibilities (presentation, application, business logic, services,
data layers).

Quality checks:

```bash
make test
make clean
make re
```

## Future Work

- Integration of a verified machine translation model.
- Android deployment.

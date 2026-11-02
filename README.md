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

The interface targets phone-sized screens and remains usable on desktop. Android
packaging and device distribution are planned separately; this repository does
not yet include a Buildozer configuration or an installable Android package.

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
make fclean
make re
```

## Future Work

- Integration of a verified machine translation model.
- Android deployment.

# MUTHU --- Project Specification

**Project name:** MUTHU\
**Full name:** MUTHU --- Portuguese ↔ Kimbundu Translator\
**Type:** Bilingual translation application\
**Languages:** Portuguese ↔ Kimbundu\
**Technology:** Python + KivyMD\
**Initial platform:** Desktop\
**Future platform:** Android\
**Slogan:** "Two languages. One connection."

------------------------------------------------------------------------

## 1. Project Overview

MUTHU is a bilingual translation application designed to translate
words, phrases, paragraphs, and longer texts between Portuguese and
Kimbundu.

The application aims to make communication between the two languages
more accessible through a clean interface, a modular architecture, and
carefully managed linguistic resources.

MUTHU is also intended to contribute to the preservation and digital
accessibility of the Kimbundu language.

Linguistic accuracy is a core requirement. The application must never
invent Kimbundu expressions or present uncertain translations as
verified.

## 2. Main Objectives

-   Translate from Portuguese to Kimbundu.
-   Translate from Kimbundu to Portuguese.
-   Support words, expressions, phrases, paragraphs, and longer texts.
-   Provide a searchable bilingual dictionary.
-   Preserve translation history and allow users to save favorites.
-   Clearly communicate uncertainty and limitations.
-   Use an architecture that allows translation providers and linguistic
    resources to be replaced or extended.
-   Build an accessible and consistent user experience with KivyMD.

## 3. Core Functional Requirements

### 3.1 Translation

The application must support:

-   Portuguese → Kimbundu.
-   Kimbundu → Portuguese.
-   Translation of individual words and expressions.
-   Translation of sentences, paragraphs, and longer texts.
-   Manual source and target language selection.
-   Language switching through a dedicated button.
-   Automatic language detection only when a reliable detection
    mechanism is available.
-   Copying translated text.
-   Clearing input and output fields.
-   Character counting.
-   Empty-input validation.
-   Loading indicators while a translation is being processed.
-   Error handling for unavailable services, unsupported expressions,
    and invalid responses.
-   Alternative translations and linguistic notes whenever reliable
    information is available.

The application must distinguish between a dictionary lookup and a
contextual translation. Replacing individual words is not sufficient to
claim that a complete sentence has been translated correctly.

### 3.2 Translation Reliability

Every translation result should communicate its origin and reliability
where possible.

The application should distinguish between:

-   Verified translations.
-   Dictionary-based results.
-   Machine-generated translations.
-   Unverified community contributions.
-   Unsupported expressions.
-   Results whose reliability cannot be established.

Uncertain results must not be presented as confirmed translations.

### 3.3 Main Screen

The main screen should contain:

-   MUTHU logo and application name.
-   Source language selector.
-   Target language selector.
-   Language-switch button.
-   Text input area.
-   Character counter.
-   Translate button.
-   Translation result area.
-   Copy button.
-   Clear button.
-   Shortcut to favorites.
-   Loading, success, and error states.

### 3.4 Translation History

The history screen should provide:

-   Original text.
-   Translated text.
-   Source and target languages.
-   Translation provider or method, when available.
-   Verification status.
-   Date and time.
-   Search functionality.
-   Individual deletion.
-   Option to clear the complete history.

### 3.5 Favorites

Users should be able to:

-   Save translations and expressions.
-   View saved items.
-   Search favorites.
-   Copy saved text.
-   Remove individual favorites.

### 3.6 Dictionary

The dictionary should support searches in both directions:

-   Kimbundu → Portuguese.
-   Portuguese → Kimbundu.

A dictionary entry may include:

-   Kimbundu word or expression.
-   Portuguese translation.
-   Definition.
-   Alternative meanings.
-   Example sentences.
-   Grammatical category.
-   Regional or dialectal variation.
-   Verification status.
-   Source or reference.
-   Suggestions for corrections.

Verified entries and unverified contributions must be clearly
distinguished.

### 3.7 Settings

The settings screen should provide:

-   Light and dark themes.
-   Default language preferences.
-   Application information.
-   Data-management options.
-   Other user preferences as the application evolves.

### 3.8 Navigation

The main navigation should include:

1.  Home
2.  Dictionary
3.  History
4.  Favorites
5.  Settings

------------------------------------------------------------------------

## 4. Technology and User Interface

The application will initially be developed with:

-   **Python** as the programming language.
-   **Kivy** as the application framework.
-   **KivyMD** for Material Design components.
-   **SQLite** for local persistence.

The interface should be:

-   Simple and intuitive.
-   Responsive to different window sizes.
-   Accessible and readable.
-   Visually consistent.
-   Designed to avoid unnecessary complexity.

The initial target is desktop. The architecture should make future
Android support possible without requiring a complete rewrite.

------------------------------------------------------------------------

## 5. Software Architecture

MUTHU should use a modular architecture with clear separation of
responsibilities.

### 5.1 Presentation Layer

Responsible for the graphical interface:

-   Kivy/KivyMD screens.
-   Reusable widgets.
-   Navigation.
-   Displaying translation results and application states.
-   Capturing user input.

The UI must not contain database implementation details or depend
directly on a specific translation provider.

### 5.2 Application Layer

Coordinates application workflows:

-   Translation requests.
-   Dictionary searches.
-   History management.
-   Favorites management.
-   User preferences.
-   Communication between the interface and services.

### 5.3 Business Logic Layer

Contains the core application rules:

-   Translation orchestration.
-   Language validation.
-   Text processing.
-   Linguistic resource management.
-   Translation result classification.
-   Confidence and verification status handling.

### 5.4 Services Layer

Provides application services:

-   Translation service.
-   Dictionary service.
-   Storage service.
-   External API communication.
-   Linguistic resource access.

### 5.5 Data Layer

Responsible for persistence and data access:

-   SQLite database.
-   Database models.
-   Repositories.
-   Local dictionaries and linguistic resources.

The architecture should allow each layer to evolve independently as much
as possible.

------------------------------------------------------------------------

## 6. Translation Engine

The translation engine must be independent of the graphical interface
and the database.

### 6.1 Provider Abstraction

Use a provider-independent interface so that different translation
implementations can be integrated without changing the rest of the
application.

Example:

``` python
class TranslationProvider:

    def translate(self, text, source, target):
        raise NotImplementedError

    def detect_language(self, text):
        raise NotImplementedError
```

Possible implementations include:

-   `LocalDictionaryProvider`
-   `MachineTranslationProvider`
-   `CustomKimbunduModelProvider`

These are possible architectural components, not claims that suitable
services or models already exist.

### 6.2 Research Before Integration

Before choosing a translation provider, investigate:

-   Translation APIs and their actual language support.
-   Open-source machine translation models.
-   Existing Kimbundu dictionaries.
-   Linguistic corpora.
-   Academic publications.
-   Available datasets.
-   Possibilities for training or fine-tuning a model.

Do not assume that services such as DeepL, Google Translate, or
LibreTranslate support Kimbundu. Their actual support must be verified
before integration.

### 6.3 Initial Translation Strategy

If no reliable Portuguese--Kimbundu machine translation model is
available, begin with a dictionary-based solution.

In that case:

-   Clearly label dictionary lookups.
-   Do not describe word substitution as contextual sentence
    translation.
-   Return an explicit unsupported result when no reliable entry exists.
-   Keep the provider architecture ready for a future machine
    translation model.

### 6.4 Linguistic Considerations

The translation system should account for:

-   Regional and dialectal variation.
-   Alternative spellings.
-   Grammar and sentence structure.
-   Context-dependent meanings.
-   Verified example sentences.
-   Source references.
-   Review by Kimbundu speakers or linguists whenever possible.

### 6.5 Asynchronous Processing

Potentially slow translation requests must not freeze the interface.

The implementation should use background processing where appropriate,
update Kivy widgets safely on the main thread, and provide:

-   Loading feedback.
-   Request timeouts.
-   Error messages.
-   Recovery from unavailable services.

------------------------------------------------------------------------

## 7. Database Design

SQLite will be used for local persistence.

### 7.1 Translation History

Suggested fields:

-   `id`
-   `original_text`
-   `translated_text`
-   `source_language`
-   `target_language`
-   `provider`
-   `verification_status`
-   `timestamp`

### 7.2 Favorites

Suggested fields:

-   `id`
-   `original_text`
-   `translated_text`
-   `source_language`
-   `target_language`
-   `timestamp`

### 7.3 Dictionary

Suggested fields:

-   `id`
-   `kimbundu_term`
-   `portuguese_translation`
-   `definition`
-   `alternative_meanings`
-   `examples`
-   `grammatical_category`
-   `regional_variation`
-   `verification_status`
-   `source_reference`
-   `timestamp`

### 7.4 Community Contributions (Optional)

A future version may allow users to suggest:

-   New words.
-   Expressions.
-   Corrections.
-   Alternative meanings.
-   Example sentences.

Community contributions must remain unverified until reviewed by an
appropriate reviewer.

------------------------------------------------------------------------

## 8. Suggested Project Structure

``` text
MUTHU/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── fonts/
│
├── src/
│   ├── ui/
│   │   ├── screens/
│   │   │   ├── home.py
│   │   │   ├── dictionary.py
│   │   │   ├── history.py
│   │   │   ├── favorites.py
│   │   │   └── settings.py
│   │   │
│   │   └── widgets/
│   │       ├── language_selector.py
│   │       ├── translation_card.py
│   │       ├── text_input.py
│   │       └── dictionary_entry.py
│   │
│   ├── core/
│   │   ├── translator.py
│   │   ├── language.py
│   │   ├── validators.py
│   │   └── translation_result.py
│   │
│   ├── services/
│   │   ├── translation_service.py
│   │   ├── dictionary_service.py
│   │   └── storage_service.py
│   │
│   ├── providers/
│   │   ├── base_provider.py
│   │   ├── dictionary_provider.py
│   │   └── machine_translation_provider.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   └── config/
│       └── settings.py
│
├── data/
│   ├── dictionary.json
│   └── linguistic_resources/
│
└── tests/
    ├── test_translator.py
    ├── test_dictionary.py
    ├── test_validators.py
    ├── test_storage.py
    └── test_language_switch.py
```

The structure is a starting point. It may be adjusted when
implementation needs justify the change, while preserving separation of
concerns.

------------------------------------------------------------------------

## 9. Code Quality Requirements

The codebase should follow these principles:

-   Clean, readable, and maintainable Python.
-   Separation of concerns.
-   Object-oriented design where appropriate.
-   Meaningful class, function, and variable names.
-   Avoid unnecessary duplication.
-   Appropriate exception handling.
-   Documentation for important modules and public methods.
-   Avoid placing the entire application in `main.py`.
-   Avoid hardcoded API credentials.
-   Reusable UI components.
-   Translation-provider independence.
-   Type hints where appropriate.
-   Consistent Python conventions.
-   No unverified linguistic claims.

------------------------------------------------------------------------

## 10. Testing Strategy

Automated tests should cover the main application behavior.

### 10.1 Translation Tests

-   Portuguese → Kimbundu.
-   Kimbundu → Portuguese.
-   Empty input.
-   Unsupported expressions.
-   Invalid provider responses.
-   Provider failures.
-   Language switching.
-   Verification-status handling.

### 10.2 Dictionary Tests

-   Search in both directions.
-   Search for words and expressions.
-   Alternative meanings.
-   Verification status.
-   Missing entries.
-   Regional variations where represented in the data.

### 10.3 Persistence Tests

-   Save and retrieve translation history.
-   Delete individual history entries.
-   Clear history.
-   Add and remove favorites.
-   Retrieve saved favorites.

### 10.4 Reliability Tests

-   Unverified entries must remain marked as unverified.
-   The application must not fabricate translations.
-   Dictionary lookup must not be confused with contextual machine
    translation.
-   Provider errors must be handled without crashing the application.

External services should be mocked during automated tests so that tests
do not depend on network availability.

------------------------------------------------------------------------

## 11. Development Phases

### Phase 1 --- Research and Foundation

Tasks:

-   Research Kimbundu linguistic resources.
-   Investigate APIs and machine translation models.
-   Identify dictionaries, corpora, and academic references.
-   Choose a realistic initial translation strategy.
-   Create the project structure.
-   Configure the Python environment and dependencies.
-   Create an executable application entry point.

**Completion criteria:** A working project foundation and documented
translation strategy based on verified research.

### Phase 2 --- User Interface

Tasks:

-   Create the main screen.
-   Implement language selectors.
-   Add input and output areas.
-   Implement the language-switch control.
-   Create navigation.
-   Build the dictionary screen.
-   Establish the visual identity of MUTHU.

**Completion criteria:** The user can navigate through the application
and interact with the main interface.

### Phase 3 --- Linguistic Database

Tasks:

-   Design the dictionary data model.
-   Create the initial vocabulary dataset.
-   Add definitions and linguistic annotations where available.
-   Store verification status and sources.
-   Implement dictionary search.
-   Validate entries before marking them as verified.

**Completion criteria:** A searchable bilingual dictionary with
traceable sources and clear verification status.

### Phase 4 --- Translation Engine

Tasks:

-   Implement the provider abstraction.
-   Support both translation directions.
-   Integrate a verified translation model if one is available.
-   Implement dictionary fallback where appropriate.
-   Handle asynchronous operations.
-   Handle errors and unsupported expressions.
-   Distinguish verified, dictionary-based, generated, and unsupported
    results.

**Completion criteria:** A working translation workflow that
communicates its limitations honestly.

### Phase 5 --- Persistence

Tasks:

-   Implement SQLite integration.
-   Save translation history.
-   Implement favorites.
-   Add search and deletion operations.
-   Persist application preferences.

**Completion criteria:** History, favorites, and preferences remain
available after restarting the application.

### Phase 6 --- Quality Assurance

Tasks:

-   Run automated tests.
-   Test the interface manually.
-   Test network failures and provider errors.
-   Test different window sizes.
-   Fix discovered bugs.
-   Review linguistic reliability.

**Completion criteria:** The application behaves consistently under
normal and failure conditions.

### Phase 7 --- Documentation and Distribution

Tasks:

-   Write the README.
-   Document installation and configuration.
-   Explain translation limitations.
-   Document linguistic data sources.
-   Describe verification procedures.
-   Prepare the application for desktop distribution.
-   Evaluate Android support as a future milestone.

**Completion criteria:** Another developer can install, understand,
configure, and run the project using the documentation.

------------------------------------------------------------------------

## 12. Instructions for AI-Assisted Development

Any AI assistant contributing to MUTHU must follow these rules:

1.  Do not implement the entire application in one file.
2.  Establish and respect the architecture before adding features.
3.  Develop incrementally and validate each phase.
4.  Explain important architectural decisions.
5.  Do not present placeholders as completed functionality.
6.  Verify imports, dependencies, and file paths.
7.  Keep the application executable throughout development.
8.  Use stable and compatible Python, Kivy, and KivyMD versions.
9.  Keep translation providers replaceable.
10. Prioritize functionality, maintainability, and user experience.
11. Do not assume that an API supports Kimbundu.
12. Never fabricate Kimbundu words or translations.
13. Distinguish dictionary lookup from contextual translation.
14. Communicate limitations clearly.
15. Prioritize linguistic accuracy over the quantity of features.
16. Document the origin and verification status of linguistic resources.
17. Do not claim that the application works offline unless that
    capability is actually implemented and tested.

------------------------------------------------------------------------

## 13. Expected Final Result

The expected result is a functional Portuguese--Kimbundu translation
application featuring:

-   A modern KivyMD interface.
-   Bidirectional translation workflows.
-   A searchable bilingual dictionary.
-   Translation history.
-   Favorites.
-   SQLite persistence.
-   A modular and replaceable translation engine.
-   Carefully managed linguistic resources.
-   Clear verification and uncertainty indicators.
-   Error handling.
-   Automated tests.
-   Complete project documentation.

The application should be extensible and maintainable, with a structure
that supports future improvements and potential Android deployment.

## 14. Final Principle

**MUTHU is not merely a translation application. It is a digital
language bridge intended to make Kimbundu more accessible through
technology.**

The quality of its linguistic resources and the accuracy of its
translations must always take priority over the number of features it
offers.

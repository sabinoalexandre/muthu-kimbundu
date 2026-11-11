"""Application settings."""

from typing import Optional

from src.core.language import KIMBUNDU, PORTUGUESE

DEFAULT_THEME = "light"
DEFAULT_SOURCE_LANGUAGE = PORTUGUESE
DEFAULT_TARGET_LANGUAGE = KIMBUNDU
DEFAULT_TRANSLATION_PROVIDER = "dictionary"


class AppSettings:
    """User preferences of the MUTHU application."""

    def __init__(
        self,
        theme: str = DEFAULT_THEME,
        default_source_language: str = DEFAULT_SOURCE_LANGUAGE,
        default_target_language: str = DEFAULT_TARGET_LANGUAGE,
        translation_provider: str = DEFAULT_TRANSLATION_PROVIDER,
    ) -> None:
        self.theme = theme
        self.default_source_language = default_source_language
        self.default_target_language = default_target_language
        self.translation_provider = translation_provider

    @classmethod
    def from_env(cls, environ=None) -> "AppSettings":
        """Build settings from environment variables."""
        import os

        # Load the optional project-local configuration without overriding
        # environment variables supplied by the shell or the operating system.
        if environ is None:
            try:
                from dotenv import load_dotenv

                load_dotenv()
            except ImportError:
                pass

        env = os.environ if environ is None else environ
        return cls(
            theme=env.get("MUTHU_THEME", DEFAULT_THEME),
            default_source_language=env.get(
                "MUTHU_DEFAULT_SOURCE", DEFAULT_SOURCE_LANGUAGE
            ),
            default_target_language=env.get(
                "MUTHU_DEFAULT_TARGET", DEFAULT_TARGET_LANGUAGE
            ),
            translation_provider=env.get(
                "TRANSLATION_PROVIDER", DEFAULT_TRANSLATION_PROVIDER
            ),
        )

    def to_dict(self) -> dict:
        """Return the settings as a plain dictionary."""
        return {
            "theme": self.theme,
            "default_source_language": self.default_source_language,
            "default_target_language": self.default_target_language,
            "translation_provider": self.translation_provider,
        }

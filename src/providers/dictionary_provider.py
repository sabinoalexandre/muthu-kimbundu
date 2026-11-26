"""Local multilingual dictionary translation provider."""

import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.language import KIKONGO, KIMBUNDU, PORTUGUESE, UMBUNDU
from src.core.translation_result import TranslationResult
from src.providers.base_provider import TranslationProvider

DEFAULT_DICTIONARY_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "dictionary.json"
)
_WORD_PATTERN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def normalize_dictionary_term(value: Optional[str]) -> str:
    """Normalize case, accents, whitespace and sentence-ending punctuation."""
    normalized = unicodedata.normalize("NFD", str(value or "").casefold().strip())
    normalized = "".join(
        character for character in normalized
        if unicodedata.category(character) != "Mn"
    )
    normalized = unicodedata.normalize("NFC", normalized)
    normalized = " ".join(normalized.split())
    return normalized.rstrip(".,;:!?…\"'”’»)]}")


class LocalDictionaryProvider(TranslationProvider):
    """Dictionary based provider for Portuguese, Kimbundu, Kikongo and Umbundu."""

    def __init__(self, dictionary_path: Optional[str] = None) -> None:
        self.dictionary_path = (
            Path(dictionary_path) if dictionary_path else DEFAULT_DICTIONARY_PATH
        )
        self.entries: List[Dict[str, Any]] = self._load_entries()
        self._entry_indexes: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._translation_indexes: Dict[
            tuple[str, str],
            tuple[Dict[tuple[str, ...], List[Dict[str, Any]]], int],
        ] = {}

    def _load_entries(self) -> List[Dict[str, Any]]:
        """Load the multilingual dictionary resource."""
        if not self.dictionary_path.exists():
            return []
        with open(self.dictionary_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        entries = data.get("entries") or []
        if not isinstance(entries, list):
            return []
        loaded = [entry for entry in entries if isinstance(entry, dict)]
        if self.dictionary_path.resolve() == DEFAULT_DICTIONARY_PATH.resolve():
            imported_dir = self.dictionary_path.parent / "kimbundu_archive"
            for shard_path in sorted(imported_dir.glob("terms_*.json")):
                try:
                    with shard_path.open("r", encoding="utf-8") as handle:
                        shard = json.load(handle)
                except (OSError, json.JSONDecodeError):
                    continue
                shard_entries = shard.get("entries") if isinstance(shard, dict) else None
                if isinstance(shard_entries, list):
                    loaded.extend(
                        entry for entry in shard_entries if isinstance(entry, dict)
                    )
            umbundu_dir = self.dictionary_path.parent / "umbundu_archive"
            for shard_path in sorted(umbundu_dir.glob("terms_*.json")):
                try:
                    with shard_path.open("r", encoding="utf-8") as handle:
                        shard = json.load(handle)
                except (OSError, json.JSONDecodeError):
                    continue
                shard_entries = shard.get("entries") if isinstance(shard, dict) else None
                if isinstance(shard_entries, list):
                    loaded.extend(
                        entry for entry in shard_entries if isinstance(entry, dict)
                    )
        return loaded

    def _get_entry_index(self, field: str) -> Dict[str, Dict[str, Any]]:
        """Build an exact term index on first use."""
        if field not in self._entry_indexes:
            index: Dict[str, Dict[str, Any]] = {}
            for entry in self.entries:
                normalized = normalize_dictionary_term(entry.get(field))
                if normalized:
                    index.setdefault(normalized, entry)
            self._entry_indexes[field] = index
        return self._entry_indexes[field]

    def _get_translation_index(
        self, source_field: str, target_field: str
    ) -> tuple[Dict[tuple[str, ...], List[Dict[str, Any]]], int]:
        """Cache phrase matches for a language pair after its first lookup."""
        cache_key = (source_field, target_field)
        if cache_key not in self._translation_indexes:
            matches: Dict[tuple[str, ...], List[Dict[str, Any]]] = {}
            max_phrase_length = 1
            for entry in self.entries:
                source_words = tuple(
                    normalize_dictionary_term(word)
                    for word in _WORD_PATTERN.findall(
                        str(entry.get(source_field) or "")
                    )
                )
                if source_words and str(entry.get(target_field) or "").strip():
                    matches.setdefault(source_words, []).append(entry)
                    max_phrase_length = max(max_phrase_length, len(source_words))
            self._translation_indexes[cache_key] = (matches, max_phrase_length)
        return self._translation_indexes[cache_key]

    @property
    def entry_count(self) -> int:
        """Return the number of loaded dictionary entries."""
        return len(self.entries)

    def get_entry(
        self,
        kimbundu_term: Optional[str] = None,
        portuguese_translation: Optional[str] = None,
        kikongo_term: Optional[str] = None,
        umbundu_term: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a single dictionary entry matching the given fields."""
        term = normalize_dictionary_term(kimbundu_term)
        kikongo = normalize_dictionary_term(kikongo_term)
        umbundu = normalize_dictionary_term(umbundu_term)
        translation = normalize_dictionary_term(portuguese_translation)
        for field, normalized in (
            ("kimbundu_term", term),
            ("kikongo_term", kikongo),
            ("umbundu_term", umbundu),
            ("portuguese_translation", translation),
        ):
            if normalized:
                entry = self._get_entry_index(field).get(normalized)
                if entry is not None:
                    return entry
        return None

    def translate(
        self, text: str, source: str, target: str
    ) -> TranslationResult:
        """Replace the longest sourced word or expression in any language pair.

        Unmatched words and punctuation remain exactly as entered. This is a
        dictionary lookup, so matching words does not claim sentence-level grammar.
        """
        term = (text or "").strip()
        language_fields = {
            KIMBUNDU: "kimbundu_term",
            KIKONGO: "kikongo_term",
            UMBUNDU: "umbundu_term",
            PORTUGUESE: "portuguese_translation",
        }
        if (
            not term
            or source not in language_fields
            or target not in language_fields
            or source == target
        ):
            return TranslationResult.unsupported(
                term, source, target, "",
            )

        matches, max_phrase_length = self._get_translation_index(
            language_fields[source], language_fields[target]
        )

        input_words = list(_WORD_PATTERN.finditer(term))
        if not input_words:
            return TranslationResult.unsupported(
                term, source, target, "",
            )

        output: List[str] = []
        cursor = 0
        word_index = 0
        matched_entries: List[Dict[str, Any]] = []
        matched_any = False
        while word_index < len(input_words):
            selected = None
            selected_length = 0
            max_length = min(max_phrase_length, len(input_words) - word_index)
            for length in range(max_length, 0, -1):
                spans = input_words[word_index:word_index + length]
                if any(
                    not term[spans[i].end():spans[i + 1].start()].isspace()
                    for i in range(len(spans) - 1)
                ):
                    continue
                key = tuple(normalize_dictionary_term(span.group()) for span in spans)
                candidates = matches.get(key)
                if candidates:
                    selected = candidates[0]
                    selected_length = length
                    break

            if selected is None:
                word_index += 1
                continue

            first_span = input_words[word_index]
            last_span = input_words[word_index + selected_length - 1]
            output.append(term[cursor:first_span.start()])
            output.append(str(selected.get(
                language_fields[target]
            ) or ""))
            cursor = last_span.end()
            matched_entries.append(selected)
            matched_any = True
            word_index += selected_length

        if not matched_any:
            return TranslationResult.unsupported(term, source, target, "")

        output.append(term[cursor:])
        translated_text = "".join(output)
        result = TranslationResult.from_dictionary(
            original_text=term,
            translated_text=translated_text,
            source_language=source,
            target_language=target,
            entry=matched_entries[0],
        )
        if any(entry.get("verification_status") != "verified" for entry in matched_entries):
            result.verification_status = "unverified"
            result.confidence = min(result.confidence, 0.5)
        return result

    def detect_language(self, text: str) -> Optional[str]:
        """Dictionary lookups cannot reliably detect language by themselves."""
        return None

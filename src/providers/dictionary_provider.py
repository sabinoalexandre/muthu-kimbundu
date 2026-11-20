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


def _normalize_term(value: Optional[str]) -> str:
    """Normalize accents, case, whitespace and sentence-ending punctuation."""
    normalized = unicodedata.normalize("NFC", str(value or "")).casefold().strip()
    normalized = " ".join(normalized.split())
    return normalized.rstrip(".,;:!?…\"'”’»)]}")


class LocalDictionaryProvider(TranslationProvider):
    """Dictionary based provider for Portuguese, Kimbundu, Kikongo and Umbundu."""

    def __init__(self, dictionary_path: Optional[str] = None) -> None:
        self.dictionary_path = (
            Path(dictionary_path) if dictionary_path else DEFAULT_DICTIONARY_PATH
        )
        self.entries: List[Dict[str, Any]] = self._load_entries()

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
        term = _normalize_term(kimbundu_term)
        kikongo = _normalize_term(kikongo_term)
        umbundu = _normalize_term(umbundu_term)
        translation = _normalize_term(portuguese_translation)
        for entry in self.entries:
            entry_term = _normalize_term(entry.get("kimbundu_term"))
            entry_kikongo = _normalize_term(entry.get("kikongo_term"))
            entry_umbundu = _normalize_term(entry.get("umbundu_term"))
            entry_translation = _normalize_term(entry.get("portuguese_translation"))
            if term and entry_term == term:
                return entry
            if kikongo and entry_kikongo == kikongo:
                return entry
            if umbundu and entry_umbundu == umbundu:
                return entry
            if translation and entry_translation == translation:
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

        matches: Dict[tuple[str, ...], List[Dict[str, Any]]] = {}
        for entry in self.entries:
            source_term = entry.get(language_fields[source])
            target_term = entry.get(language_fields[target])
            source_words = tuple(_normalize_term(word) for word in _WORD_PATTERN.findall(str(source_term or "")))
            if source_words and str(target_term or "").strip():
                matches.setdefault(source_words, []).append(entry)

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
        max_phrase_length = max((len(key) for key in matches), default=1)
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
                key = tuple(_normalize_term(span.group()) for span in spans)
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

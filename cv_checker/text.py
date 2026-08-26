"""Normalisation de texte partagée par le parseur et les règles."""

from __future__ import annotations

import unicodedata

# Apostrophes typographiques ramenées à l'apostrophe simple, pour que les
# motifs de config.yml n'aient pas à gérer les deux variantes.
_APOSTROPHES = {"’": "'", "ʼ": "'", "‘": "'"}


def normalize(text: str) -> str:
    """Minuscules, sans accents, apostrophes uniformisées.

    Les positions des caractères sont préservées (la décomposition Unicode
    ne retire que les diacritiques combinants), ce qui permet d'appliquer
    un motif sur le texte normalisé et de retrouver l'extrait d'origine.
    """
    for fancy, plain in _APOSTROPHES.items():
        text = text.replace(fancy, plain)
    decomposed = unicodedata.normalize("NFD", text)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", stripped).lower()


def count_words(text: str) -> int:
    """Nombre de mots « utiles » : la ponctuation Markdown ne compte pas."""
    cleaned = "".join(c if (c.isalnum() or c in "-'@.+") else " " for c in text)
    return len([w for w in cleaned.split() if any(ch.isalnum() for ch in w)])

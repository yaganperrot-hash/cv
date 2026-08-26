"""Parseur Markdown minimal : titres et sections.

On ne dépend d'aucune lib Markdown : un CV reste un document simple, et
un parseur maison de 60 lignes évite une dépendance de plus dans la CI.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .text import count_words, normalize

_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    line: int  # 1-indexé


@dataclass
class Section:
    title: str
    level: int
    line: int
    body: str

    @property
    def word_count(self) -> int:
        return count_words(self.body)


@dataclass
class Document:
    """Un CV Markdown parsé."""

    raw: str
    headings: list[Heading] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)

    @property
    def normalized(self) -> str:
        return normalize(self.raw)

    def headings_at(self, level: int) -> list[Heading]:
        return [h for h in self.headings if h.level == level]


def parse(text: str, section_level: int = 2) -> Document:
    """Découpe le Markdown en titres et en sections de niveau `section_level`.

    Le corps d'une section court jusqu'au titre suivant de niveau inférieur
    ou égal ; les blocs de code sont ignorés pour la détection des titres
    (un `# commentaire` en Python n'est pas un titre).
    """
    lines = text.splitlines()
    headings: list[Heading] = []
    in_fence = False

    for index, line in enumerate(lines, start=1):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _HEADING_RE.match(line)
        if match:
            headings.append(
                Heading(
                    level=len(match.group("hashes")),
                    title=match.group("title").strip(),
                    line=index,
                )
            )

    sections: list[Section] = []
    for position, heading in enumerate(headings):
        if heading.level != section_level:
            continue
        end = len(lines)
        for following in headings[position + 1 :]:
            if following.level <= section_level:
                end = following.line - 1
                break
        body = "\n".join(lines[heading.line : end]).strip()
        sections.append(
            Section(title=heading.title, level=heading.level, line=heading.line, body=body)
        )

    return Document(raw=text, headings=headings, sections=sections)

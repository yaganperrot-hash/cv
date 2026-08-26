"""Évaluation des champs de `config.yml` contre un CV parsé."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config, FieldSpec
from .document import Document, Section, parse
from .text import normalize


@dataclass(frozen=True)
class SubResult:
    id: str
    label: str
    ok: bool
    help: str = ""


@dataclass(frozen=True)
class FieldResult:
    id: str
    label: str
    ok: bool
    required: bool = True
    detail: str = ""
    help: str = ""
    evidence: str = ""
    sub_results: tuple[SubResult, ...] = ()

    @property
    def blocking(self) -> bool:
        """Un champ requis absent fait échouer le check (et donc la CI)."""
        return self.required and not self.ok


@dataclass
class Report:
    source: str
    results: tuple[FieldResult, ...] = field(default_factory=tuple)

    @property
    def missing(self) -> tuple[FieldResult, ...]:
        return tuple(r for r in self.results if not r.ok)

    @property
    def blocking(self) -> tuple[FieldResult, ...]:
        return tuple(r for r in self.results if r.blocking)

    @property
    def present_count(self) -> int:
        return sum(1 for r in self.results if r.ok)

    @property
    def ok(self) -> bool:
        return not self.blocking

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def check_file(path: str | Path, config: Config) -> Report:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return check_text(text, config, source=str(path))


def check_text(text: str, config: Config, source: str = "<cv>") -> Report:
    document = parse(text, section_level=config.section_level)
    sections: dict[str, Section | None] = {}
    results: list[FieldResult] = []

    # Les sections d'abord : les autres champs peuvent cibler leur contenu.
    for spec in config.fields:
        if spec.type == "section":
            result, matched = _check_section(spec, document)
            sections[spec.id] = matched
            results.append(result)

    for spec in config.fields:
        if spec.type == "section":
            continue
        if spec.type == "heading":
            results.append(_check_heading(spec, document))
        elif spec.type == "regex":
            results.append(_check_regex(spec, document, sections))
        elif spec.type == "all_of":
            results.append(_check_all_of(spec, document, sections))

    order = {spec.id: index for index, spec in enumerate(config.fields)}
    results.sort(key=lambda r: order[r.id])
    return Report(source=source, results=tuple(results))


def _haystack(
    spec: FieldSpec, document: Document, sections: dict[str, Section | None]
) -> tuple[str, str | None]:
    """Retourne (texte à fouiller, raison d'échec si le scope est introuvable)."""
    section_id = spec.scope_section_id
    if section_id is None:
        return document.raw, None
    section = sections.get(section_id)
    if section is None:
        return "", f"la section ciblée (`{section_id}`) est absente"
    return section.body, None


def _search(spec: FieldSpec, pattern: re.Pattern[str], text: str) -> re.Match[str] | None:
    return pattern.search(normalize(text) if spec.normalize else text)


def _evidence(text: str, match: re.Match[str] | None, normalized: bool) -> str:
    if match is None:
        return ""
    if normalized:
        # La normalisation préserve les positions : on peut réafficher
        # l'extrait d'origine, accents compris.
        snippet = text[match.start() : match.end()]
        if len(snippet) == len(match.group(0)):
            return snippet.strip()
    return match.group(0).strip()


def _check_heading(spec: FieldSpec, document: Document) -> FieldResult:
    candidates = document.headings_at(spec.level)
    if not candidates:
        return FieldResult(
            id=spec.id,
            label=spec.label,
            ok=False,
            required=spec.required,
            detail=f"aucun titre de niveau {spec.level} (`{'#' * spec.level} …`) dans le CV",
            help=spec.help,
        )
    for heading in candidates:
        title = normalize(heading.title) if spec.normalize else heading.title
        if spec.pattern is not None and spec.pattern.search(title):
            return FieldResult(
                id=spec.id,
                label=spec.label,
                ok=True,
                required=spec.required,
                evidence=heading.title,
            )
    return FieldResult(
        id=spec.id,
        label=spec.label,
        ok=False,
        required=spec.required,
        detail=f"titre trouvé (« {candidates[0].title} ») mais format inattendu",
        help=spec.help,
    )


def _check_section(spec: FieldSpec, document: Document) -> tuple[FieldResult, Section | None]:
    aliases = [normalize(t) for t in spec.titles]
    matched: Section | None = None
    for section in document.sections:
        title = normalize(section.title)
        if any(alias == title for alias in aliases) or any(alias in title for alias in aliases):
            matched = section
            break

    if matched is None:
        return (
            FieldResult(
                id=spec.id,
                label=spec.label,
                ok=False,
                required=spec.required,
                detail="section absente (titres acceptés : "
                + ", ".join(f"« {t} »" for t in spec.titles)
                + ")",
                help=spec.help,
            ),
            None,
        )

    if matched.word_count < spec.min_words:
        return (
            FieldResult(
                id=spec.id,
                label=spec.label,
                ok=False,
                required=spec.required,
                detail=(
                    f"section « {matched.title} » présente mais quasi vide "
                    f"({matched.word_count} mot(s), minimum {spec.min_words})"
                ),
                help=spec.help,
                evidence=matched.title,
            ),
            matched,
        )

    return (
        FieldResult(
            id=spec.id,
            label=spec.label,
            ok=True,
            required=spec.required,
            evidence=f"« {matched.title} » (ligne {matched.line}, {matched.word_count} mots)",
        ),
        matched,
    )


def _check_regex(
    spec: FieldSpec, document: Document, sections: dict[str, Section | None]
) -> FieldResult:
    text, scope_error = _haystack(spec, document, sections)
    if scope_error:
        return FieldResult(
            id=spec.id,
            label=spec.label,
            ok=False,
            required=spec.required,
            detail=scope_error,
            help=spec.help,
        )
    assert spec.pattern is not None
    match = _search(spec, spec.pattern, text)
    if match is None:
        return FieldResult(
            id=spec.id,
            label=spec.label,
            ok=False,
            required=spec.required,
            detail="introuvable ou format invalide",
            help=spec.help,
        )
    return FieldResult(
        id=spec.id,
        label=spec.label,
        ok=True,
        required=spec.required,
        evidence=_evidence(text, match, spec.normalize),
    )


def _check_all_of(
    spec: FieldSpec, document: Document, sections: dict[str, Section | None]
) -> FieldResult:
    text, scope_error = _haystack(spec, document, sections)
    subs: list[SubResult] = []
    for rule in spec.rules:
        found = False if scope_error else _search(spec, rule.pattern, text) is not None
        subs.append(SubResult(id=rule.id, label=rule.label, ok=found, help=rule.help))

    missing = [s for s in subs if not s.ok]
    if not missing:
        return FieldResult(
            id=spec.id,
            label=spec.label,
            ok=True,
            required=spec.required,
            evidence=f"{len(subs)}/{len(subs)} mentions attendues trouvées",
            sub_results=tuple(subs),
        )
    detail = scope_error or "mention(s) manquante(s) : " + ", ".join(s.label for s in missing)
    return FieldResult(
        id=spec.id,
        label=spec.label,
        ok=False,
        required=spec.required,
        detail=detail,
        help=spec.help,
        sub_results=tuple(subs),
    )

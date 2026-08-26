"""Rendu du rapport : console lisible + artefact Markdown/texte."""

from __future__ import annotations

import os
import sys
from datetime import date

from .checker import FieldResult, Report

OK_MARK = "OK"
KO_MARK = "MANQUE"


class _Palette:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def _wrap(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    def green(self, text: str) -> str:
        return self._wrap("32", text)

    def red(self, text: str) -> str:
        return self._wrap("31", text)

    def yellow(self, text: str) -> str:
        return self._wrap("33", text)

    def bold(self, text: str) -> str:
        return self._wrap("1", text)

    def dim(self, text: str) -> str:
        return self._wrap("2", text)


def color_enabled(stream=sys.stdout, force: bool | None = None) -> bool:
    if force is not None:
        return force
    if os.environ.get("NO_COLOR"):
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def render_console(report: Report, color: bool = False) -> str:
    """Rapport console : une ligne par champ, l'aide sous les champs manquants."""
    palette = _Palette(color)
    width = max((len(r.label) for r in report.results), default=0)
    lines = [
        palette.bold("Vérification du CV"),
        palette.dim(f"source : {report.source}"),
        "",
    ]

    # Le gabarit est appliqué AVANT la couleur : les séquences ANSI ne comptent
    # pas dans la largeur d'une colonne.
    tag_width = max(len(OK_MARK), len(KO_MARK), len("CONSEIL")) + 2

    for result in report.results:
        if result.ok:
            tag = palette.green(f"[{OK_MARK}]".ljust(tag_width))
            info = palette.dim(result.evidence)
        elif result.required:
            tag = palette.red(f"[{KO_MARK}]".ljust(tag_width))
            info = result.detail
        else:
            tag = palette.yellow("[CONSEIL]".ljust(tag_width))
            info = result.detail
        lines.append(f"  {tag} {result.label.ljust(width)}  {info}".rstrip())
        lines.extend(_detail_lines(result, palette))

    lines.append("")
    total = len(report.results)
    summary = f"{report.present_count}/{total} champs présents"
    if report.ok:
        lines.append(palette.green(f"Résultat : {summary} — CV conforme."))
    else:
        missing = ", ".join(r.label for r in report.blocking)
        lines.append(palette.red(f"Résultat : {summary} — à compléter : {missing}."))
    return "\n".join(lines)


def _detail_lines(result: FieldResult, palette: _Palette) -> list[str]:
    if result.ok:
        return []
    lines = []
    for sub in result.sub_results:
        if not sub.ok:
            lines.append(palette.dim(f"        - manque : {sub.label}"))
    if result.help:
        for paragraph in _wrap(result.help, 80):
            lines.append(palette.yellow(f"        -> {paragraph}"))
    return lines


def _wrap(text: str, width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines


def render_markdown(report: Report) -> str:
    """Artefact archivable, lisible dans une PR ou dans les artefacts CI."""
    status = "✅ conforme" if report.ok else "❌ incomplet"
    lines = [
        "# Rapport de vérification du CV",
        "",
        f"- **Source** : `{report.source}`",
        f"- **Date** : {date.today().isoformat()}",
        f"- **Statut** : {status}",
        f"- **Champs présents** : {report.present_count}/{len(report.results)}",
        "",
        "| Champ | Statut | Détail |",
        "| --- | --- | --- |",
    ]
    for result in report.results:
        if result.ok:
            status_cell = "✅ présent"
            detail = result.evidence
        elif result.required:
            status_cell = "❌ manquant"
            detail = result.detail
        else:
            status_cell = "⚠️ conseillé"
            detail = result.detail
        lines.append(f"| {result.label} | {status_cell} | {_cell(detail)} |")

    missing = [r for r in report.results if not r.ok]
    if missing:
        lines += ["", "## À corriger", ""]
        for result in missing:
            lines.append(f"### {result.label}")
            lines.append("")
            lines.append(f"- {result.detail}")
            for sub in result.sub_results:
                if not sub.ok:
                    lines.append(f"- Manque : {sub.label}")
            if result.help:
                lines.append(f"- **Aide** : {result.help}")
            lines.append("")
    else:
        lines += ["", "Tous les champs minimum sont présents.", ""]
    return "\n".join(lines).rstrip() + "\n"


def render_text(report: Report) -> str:
    return render_console(report, color=False) + "\n"


def _cell(text: str) -> str:
    return (text or "—").replace("|", "\\|").replace("\n", " ")

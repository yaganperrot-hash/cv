"""Point d'entrée console : `python check_cv.py <cv.md>` ou `python check_cv.py data/`.

Codes de sortie :
  0 — tous les champs requis sont présents (ou tous les CV conformes)
  1 — au moins un champ requis manque (la CI passe au rouge)
  2 — erreur d'exécution (fichier ou config introuvable / invalide)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from . import report as report_module
from .checker import Report, check_file
from .config import ConfigError, load

EXIT_OK = 0
EXIT_INCOMPLETE = 1
EXIT_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_cv",
        description="Vérifie qu'un CV Markdown contient les champs minimum attendus.",
    )
    parser.add_argument(
        "cv",
        nargs="+",
        help="chemin(s) du CV ou dossier(s) contenant des .md",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yml",
        help="fichier de configuration des champs (défaut : config.yml)",
    )
    parser.add_argument(
        "-r",
        "--report",
        default=None,
        metavar="CHEMIN",
        help="écrit aussi le rapport dans un fichier (.md → Markdown, sinon texte)",
    )
    parser.add_argument("--no-color", action="store_true", help="désactive la couleur")
    parser.add_argument("--json", action="store_true", help="sortie JSON (pour tableau de bord)")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="n'affiche que la ligne de résultat"
    )
    parser.add_argument("--version", action="version", version=f"check_cv {__version__}")
    return parser


def _resolve_paths(raw_paths: list[str]) -> list[Path]:
    """Résout les chemins : un dossier → ses *.md, triés par nom."""
    paths: list[Path] = []
    for raw in raw_paths:
        p = Path(raw)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.md")))
        else:
            paths.append(p)
    return paths


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = load(args.config)
    except ConfigError as exc:
        print(f"Erreur de configuration : {exc}", file=sys.stderr)
        return EXIT_ERROR

    cv_paths = _resolve_paths(args.cv)
    if not cv_paths:
        print("Erreur : aucun fichier .md trouvé.", file=sys.stderr)
        return EXIT_ERROR

    for p in cv_paths:
        if not p.is_file():
            print(f"Erreur : CV introuvable : {p}", file=sys.stderr)
            return EXIT_ERROR

    batch = len(cv_paths) > 1
    reports: list[Report] = []

    for cv_path in cv_paths:
        result = check_file(cv_path, config)
        reports.append(result)

        if args.json:
            pass  # JSON en batch : rendu groupé à la fin
        else:
            color = report_module.color_enabled(force=False if args.no_color else None)
            rendered = report_module.render_console(result, color=color)
            print(rendered.splitlines()[-1] if args.quiet else rendered)
            if batch and not args.quiet:
                print()

    if args.json:
        if batch:
            print(report_module.render_json_batch(reports), end="")
        else:
            print(report_module.render_json(reports[0]), end="")

    if batch and not args.json and not args.quiet:
        _print_summary(reports)

    if args.report:
        _write_report(args, reports)

    all_ok = all(r.ok for r in reports)
    return EXIT_OK if all_ok else EXIT_INCOMPLETE


def _print_summary(reports: list[Report]) -> None:
    """Récapitulatif final en mode batch."""
    print("=" * 60)
    print("Récapitulatif")
    print("=" * 60)
    for r in reports:
        total = len(r.results)
        status = "OK" if r.ok else "INCOMPLET"
        print(f"  {r.source}: {r.present_count}/{total} — {status}")
    ok_count = sum(1 for r in reports if r.ok)
    print(f"\n{ok_count}/{len(reports)} CV conformes.")


def _write_report(args: argparse.Namespace, reports: list[Report]) -> None:
    destination = Path(args.report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    is_md = destination.suffix.lower() in {".md", ".markdown"}
    if len(reports) == 1:
        body = (
            report_module.render_markdown(reports[0])
            if is_md
            else report_module.render_text(reports[0])
        )
    else:
        parts = []
        for r in reports:
            parts.append(
                report_module.render_markdown(r) if is_md else report_module.render_text(r)
            )
        body = ("\n---\n\n" if is_md else "\n").join(parts)
    destination.write_text(body, encoding="utf-8")
    if not args.quiet:
        print(f"\nRapport écrit dans {destination}")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""Point d'entrée console : `python check_cv.py <cv.md>`.

Codes de sortie :
  0 — tous les champs requis sont présents
  1 — au moins un champ requis manque (la CI passe au rouge)
  2 — erreur d'exécution (fichier ou config introuvable / invalide)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, report as report_module
from .checker import check_file
from .config import ConfigError, load

EXIT_OK = 0
EXIT_INCOMPLETE = 1
EXIT_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_cv",
        description="Vérifie qu'un CV Markdown contient les champs minimum attendus.",
    )
    parser.add_argument("cv", help="chemin du CV au format Markdown")
    parser.add_argument(
        "-c", "--config", default="config.yml",
        help="fichier de configuration des champs (défaut : config.yml)",
    )
    parser.add_argument(
        "-r", "--report", default=None, metavar="CHEMIN",
        help="écrit aussi le rapport dans un fichier (.md → Markdown, sinon texte)",
    )
    parser.add_argument("--no-color", action="store_true", help="désactive la couleur")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="n'affiche que la ligne de résultat")
    parser.add_argument("--version", action="version", version=f"check_cv {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    cv_path = Path(args.cv)
    if not cv_path.is_file():
        print(f"Erreur : CV introuvable : {cv_path}", file=sys.stderr)
        return EXIT_ERROR

    try:
        config = load(args.config)
    except ConfigError as exc:
        print(f"Erreur de configuration : {exc}", file=sys.stderr)
        return EXIT_ERROR

    result = check_file(cv_path, config)

    color = report_module.color_enabled(force=False if args.no_color else None)
    rendered = report_module.render_console(result, color=color)
    print(rendered.splitlines()[-1] if args.quiet else rendered)

    if args.report:
        destination = Path(args.report)
        destination.parent.mkdir(parents=True, exist_ok=True)
        body = (
            report_module.render_markdown(result)
            if destination.suffix.lower() in {".md", ".markdown"}
            else report_module.render_text(result)
        )
        destination.write_text(body, encoding="utf-8")
        if not args.quiet:
            print(f"\nRapport écrit dans {destination}")

    return result.exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

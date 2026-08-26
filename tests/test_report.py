"""Tests du rendu console : forme, flèches, alignement.

BUG-002 est passé entre les mailles parce que les tests ne vérifiaient que la
présence des libellés, pas la structure visuelle du rapport.
"""

from cv_checker.checker import check_file
from cv_checker.report import render_console


def test_help_arrow_only_on_first_line(incomplete_path, config):
    """La flèche `->` apparaît uniquement sur la première ligne d'aide."""
    report = check_file(incomplete_path, config)
    rendered = render_console(report, color=False)
    arrow_lines = [line for line in rendered.splitlines() if "-> " in line]
    continuation_lines = [
        line
        for line in rendered.splitlines()
        if line.startswith("        ")
        and "-> " not in line
        and line.strip()
        and not line.strip().startswith("[")
    ]

    assert arrow_lines, "il doit y avoir au moins une ligne d'aide avec flèche"
    for line in continuation_lines:
        assert "->" not in line, (
            f"la flèche ne doit pas apparaître sur une ligne de suite : {line!r}"
        )


def test_help_block_appears_only_under_missing_fields(incomplete_path, config):
    """Les lignes d'aide n'apparaissent que sous les champs manquants."""
    report = check_file(incomplete_path, config)
    rendered = render_console(report, color=False)
    lines = rendered.splitlines()

    for i, line in enumerate(lines):
        if "[OK]" in line and i + 1 < len(lines):
            next_line = lines[i + 1]
            assert "-> " not in next_line, (
                f"aide inattendue sous un champ OK : {line!r} suivi de {next_line!r}"
            )


def test_ok_fields_show_evidence(template_path, config):
    """Un champ OK affiche l'evidence (le contenu trouvé)."""
    report = check_file(template_path, config)
    rendered = render_console(report, color=False)
    for line in rendered.splitlines():
        if "[OK]" in line:
            parts = line.split("[OK]", 1)
            assert len(parts[1].strip()) > 0, f"pas d'evidence après [OK] : {line!r}"


def test_missing_fields_show_detail(incomplete_path, config):
    """Un champ MANQUE affiche un détail explicatif."""
    report = check_file(incomplete_path, config)
    rendered = render_console(report, color=False)
    manque_lines = [line for line in rendered.splitlines() if "[MANQUE]" in line]
    assert manque_lines, "il doit y avoir des champs manquants"
    for line in manque_lines:
        parts = line.split("[MANQUE]", 1)
        assert len(parts[1].strip()) > 0, f"pas de détail après [MANQUE] : {line!r}"


def test_summary_line_format(incomplete_path, config):
    """La ligne de résumé a le format attendu."""
    report = check_file(incomplete_path, config)
    rendered = render_console(report, color=False)
    last_line = rendered.splitlines()[-1]
    assert "Résultat :" in last_line
    assert "champs présents" in last_line
    assert "à compléter" in last_line


def test_valid_cv_summary(template_path, config):
    """Un CV valide a la mention 'CV conforme'."""
    report = check_file(template_path, config)
    rendered = render_console(report, color=False)
    last_line = rendered.splitlines()[-1]
    assert "CV conforme" in last_line


def test_header_contains_source(template_path, config):
    """L'en-tête du rapport contient le chemin source."""
    report = check_file(template_path, config)
    rendered = render_console(report, color=False)
    assert "source" in rendered.splitlines()[1].lower()

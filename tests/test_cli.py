"""Contrat avec la CI : codes de sortie, rapport console et artefact."""

from cv_checker import report as report_module
from cv_checker.checker import check_file
from cv_checker.cli import main


def test_cli_returns_zero_on_the_template(template_path, repo_root, capsys):
    code = main([str(template_path), "--config", str(repo_root / "config.yml"), "--no-color"])
    assert code == 0
    assert "CV conforme" in capsys.readouterr().out


def test_cli_returns_one_when_fields_are_missing(incomplete_path, repo_root, capsys):
    code = main([str(incomplete_path), "--config", str(repo_root / "config.yml"), "--no-color"])
    assert code == 1
    out = capsys.readouterr().out
    assert "Téléphone" in out and "à compléter" in out


def test_cli_returns_two_when_the_cv_is_missing(tmp_path, repo_root, capsys):
    code = main([str(tmp_path / "absent.md"), "--config", str(repo_root / "config.yml")])
    assert code == 2
    assert "introuvable" in capsys.readouterr().err


def test_cli_returns_two_on_a_broken_config(template_path, tmp_path, capsys):
    broken = tmp_path / "config.yml"
    broken.write_text("fields: []\n", encoding="utf-8")
    assert main([str(template_path), "--config", str(broken)]) == 2
    assert "configuration" in capsys.readouterr().err


def test_cli_writes_a_markdown_report(incomplete_path, repo_root, tmp_path, capsys):
    destination = tmp_path / "out" / "cv-report.md"
    code = main(
        [
            str(incomplete_path),
            "--config", str(repo_root / "config.yml"),
            "--report", str(destination),
            "--no-color",
        ]
    )
    capsys.readouterr()
    assert code == 1
    body = destination.read_text(encoding="utf-8")
    assert body.startswith("# Rapport de vérification du CV")
    assert "❌ manquant" in body and "## À corriger" in body


def test_cli_writes_a_text_report(template_path, repo_root, tmp_path, capsys):
    destination = tmp_path / "cv-report.txt"
    assert main(
        [str(template_path), "--config", str(repo_root / "config.yml"),
         "--report", str(destination), "--no-color", "--quiet"]
    ) == 0
    capsys.readouterr()
    assert "8/8 champs présents" in destination.read_text(encoding="utf-8")


def test_quiet_mode_prints_only_the_verdict(template_path, repo_root, capsys):
    main([str(template_path), "--config", str(repo_root / "config.yml"), "--no-color", "-q"])
    assert capsys.readouterr().out.strip().startswith("Résultat :")


def test_markdown_report_of_a_valid_cv_has_no_todo_section(template_path, config):
    body = report_module.render_markdown(check_file(template_path, config))
    assert "✅ conforme" in body
    assert "## À corriger" not in body


def test_console_report_can_be_colorized(template_path, config):
    colored = report_module.render_console(check_file(template_path, config), color=True)
    assert "\033[" in colored

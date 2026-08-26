"""Le cœur du contrat : un CV complet passe, un CV incomplet échoue."""

import pytest

from cv_checker.checker import check_file, check_text


def test_template_passes_all_checks(template_path, config):
    report = check_file(template_path, config)
    assert report.missing == ()
    assert report.ok is True
    assert report.exit_code == 0
    assert report.present_count == len(config.fields)


def test_incomplete_cv_fails_with_the_expected_fields(incomplete_path, config):
    report = check_file(incomplete_path, config)
    assert report.exit_code == 1
    missing = {result.id for result in report.missing}
    assert missing == {
        "full_name",
        "email",
        "phone",
        "formation",
        "competences",
        "rythme_alternance",
        "disponibilite",
    }
    assert {result.id for result in report.results if result.ok} == {"experience"}


def test_partial_cv_fails_on_the_three_usual_omissions(partial_path, config):
    """Le cas réaliste : un CV correct auquel il manque les oublis classiques."""
    report = check_file(partial_path, config)
    assert report.exit_code == 1
    assert {result.id for result in report.missing} == {
        "phone",
        "rythme_alternance",
        "disponibilite",
    }
    rythme = next(r for r in report.results if r.id == "rythme_alternance")
    assert [sub.id for sub in rythme.sub_results if not sub.ok] == ["elearning"]


def test_every_missing_field_carries_a_help_message(incomplete_path, config):
    report = check_file(incomplete_path, config)
    for result in report.missing:
        assert result.help, f"pas de message d'aide pour {result.id}"
        assert result.detail


def _result(text, config, field_id):
    return next(r for r in check_text(text, config).results if r.id == field_id)


@pytest.mark.parametrize(
    "heading, expected",
    [("# Camille Dubois", True), ("# Camille", False), ("# 2025", False), ("", False)],
)
def test_full_name_requires_first_and_last_name(heading, expected, config):
    assert _result(heading + "\n", config, "full_name").ok is expected


@pytest.mark.parametrize(
    "line, expected",
    [
        ("camille.dubois@example.com", True),
        ("camille+cv@sous.domaine.fr", True),
        ("camille[at]example.com", False),
        ("camille@example", False),
        ("camille@.com", False),
    ],
)
def test_email_format_is_validated(line, expected, config):
    assert _result(f"# Camille Dubois\n\n{line}\n", config, "email").ok is expected


@pytest.mark.parametrize(
    "line, expected",
    [
        ("06 12 34 56 78", True),
        ("06.12.34.56.78", True),
        ("+33 6 12 34 56 78", True),
        ("0612345678", True),
        ("+44 7911 123456", True),
        ("+1 555 123 4567", True),
        ("+49 170 1234567", True),
        ("+352 621 123 456", True),
        ("06 12 34 56", False),
        ("2025 promotion 12345", False),
        ("+0 123 456", False),
    ],
)
def test_phone_format_is_validated(line, expected, config):
    assert _result(f"# Camille Dubois\n\n{line}\n", config, "phone").ok is expected


def test_section_present_but_empty_is_rejected(config):
    result = _result("# Camille Dubois\n\n## Formation\n\nETNA.\n", config, "formation")
    assert result.ok is False
    assert "quasi vide" in result.detail


def test_section_title_variants_are_accepted(config):
    text = "# Camille Dubois\n\n## Expériences professionnelles\n\n" + "mot " * 10 + "\n"
    assert _result(text, config, "experience").ok is True


ALTERNANCE = (
    "- Rythme : 3 semaines en entreprise, 1 vendredi sur 3 à l'école (ETNA),\n"
    "  et 33 h d'e-learning sur 3 semaines.\n"
)


def test_alternance_rhythm_needs_all_three_mentions(config):
    result = _result(f"# Camille Dubois\n\n{ALTERNANCE}", config, "rythme_alternance")
    assert result.ok is True
    assert all(sub.ok for sub in result.sub_results)


def test_alternance_rhythm_reports_the_missing_mention(config):
    partial = "- Rythme : 3 semaines en entreprise, 1 vendredi sur 3 à l'école.\n"
    result = _result(f"# Camille Dubois\n\n{partial}", config, "rythme_alternance")
    assert result.ok is False
    assert [sub.id for sub in result.sub_results if not sub.ok] == ["elearning"]
    assert "33 h" in result.detail


@pytest.mark.parametrize(
    "line, expected",
    [
        ("Disponibilité : dès que possible", True),
        ("Disponibilite : des que possible", True),
        ("Disponibilité : à partir de septembre", False),
    ],
)
def test_availability_expects_the_agreed_wording(line, expected, config):
    assert _result(f"# Camille Dubois\n\n{line}\n", config, "disponibilite").ok is expected

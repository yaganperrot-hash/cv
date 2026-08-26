"""La config est la source de vérité : elle doit être validée sévèrement."""

import pytest

from cv_checker import config as config_module
from cv_checker.config import ConfigError

MINIMAL = {
    "fields": [
        {"id": "email", "label": "Email", "type": "regex", "pattern": r"\S+@\S+"},
    ]
}


def test_repo_config_declares_the_expected_fields(config):
    assert [f.id for f in config.fields] == [
        "full_name",
        "email",
        "phone",
        "formation",
        "experience",
        "competences",
        "rythme_alternance",
        "disponibilite",
    ]
    assert config.section_level == 2
    assert all(f.help for f in config.fields), "chaque champ doit porter un message d'aide"


def test_parse_accepts_a_minimal_config():
    parsed = config_module.parse(MINIMAL)
    assert parsed.by_id("email") is not None
    assert parsed.by_id("email").required is True


def test_missing_fields_key_is_rejected():
    with pytest.raises(ConfigError, match="fields"):
        config_module.parse({"version": 1})


def test_unknown_field_type_is_rejected():
    with pytest.raises(ConfigError, match="inconnu"):
        config_module.parse({"fields": [{"id": "x", "type": "magique"}]})


def test_regex_field_without_pattern_is_rejected():
    with pytest.raises(ConfigError, match="pattern"):
        config_module.parse({"fields": [{"id": "x", "type": "regex"}]})


def test_invalid_regex_is_reported_with_its_field():
    with pytest.raises(ConfigError, match="invalide"):
        config_module.parse({"fields": [{"id": "x", "type": "regex", "pattern": "([a-z"}]})


def test_duplicate_field_id_is_rejected():
    with pytest.raises(ConfigError, match="dupliqué"):
        config_module.parse({"fields": [MINIMAL["fields"][0], MINIMAL["fields"][0]]})


def test_scope_pointing_to_an_unknown_section_is_rejected():
    with pytest.raises(ConfigError, match="scope"):
        config_module.parse(
            {
                "fields": [
                    {
                        "id": "x",
                        "type": "regex",
                        "pattern": "a",
                        "scope": "section:inexistante",
                    }
                ]
            }
        )


def test_scope_can_target_a_declared_section():
    parsed = config_module.parse(
        {
            "fields": [
                {"id": "formation", "type": "section", "titles": ["formation"]},
                {"id": "diplome", "type": "regex", "pattern": "bts", "scope": "section:formation"},
            ]
        }
    )
    assert parsed.by_id("diplome").scope_section_id == "formation"


def test_missing_config_file_is_reported(tmp_path):
    with pytest.raises(ConfigError, match="introuvable"):
        config_module.load(tmp_path / "absent.yml")

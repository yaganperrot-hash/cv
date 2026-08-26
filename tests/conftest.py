"""Fixtures partagées : chemins du dépôt et config réelle."""

from __future__ import annotations

from pathlib import Path

import pytest

from cv_checker import config as config_module

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def config():
    """La config réelle du dépôt : les tests protègent ce qui tourne en CI."""
    return config_module.load(ROOT / "config.yml")


@pytest.fixture(scope="session")
def template_path() -> Path:
    return ROOT / "templates" / "cv-template.md"


@pytest.fixture(scope="session")
def incomplete_path() -> Path:
    return FIXTURES / "cv-incomplet.md"


@pytest.fixture(scope="session")
def partial_path() -> Path:
    """CV crédible mais amputé des trois oublis les plus fréquents."""
    return FIXTURES / "cv-partiel.md"

"""Chargement et validation de `config.yml`.

Toute la définition des champs attendus vient d'ici : le reste du code ne
connaît que les *types* de règles, jamais les champs eux-mêmes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

FIELD_TYPES = {"heading", "section", "regex", "all_of"}
DEFAULT_SECTION_LEVEL = 2


class ConfigError(ValueError):
    """Config absente, mal formée ou incohérente."""


@dataclass(frozen=True)
class SubRule:
    """Une des conditions d'un champ `all_of`."""

    id: str
    label: str
    pattern: re.Pattern[str]
    help: str = ""


@dataclass(frozen=True)
class FieldSpec:
    id: str
    label: str
    type: str
    help: str = ""
    required: bool = True
    normalize: bool = True
    scope: str = "document"
    pattern: re.Pattern[str] | None = None
    level: int = 1
    titles: tuple[str, ...] = ()
    min_words: int = 0
    rules: tuple[SubRule, ...] = ()

    @property
    def scope_section_id(self) -> str | None:
        """Id de la section ciblée, ou None si le scope est le document."""
        if self.scope.startswith("section:"):
            return self.scope.split(":", 1)[1].strip()
        return None


@dataclass(frozen=True)
class Config:
    version: int = 1
    section_level: int = DEFAULT_SECTION_LEVEL
    fields: tuple[FieldSpec, ...] = field(default_factory=tuple)

    def by_id(self, field_id: str) -> FieldSpec | None:
        return next((f for f in self.fields if f.id == field_id), None)


def load(path: str | Path) -> Config:
    """Lit un `config.yml` et le valide."""
    path = Path(path)
    if not path.is_file():
        raise ConfigError(f"config introuvable : {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - dépend de PyYAML
        raise ConfigError(f"YAML invalide dans {path} : {exc}") from exc
    return parse(data, source=str(path))


def parse(data: Any, source: str = "<config>") -> Config:
    if not isinstance(data, dict):
        raise ConfigError(f"{source} : la racine doit être un mapping YAML")

    raw_fields = data.get("fields")
    if not isinstance(raw_fields, list) or not raw_fields:
        raise ConfigError(f"{source} : la clé `fields` doit être une liste non vide")

    parsing = data.get("parsing") or {}
    section_level = int(parsing.get("section_level", DEFAULT_SECTION_LEVEL))

    specs: list[FieldSpec] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_fields, start=1):
        spec = _parse_field(raw, index, source)
        if spec.id in seen:
            raise ConfigError(f"{source} : id de champ dupliqué `{spec.id}`")
        seen.add(spec.id)
        specs.append(spec)

    config = Config(
        version=int(data.get("version", 1)),
        section_level=section_level,
        fields=tuple(specs),
    )
    _validate_scopes(config, source)
    return config


def _parse_field(raw: Any, index: int, source: str) -> FieldSpec:
    where = f"{source} : champ #{index}"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} : chaque champ doit être un mapping")

    field_id = str(raw.get("id") or "").strip()
    if not field_id:
        raise ConfigError(f"{where} : clé `id` manquante")

    field_type = str(raw.get("type") or "").strip()
    if field_type not in FIELD_TYPES:
        raise ConfigError(
            f"{where} (`{field_id}`) : type `{field_type or '?'}` inconnu, "
            f"attendu parmi {sorted(FIELD_TYPES)}"
        )

    normalize = bool(raw.get("normalize", True))
    flags = re.IGNORECASE if normalize else 0

    pattern = None
    if raw.get("pattern") is not None:
        pattern = _compile(raw["pattern"], flags, f"{where} (`{field_id}`)")
    if field_type in {"heading", "regex"} and pattern is None:
        raise ConfigError(f"{where} (`{field_id}`) : un champ `{field_type}` exige `pattern`")

    titles = tuple(str(t) for t in (raw.get("titles") or ()))
    if field_type == "section" and not titles:
        raise ConfigError(f"{where} (`{field_id}`) : un champ `section` exige `titles`")

    sub_rules: list[SubRule] = []
    for position, sub in enumerate(raw.get("rules") or (), start=1):
        if not isinstance(sub, dict) or sub.get("pattern") is None:
            raise ConfigError(f"{where} (`{field_id}`) : règle #{position} sans `pattern`")
        sub_id = str(sub.get("id") or f"rule-{position}")
        sub_rules.append(
            SubRule(
                id=sub_id,
                label=str(sub.get("label") or sub_id),
                pattern=_compile(sub["pattern"], flags, f"{where} (`{field_id}`/{sub_id})"),
                help=str(sub.get("help") or ""),
            )
        )
    if field_type == "all_of" and not sub_rules:
        raise ConfigError(f"{where} (`{field_id}`) : un champ `all_of` exige `rules`")

    return FieldSpec(
        id=field_id,
        label=str(raw.get("label") or field_id),
        type=field_type,
        help=str(raw.get("help") or "").strip(),
        required=bool(raw.get("required", True)),
        normalize=normalize,
        scope=str(raw.get("scope") or "document").strip(),
        pattern=pattern,
        level=int(raw.get("level", 1)),
        titles=titles,
        min_words=int(raw.get("min_words", 0)),
        rules=tuple(sub_rules),
    )


def _compile(pattern: Any, flags: int, where: str) -> re.Pattern[str]:
    try:
        return re.compile(str(pattern), flags)
    except re.error as exc:
        raise ConfigError(f"{where} : expression régulière invalide ({exc})") from exc


def _validate_scopes(config: Config, source: str) -> None:
    section_ids = {f.id for f in config.fields if f.type == "section"}
    for spec in config.fields:
        target = spec.scope_section_id
        if target is None:
            if spec.scope != "document":
                raise ConfigError(
                    f"{source} : champ `{spec.id}` — scope `{spec.scope}` inconnu "
                    "(attendu `document` ou `section:<id>`)"
                )
        elif target not in section_ids:
            raise ConfigError(
                f"{source} : champ `{spec.id}` — scope `section:{target}` "
                "ne correspond à aucun champ de type `section`"
            )

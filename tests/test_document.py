"""Parseur Markdown : titres, bornes de sections, blocs de code."""

from cv_checker.document import parse
from cv_checker.text import count_words, normalize

MD = """# Camille Dubois

contact@example.com

## Formation

- ETNA

### Détail

Deux lignes de plus.

## Compétences

Python, Git

```python
# ceci n'est pas un titre
## non plus
```
"""


def test_headings_are_collected_with_levels_and_lines():
    document = parse(MD)
    assert [(h.level, h.title) for h in document.headings] == [
        (1, "Camille Dubois"),
        (2, "Formation"),
        (3, "Détail"),
        (2, "Compétences"),
    ]
    assert document.headings[0].line == 1


def test_code_fences_are_not_parsed_as_headings():
    document = parse(MD)
    assert all("ceci n'est pas un titre" not in h.title for h in document.headings)


def test_section_body_stops_at_next_section_but_keeps_subsections():
    document = parse(MD)
    formation = next(s for s in document.sections if s.title == "Formation")
    assert "Détail" in formation.body
    assert "Compétences" not in formation.body


def test_sections_only_at_configured_level():
    document = parse(MD, section_level=3)
    assert [s.title for s in document.sections] == ["Détail"]


def test_normalize_strips_accents_and_case():
    assert normalize("Dès que Possible — École") == "des que possible — ecole"


def test_count_words_ignores_markdown_punctuation():
    assert count_words("- **Python**, Git ;") == 2

# TASK-002 — Vérifier un lot de CV en une commande

- **Statut** : à faire
- **Créée le** : 2026-08-26
- **Branche** : `feat/batch`
- **Todo liée** : TODO-003

## Pourquoi

Côté école, on relit des dizaines de CV. Aujourd'hui `check_cv.py` prend un
seul fichier. Passer un dossier permettrait d'obtenir en une commande le
tableau de qui doit corriger quoi.

## Périmètre

**Inclus**
- `check_cv.py` accepte plusieurs chemins et/ou un dossier (`data/`).
- Un récapitulatif final : une ligne par CV, `n/8` champs présents.
- Code de sortie 1 dès qu'un seul CV est incomplet.
- Rapport Markdown agrégé (une section par CV).

**Exclus**
- Toute forme de stockage ou d'envoi des CV analysés : le lot reste local,
  jamais committé (RGPD).
- Une interface web.

## Critères d'acceptation

- [ ] `python check_cv.py data/` parcourt les `*.md` du dossier, triés par nom.
- [ ] Un dossier vide sort en code 2 avec un message explicite.
- [ ] Tests : dossier de 3 CV fictifs (2 conformes, 1 incomplet) → code 1.
- [ ] Le comportement mono-fichier existant reste identique.

## Notes techniques

`Report` devient un élément d'un `BatchReport` ; garder `render_console` pour
le détail d'un CV et ajouter un `render_summary` pour le tableau final.

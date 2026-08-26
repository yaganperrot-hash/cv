# Session du 2026-08-26 — Merge sur main

- **Branche** : `main` (tout mergé)
- **Point de départ** : `feat/gitlab-ci` et `setup` non mergées
- **État à l'arrivée** : ✅ tout sur `main`, 72 tests, CI verte

## Ce qui a été fait

1. **Merge PR #1** (`feat/gitlab-ci` → `setup`) via GitHub.
2. **Merge PR #2** (`setup` → `main`) via GitHub.
3. Branches `setup` et `feat/gitlab-ci` supprimées sur le remote.

Tout le travail est maintenant sur `main` :
- Vérificateur de CV (Python, 8 champs, config.yml)
- CI GitHub Actions (lint + check + tests)
- CI GitLab (check + commentaire sur commit)
- Sujet PRO-INTG (`tasks/TASK-003`)
- ruff, `--json`, mode batch, téléphones internationaux
- 72 tests

## Prochaines étapes

1. Tester la CI GitLab au premier push sur le serveur auto-hébergé (TODO-009).

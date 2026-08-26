# TODOs actives

> Convention : une ligne = une todo. Format `- [ ] (P1) TODO-000 — description`.
> Priorités : P1 (bloquant), P2 (important), P3 (confort).
> Une todo terminée part dans `todos/archive/YYYY-MM-DD-titre.md`.
> Dernière mise à jour : 2026-08-26 (fin de session).

## En cours

_(rien — la branche `setup` attend sa relecture)_

## À faire

- [ ] (P1) TODO-001 — Vérifier le premier run du workflow `check-cv` dans
      l'onglet *Actions* : la conversion pandoc n'a jamais tourné en local
      (pandoc absent de la machine de dev). Le push est fait, la CI a donc
      démarré.
- [ ] (P3) TODO-008 — Tester la *forme* du rendu console (bloc d'aide replié,
      flèche uniquement sur la première ligne) : BUG-002 est passé entre les
      mailles parce que les tests ne vérifiaient que la présence des libellés.
- [ ] (P2) TODO-002 — TASK-001 : mise en forme du `.docx` via
      `--reference-doc=templates/reference.docx`, sans casser la lisibilité ATS.
- [ ] (P2) TODO-003 — TASK-002 : accepter un dossier de CV (`python check_cv.py
      data/`) avec un récapitulatif en fin d'exécution.
- [ ] (P3) TODO-004 — Ajouter ruff (lint + format) au projet et à la CI.
- [ ] (P3) TODO-005 — Étendre la validation du téléphone aux numéros
      internationaux si des alternants hors France arrivent.
- [ ] (P3) TODO-006 — Ajouter un `--json` à la CLI pour brancher un tableau de
      bord côté école.

## Bloquées

- [ ] (P1) TODO-007 — Merger la PR `setup` → `main`. **Bloquée** : relecture
      humaine explicitement demandée, aucun merge automatique.
      https://github.com/yaganperrot-hash/cv/pull/new/setup

## Questions ouvertes

- Certains champs doivent-ils devenir « conseillés » (`required: false`) plutôt
  que bloquants ? Ex. LinkedIn, GitHub.
- Le rythme d'alternance (3 semaines / 1 vendredi sur 3 / 33 h) est-il le même
  pour toutes les promos ?

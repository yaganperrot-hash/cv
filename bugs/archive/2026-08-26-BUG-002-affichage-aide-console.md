# BUG-002 — Affichage illisible de l'aide sous un champ manquant

- **Statut** : résolu
- **Sévérité** : mineur
- **Détecté le** : 2026-08-26 (en passant le script sur `cv-partiel.md`)
- **Résolu le** : 2026-08-26 (commit `fix(report): allège l'affichage des champs manquants`)
- **Contexte** : `cv_checker/report.py`, rendu console

## Repro

1. `python check_cv.py tests/fixtures/cv-partiel.md --no-color`
2. Regarder le bloc du champ « Rythme d'alternance ».

## Attendu

Une flèche `->` introduisant le message d'aide, et la mention manquante citée
une seule fois.

## Obtenu

- Le préfixe `-> ` était répété au début de **chaque** ligne d'une aide repliée
  sur plusieurs lignes, cassant la lecture.
- La sous-règle manquante était affichée deux fois : une fois dans `detail`
  (« mention(s) manquante(s) : … ») et une fois par la boucle sur
  `sub_results`.

## Résolution

`_detail_lines()` ne rend plus que le message d'aide : la flèche n'apparaît que
sur la première ligne, les suivantes s'alignent dessous, et l'énumération des
sous-règles manquantes est laissée à `detail`, qui la faisait déjà.

## Leçon

Le rendu console n'était couvert que par des tests d'existence
(`"Téléphone" in out`). Un test sur la **forme** exacte du bloc d'aide reste à
écrire — noté en TODO-008.

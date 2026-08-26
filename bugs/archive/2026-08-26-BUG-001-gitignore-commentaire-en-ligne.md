# BUG-001 — Le `.gitignore` ne réactivait pas `templates/*.docx`

- **Statut** : résolu
- **Sévérité** : mineur
- **Détecté le** : 2026-08-26
- **Résolu le** : 2026-08-26 (commit `fix(gitignore): sort le commentaire de la ligne de négation`)
- **Contexte** : `.gitignore`, règle d'exception pour un futur `reference.docx`

## Repro

1. Écrire dans `.gitignore` : `!templates/*.docx    # exception : …`
2. `git check-ignore -v templates/reference.docx`

## Attendu

Le fichier n'est pas ignoré (la négation s'applique).

## Obtenu

Le fichier reste ignoré : git ne gère pas les commentaires en fin de ligne, le
motif valait littéralement `!templates/*.docx    # exception : …` et ne
correspondait à aucun fichier.

## Résolution

Commentaire déplacé sur sa propre ligne, au-dessus du motif. Seul un `#` en
début de ligne introduit un commentaire dans un `.gitignore`.

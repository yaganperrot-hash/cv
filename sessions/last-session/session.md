# Session du 2026-08-26 — Sujet PRO-INTG

- **Branche** : `feat/gitlab-ci` (suite)
- **Point de départ** : CI GitLab créée, besoin du sujet étudiant pour le module
- **État à l'arrivée** : ✅ sujet rédigé, prêt à relecture

## Ce qui a été fait

1. **`tasks/TASK-003-sujet-pro-intg.md`** : sujet complet du module PRO-INTG / Cv.
   - Calqué sur le format des sujets ETNA (PathCraft comme modèle).
   - 14 jours, individuel, validation automatique par CI GitLab.
   - Contenu : modalités, objectifs, principe du pipeline, consignes en 5 étapes,
     les 8 champs obligatoires détaillés, structure recommandée (squelette MD),
     tableau de validation, section « ce qu'il ne faut PAS faire », commandes
     utiles, FAQ.
2. **Archivage** de la session précédente (GitLab CI) dans
   `sessions/archive/2026-08-26-gitlab-ci.md`.

## Décisions prises

- **Première étape = validation CI uniquement** : pas de critère humain ni de
  mise en forme pour ce premier jet. La seule condition : pipeline vert (8/8).
- **L'étudiant ne touche pas au code** : il écrit son CV en Markdown, pousse,
  lit le retour CI, corrige, repousse.
- **Le sujet vit dans `tasks/`** conformément aux conventions du dépôt.

## Prochaines étapes

1. Relire et valider le sujet (ton, complétude, clarté pour un étudiant débutant).
2. Reprendre les TODOs existantes (TODO-001, TODO-009, puis TASK-001/002).

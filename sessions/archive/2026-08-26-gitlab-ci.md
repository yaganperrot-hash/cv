# Session du 2026-08-26 — Migration GitLab CI

- **Branche** : `feat/gitlab-ci` (branchée sur `setup`, **non mergée**)
- **Point de départ** : CI GitHub Actions fonctionnelle, besoin d'une CI GitLab
  pour le déploiement sur GitLab auto-hébergé (un repo par étudiant)
- **État à l'arrivée** : ✅ fichiers créés, tests verts (51 passed, template 8/8)

## Ce qui a été fait

1. **`.gitlab-ci.yml`** : pipeline à 2 stages (check + build).
   - Stage `check` : détecte le CV automatiquement, installe PyYAML, lance
     `check_cv.py`, poste le rapport en commentaire sur le commit via l'API
     GitLab (`CI_JOB_TOKEN`), sauvegarde le rapport en artefact.
   - Stage `build` : génère le `.docx` via pandoc, artefact téléchargeable.
2. **`ci/find-cv.sh`** : détection automatique du CV à la racine (exclut
   README.md, CLAUDE.md, etc.). Erreur claire si 0 ou >1 fichiers trouvés.
3. **`ci/post-comment.sh`** : poste le rapport comme commentaire sur le commit
   via `curl` + API GitLab. Utilise `CI_JOB_TOKEN` (aucune config manuelle).
   Message d'aide si le post échoue (suggestion Project Access Token).

## Décisions prises

- **Deux CI coexistent** : `.github/workflows/check-cv.yml` (GitHub) et
  `.gitlab-ci.yml` (GitLab). Le projet fonctionne sur les deux plateformes.
- **Détection automatique du CV** plutôt qu'une variable `CV_PATH` en dur :
  l'étudiant n'a qu'à pousser son `.md` à la racine, pas de config à faire.
- **`CI_JOB_TOKEN`** par défaut (zéro config), avec fallback documenté vers
  un Project Access Token si les permissions sont insuffisantes.
- **Le check non bloquant pour le commentaire** : si le post échoue, le job
  continue et affiche un message d'aide. Le check lui-même reste bloquant.

## Vérifications passées en local

```
pytest                                       → 51 passed
python check_cv.py templates/cv-template.md  → 8/8, exit 0
```

## Limites connues

- **Le pipeline GitLab n'a pas encore tourné** : à tester au premier push sur
  le GitLab auto-hébergé. En particulier vérifier que `CI_JOB_TOKEN` a les
  permissions pour poster des commentaires sur les commits.
- **L'image `pandoc/core:latest`** dans le stage build doit être accessible
  depuis le GitLab auto-hébergé (registry Docker).

## Prochaines étapes

1. Pousser sur le GitLab auto-hébergé et vérifier le premier run du pipeline.
2. Si `CI_JOB_TOKEN` ne suffit pas pour les commentaires, documenter la
   création d'un Project Access Token.
3. Reprendre les TODOs existantes (TASK-001, TASK-002, etc.).

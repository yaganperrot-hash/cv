# TASK-001 — Mise en forme du .docx exporté

- **Statut** : à faire
- **Créée le** : 2026-08-26
- **Branche** : `feat/docx-reference`
- **Todo liée** : TODO-002

## Pourquoi

La conversion pandoc actuelle utilise le style Word par défaut : lisible et
parfaitement analysable par un ATS, mais fade. Un document de référence pandoc
(`--reference-doc`) permet de fixer polices, tailles et marges sans toucher au
Markdown, et sans casser la lisibilité machine.

## Périmètre

**Inclus**
- Un `templates/reference.docx` sobre : une seule colonne, pas de tableau de
  mise en page, pas de zone de texte, pas d'en-tête ni de pied de page
  (les ATS lisent mal tout cela).
- L'option `--reference-doc=templates/reference.docx` dans le workflow CI.
- L'exception `!templates/*.docx` du `.gitignore` est déjà en place.

**Exclus**
- Toute mise en page multi-colonnes ou graphique.
- Un export PDF (autre tâche si le besoin apparaît).

## Critères d'acceptation

- [ ] `pandoc templates/cv-template.md --reference-doc=templates/reference.docx
      -o dist/cv.docx` produit un document ouvrable sous Word et LibreOffice.
- [ ] Le texte extrait du `.docx` contient toujours les 8 champs vérifiés
      (contrôle : réextraire le texte et le repasser dans `check_cv.py`).
- [ ] La CI publie toujours l'artefact `cv-docx`.

## Notes techniques

`pandoc --print-default-data-file reference.docx > templates/reference.docx`
donne un point de départ à modifier dans Word.

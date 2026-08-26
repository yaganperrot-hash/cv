# Rapports de vérification

Ces rapports sont **générés**, mais versionnés à dessein : ils rendent lisible
en pull request ce que le vérificateur reproche (ou non) à chaque CV fictif du
dépôt, sans avoir à télécharger l'artefact de CI.

| Rapport | CV source | Attendu |
| --- | --- | --- |
| `cv-template-report.md` | `templates/cv-template.md` | 8/8 — conforme |
| `cv-partiel-report.md` | `tests/fixtures/cv-partiel.md` | 5/8 — les trois oublis fréquents |
| `cv-incomplet-report.md` | `tests/fixtures/cv-incomplet.md` | 1/8 — CV à peine commencé |

Régénération après toute modification de `config.yml`, du template ou d'une
fixture :

```bash
for cv in templates/cv-template.md tests/fixtures/*.md; do
  python check_cv.py "$cv" --no-color --quiet \
    --report "reports/$(basename "${cv%.md}")-report.md"
done
```

⚠️ **Jamais de rapport d'un CV réel ici** : il en contiendrait les coordonnées.
Les CV réels se vérifient depuis `data/`, dont les rapports restent locaux.

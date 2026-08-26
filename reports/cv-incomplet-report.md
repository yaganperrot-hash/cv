# Rapport de vérification du CV

- **Source** : `tests\fixtures\cv-incomplet.md`
- **Date** : 2026-08-26
- **Statut** : ❌ incomplet
- **Champs présents** : 1/8

| Champ | Statut | Détail |
| --- | --- | --- |
| Nom et prénom | ❌ manquant | titre trouvé (« camille ») mais format inattendu |
| Email | ❌ manquant | introuvable ou format invalide |
| Téléphone | ❌ manquant | introuvable ou format invalide |
| Section Formation | ❌ manquant | section « Formation » présente mais quasi vide (1 mot(s), minimum 8) |
| Section Expérience | ✅ présent | « Expérience » (ligne 9, 33 mots) |
| Section Compétences | ❌ manquant | section absente (titres acceptés : « competences », « competence », « competences techniques », « skills », « stack technique ») |
| Rythme d'alternance | ❌ manquant | mention(s) manquante(s) : 1 vendredi sur 3 à l'école, 33 h d'e-learning sur 3 semaines |
| Disponibilité | ❌ manquant | introuvable ou format invalide |

## À corriger

### Nom et prénom

- titre trouvé (« camille ») mais format inattendu
- **Aide** : Commence le CV par un titre de niveau 1 avec ton prénom ET ton nom, par exemple : `# Camille Dubois`.

### Email

- introuvable ou format invalide
- **Aide** : Ajoute une adresse email valide dans l'en-tête du CV (format attendu : prenom.nom@domaine.fr).

### Téléphone

- introuvable ou format invalide
- **Aide** : Ajoute un numéro de téléphone valide (formats acceptés : `06 12 34 56 78`, `+33 6 12 34 56 78`, `+44 7911 123456`, `+1 555 123 4567`).

### Section Formation

- section « Formation » présente mais quasi vide (1 mot(s), minimum 8)
- **Aide** : Ajoute une section `## Formation` listant tes diplômes et ton cursus en cours (intitulé, établissement, dates).

### Section Compétences

- section absente (titres acceptés : « competences », « competence », « competences techniques », « skills », « stack technique »)
- **Aide** : Ajoute une section `## Compétences` (langages, frameworks, outils, systèmes, langues).

### Rythme d'alternance

- mention(s) manquante(s) : 1 vendredi sur 3 à l'école, 33 h d'e-learning sur 3 semaines
- Manque : 1 vendredi sur 3 à l'école
- Manque : 33 h d'e-learning sur 3 semaines
- **Aide** : Précise le rythme d'alternance quelque part dans le CV (en-tête ou section `## Alternance`) : 3 semaines en entreprise, 1 vendredi sur 3 à l'école, 33 h d'e-learning sur 3 semaines.

### Disponibilité

- introuvable ou format invalide
- **Aide** : Indique ta disponibilité avec la formule attendue : « dès que possible » (par exemple : `**Disponibilité :** dès que possible`).

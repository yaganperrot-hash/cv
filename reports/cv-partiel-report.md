# Rapport de vérification du CV

- **Source** : `tests\fixtures\cv-partiel.md`
- **Date** : 2026-08-26
- **Statut** : ❌ incomplet
- **Champs présents** : 5/8

| Champ | Statut | Détail |
| --- | --- | --- |
| Nom et prénom | ✅ présent | Sofiane Bertrand |
| Email | ✅ présent | sofiane.bertrand@example.com |
| Téléphone | ❌ manquant | introuvable ou format invalide |
| Section Formation | ✅ présent | « Formation » (ligne 15, 30 mots) |
| Section Expérience | ✅ présent | « Expérience » (ligne 23, 52 mots) |
| Section Compétences | ✅ présent | « Compétences » (ligne 33, 18 mots) |
| Rythme d'alternance | ❌ manquant | mention(s) manquante(s) : 33 h d'e-learning sur 3 semaines |
| Disponibilité | ❌ manquant | introuvable ou format invalide |

## À corriger

### Téléphone

- introuvable ou format invalide
- **Aide** : Ajoute un numéro de téléphone valide (formats acceptés : `06 12 34 56 78`, `+33 6 12 34 56 78`, `+44 7911 123456`, `+1 555 123 4567`).

### Rythme d'alternance

- mention(s) manquante(s) : 33 h d'e-learning sur 3 semaines
- Manque : 33 h d'e-learning sur 3 semaines
- **Aide** : Précise le rythme d'alternance quelque part dans le CV (en-tête ou section `## Alternance`) : 3 semaines en entreprise, 1 vendredi sur 3 à l'école, 33 h d'e-learning sur 3 semaines.

### Disponibilité

- introuvable ou format invalide
- **Aide** : Indique ta disponibilité avec la formule attendue : « dès que possible » (par exemple : `**Disponibilité :** dès que possible`).

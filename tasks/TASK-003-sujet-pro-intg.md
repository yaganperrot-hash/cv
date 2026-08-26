# PRO-INTG / Cv — Sujet

> Rédigez votre CV professionnel en Markdown, poussez-le sur votre dépôt GitLab,
> et laissez la CI valider qu'il contient toutes les informations attendues.

---

## Modalités

| Type       | Description                                      |
| ---------- | ------------------------------------------------ |
| Dépôt      | `$RENDU$`                                        |
| Correction | Validation automatique (CI GitLab)               |
| Durée      | 14 jours                                         |
| Effectif   | Projet individuel                                |
| Outils     | Markdown / Git                                   |

---

## Objectifs

Ce projet vous apprendra à :

- **Rédiger un CV structuré** au format Markdown, versionnable et diffable.
- **Utiliser Git** dans un workflow professionnel (clone, commit, push).
- **Lire et comprendre un retour de CI** pour corriger vos erreurs en autonomie.

À la fin du module, vous aurez un CV Markdown à jour et vérifié — un outil
concret pour votre recherche d'alternance.

---

## Principe

Votre dépôt GitLab contient un **vérificateur automatique**. À chaque `git push`,
un pipeline CI :

1. **Détecte** votre fichier `.md` à la racine du dépôt.
2. **Vérifie** qu'il contient les 8 champs obligatoires (voir ci-dessous).
3. **Poste un commentaire** sur votre commit avec le rapport de vérification.

Votre travail : écrire le CV, pousser, lire le retour, corriger, repousser —
jusqu'à ce que le pipeline passe **au vert**.

Vous ne touchez pas au code du vérificateur, uniquement à votre fichier Markdown.

---

## Consignes

### 1. Cloner le dépôt et créer votre CV

```bash
git clone <url-de-votre-dépôt>
cd cv
```

Créez un fichier Markdown à la racine (par exemple `mon-cv.md`).
Ne touchez pas aux fichiers existants (`check_cv.py`, `config.yml`, etc.).

> **Important :** un seul fichier `.md` à la racine (hors `README.md` et
> `CLAUDE.md`). Si le vérificateur en trouve zéro ou plus d'un, il échouera.

### 2. Les 8 champs obligatoires

Votre CV doit contenir **tous** les éléments suivants. Le vérificateur les
cherche automatiquement — pas besoin de les nommer exactement, mais ils doivent
être présents et reconnaissables.

#### Nom et prénom

Un titre de niveau 1 (`#`) avec votre prénom et votre nom.

```markdown
# Prénom Nom
```

#### Email

Une adresse email valide, quelque part dans le CV.

```
prenom.nom@domaine.fr
```

#### Téléphone

Un numéro de téléphone français valide.

```
06 12 34 56 78
+33 6 12 34 56 78
```

#### Section Formation

Une section `## Formation` (ou un titre équivalent : `Études`, `Cursus`…)
contenant au moins 8 mots. Listez vos diplômes, établissements et dates.

#### Section Expérience

Une section `## Expérience` (ou : `Expériences professionnelles`, `Stages`…)
contenant au moins 8 mots. Listez vos stages, projets, jobs — avec le poste,
l'entreprise, les dates, et 2–3 réalisations concrètes.

#### Section Compétences

Une section `## Compétences` (ou : `Skills`, `Stack technique`…) contenant au
moins 5 mots. Langages, frameworks, outils, langues.

#### Rythme d'alternance

Le rythme d'alternance ETNA, mentionné quelque part dans le CV :

- **3 semaines en entreprise**
- **1 vendredi sur 3 à l'école**
- **33 h d'e-learning sur 3 semaines**

Les trois éléments doivent apparaître.

#### Disponibilité

La mention **« dès que possible »** quelque part dans le CV.

### 3. Pousser et vérifier

```bash
git add mon-cv.md
git commit -m "feat: premier jet du CV"
git push
```

Allez sur votre dépôt GitLab → **CI/CD → Pipelines** pour voir le résultat.
Un commentaire sera posté sur votre commit avec le détail des champs validés
et manquants.

### 4. Corriger et repousser

Si le pipeline est rouge, lisez le rapport : il indique précisément ce qui
manque et comment le corriger. Modifiez votre CV, committez, poussez à nouveau.

Répétez jusqu'au **pipeline vert** (8/8 champs validés).

---

## Structure recommandée

Voici un squelette de départ. Adaptez le contenu, mais gardez la structure :

```markdown
# Prénom Nom

**Votre titre — Bachelor Informatique (ETNA)**

- **Email :** prenom.nom@domaine.fr
- **Téléphone :** 06 12 34 56 78
- **Localisation :** Ville (département)

## Alternance

- **Rythme :** 3 semaines en entreprise, 1 vendredi sur 3 à l'école (ETNA),
  33 h d'e-learning sur 3 semaines.
- **Disponibilité :** dès que possible.

## Formation

**Bachelor Informatique — ETNA, Ivry-sur-Seine** — 2025 à 2027 (en cours)
Développement logiciel, algorithmique, bases de données.

## Expérience

**Stage — Poste, Entreprise (Ville)** — dates
- Réalisation 1.
- Réalisation 2.

## Compétences

- **Langages :** Python, JavaScript, etc.
- **Outils :** Git, VS Code, etc.
- **Langues :** français, anglais.
```

---

## Critères de validation

| # | Champ                  | Vérifié par la CI                                    |
|---|------------------------|------------------------------------------------------|
| 1 | Nom et prénom          | Titre `#` avec au moins deux mots                    |
| 2 | Email                  | Adresse email au format valide                       |
| 3 | Téléphone              | Numéro français (06/07/+33…)                         |
| 4 | Formation              | Section `##` présente, ≥ 8 mots                      |
| 5 | Expérience             | Section `##` présente, ≥ 8 mots                      |
| 6 | Compétences            | Section `##` présente, ≥ 5 mots                      |
| 7 | Rythme d'alternance    | 3 sous-champs présents (entreprise, école, e-learning)|
| 8 | Disponibilité          | Mention « dès que possible »                         |

**Le pipeline passe au vert quand les 8 champs sont validés.** C'est la seule
condition de validation du module.

---

## Ce que vous n'avez PAS à faire

- Toucher au code Python (`check_cv.py`, `cv_checker/`).
- Modifier `config.yml`.
- Installer quoi que ce soit en dehors de Git.
- Rédiger en HTML, PDF ou Word — uniquement du Markdown.

---

## Commandes utiles

```bash
# Vérifier votre CV en local avant de pousser
pip install pyyaml
python check_cv.py mon-cv.md

# Workflow Git classique
git add mon-cv.md
git commit -m "fix: ajoute la section Compétences"
git push
```

---

## FAQ

**Q : Mon pipeline est rouge mais mon CV a l'air complet, que faire ?**
Lisez le commentaire posté sur votre commit : il indique le champ manquant et
donne un conseil pour le corriger. Les erreurs les plus fréquentes : un titre
`#` sans espace après le `#`, un numéro de téléphone mal formaté, ou le rythme
d'alternance incomplet.

**Q : Je peux ajouter des sections en plus ?**
Oui. Le vérificateur ne vérifie que les 8 champs obligatoires. Vous pouvez
ajouter `## Projets`, `## Centres d'intérêt`, `## Langues`, etc.

**Q : Quel nom donner à mon fichier ?**
N'importe quel nom en `.md`, tant qu'il est à la racine et qu'il est le seul
(hors `README.md` et `CLAUDE.md`).

**Q : Mes données personnelles sont-elles visibles ?**
Votre CV est dans votre dépôt personnel. Il n'est pas partagé avec les autres
étudiants. Les enseignants y ont accès dans le cadre du module.

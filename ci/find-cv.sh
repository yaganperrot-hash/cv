#!/usr/bin/env bash
# Cherche le fichier CV Markdown a la racine du depot.
# Exclut les fichiers non-CV connus (README, CLAUDE, etc.).
# Sortie : le chemin du CV trouve sur stdout.
# Code 1 si aucun CV ou plusieurs CVs trouves.

set -euo pipefail

EXCLUDE_PATTERN="^(README|CLAUDE|CONTRIBUTING|CHANGELOG|LICENSE)\.md$"

candidates=()
for f in *.md; do
  [ -f "$f" ] || continue
  if echo "$f" | grep -qEi "$EXCLUDE_PATTERN"; then
    continue
  fi
  candidates+=("$f")
done

if [ ${#candidates[@]} -eq 0 ]; then
  echo "Erreur : aucun fichier CV (.md) trouve a la racine du depot." >&2
  echo "Placez votre CV en Markdown a la racine (ex: mon-cv.md)." >&2
  exit 1
fi

if [ ${#candidates[@]} -gt 1 ]; then
  echo "Erreur : plusieurs fichiers .md trouves a la racine :" >&2
  printf "  - %s\n" "${candidates[@]}" >&2
  echo "Gardez un seul fichier CV .md a la racine du depot." >&2
  exit 1
fi

echo "${candidates[0]}"

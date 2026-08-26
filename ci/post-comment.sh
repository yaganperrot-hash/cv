#!/usr/bin/env bash
# Poste le rapport de verification comme commentaire sur le commit GitLab.
# Usage : ci/post-comment.sh <fichier-rapport>
#
# Variables d'environnement attendues (fournies par GitLab CI) :
#   CI_API_V4_URL, CI_PROJECT_ID, CI_COMMIT_SHA, CI_JOB_TOKEN

set -euo pipefail

REPORT_FILE="${1:?Usage: $0 <fichier-rapport>}"

if [ ! -f "$REPORT_FILE" ]; then
  echo "Erreur : rapport introuvable : $REPORT_FILE" >&2
  exit 1
fi

for var in CI_API_V4_URL CI_PROJECT_ID CI_COMMIT_SHA CI_JOB_TOKEN; do
  if [ -z "${!var:-}" ]; then
    echo "Erreur : variable $var non definie. Ce script doit tourner dans GitLab CI." >&2
    exit 1
  fi
done

BODY=$(cat "$REPORT_FILE")

# L'API GitLab attend le commentaire dans le champ "note" en JSON.
PAYLOAD=$(python3 -c "
import json, sys
body = sys.stdin.read()
print(json.dumps({'note': body}))
" <<< "$BODY")

HTTP_CODE=$(curl --silent --output /dev/stderr --write-out "%{http_code}" \
  --request POST \
  --header "JOB-TOKEN: $CI_JOB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "$PAYLOAD" \
  "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/repository/commits/${CI_COMMIT_SHA}/comments")

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "Commentaire poste sur le commit $CI_COMMIT_SHA (HTTP $HTTP_CODE)."
else
  echo "Attention : impossible de poster le commentaire (HTTP $HTTP_CODE)." >&2
  echo "Si le probleme persiste, creez un Project Access Token avec le scope 'api'" >&2
  echo "dans Settings > Access Tokens et ajoutez-le comme variable CI GITLAB_TOKEN." >&2
  exit 1
fi

#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Kullanim: ./scripts/local-deploy.sh DOCKERHUB_USERNAME"
  echo "Ornek: ./scripts/local-deploy.sh gizemakkaya"
  exit 1
fi

DOCKER_USER="$1"

ansible-playbook \
  -i ansible/inventory.ini \
  ansible/deploy.yml \
  --extra-vars "docker_user=${DOCKER_USER}" \
  --ask-become-pass

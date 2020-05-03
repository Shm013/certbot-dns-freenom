#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

Login() {
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
}

Push() {
    DOCKER_REPO="$1"
    PLUGIN_VERSION="$2"
    bash hooks/push
    bash hooks/post_push
}

WORK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

CERTBOT_VERSION="$1"
PLUGIN_VERSION="$2"

Login
Push "shm013/certbot-dns-freenom" "$CERTBOT_VERSION" "$PLUGIN_VERSION"

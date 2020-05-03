#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

Login() {
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
}

Push() {
    DOCKER_REPO="$1"
    PLUGIN_VERSION="$2"
    DOCKER_REPO=$DOCKER_REPO PLUGIN_VERSION=$PLUGIN_VERSION bash hooks/push
    DOCKER_REPO=$DOCKER_REPO PLUGIN_VERSION=$PLUGIN_VERSION bash hooks/post_push
}

WORK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

PLUGIN_VERSION="$1"

Login
Push "shm013/certbot-dns-freenom" "$PLUGIN_VERSION"

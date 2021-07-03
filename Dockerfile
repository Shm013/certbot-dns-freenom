# Docker Arch (amd64, arm32v6, ...)
ARG ARCH
ARG CERTBOT_VERSION
FROM certbot/certbot:${ARCH}-v${CERTBOT_VERSION}

# Copy Certbot DNS plugin code
COPY . /opt/certbot/src/plugin

# Build tools
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev libxml2 libxslt

# Install the DNS plugin
RUN python tools/pip_install.py --no-cache-dir --editable /opt/certbot/src/plugin

# Cleanup
RUN apk del g++ gcc libxml2-dev libxslt-dev

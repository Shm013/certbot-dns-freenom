# Docker Arch (amd64, arm32v6, ...)
ARG TARGET_ARCH
ARG CERTBOT_VERSION
FROM certbot/certbot:${TARGET_ARCH}-v${CERTBOT_VERSION}

ARG PLUGIN_NAME
ARG PLUGIN_VERSION

# Build tools
RUN apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev libxml2 libxslt

# Retrieve Certbot DNS plugin code
RUN wget -O ${PLUGIN_NAME}-${PLUGIN_VERSION}.tar.gz https://github.com/shm013/${PLUGIN_NAME}/archive/v${PLUGIN_VERSION}.tar.gz \
 && tar xf ${PLUGIN_NAME}-${PLUGIN_VERSION}.tar.gz \
 && cp -r ${PLUGIN_NAME}-${PLUGIN_VERSION} /opt/certbot/src/${PLUGIN_NAME} \
 && rm -rf ${PLUGIN_NAME}-${PLUGIN_VERSION}.tar.gz ${PLUGIN_NAME}-${PLUGIN_VERSION}

# Install the DNS plugin
RUN pip install --constraint /opt/certbot/docker_constraints.txt --no-cache-dir --editable /opt/certbot/src/${PLUGIN_NAME}

# Cleanup
RUN apk del g++ gcc libxml2-dev libxslt-dev

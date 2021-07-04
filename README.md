![PyPI version](https://badge.fury.io/py/certbot-dns-freenom.svg)
![ci](https://github.com/shm013/certbot-dns-freenom/actions/workflows/ci.yml/badge.svg)
![dockerhub](https://github.com/shm013/certbot-dns-freenom/actions/workflows/dockerhub.yml/badge.svg)

freenom DNS Authenticator plugin for Certbot
==============================================
A certbot dns plugin to obtain certificates using Freenom DNS.

# Credentials File

credentials.ini
```ini
certbot_dns_freenom:dns_freenom_username = username
certbot_dns_freenom:dns_freenom_password = password
```

```bash
chmod 600 /path/to/credentials.ini
```

# Obtaining certificate

This are examples to obtain wildcard certificate.
Change domain, email and path/to/credential.ini file to your owns.

## Using pip

```
pip install certbot certbot-dns-freenom
```

```bash
certbot certonly -a certbot-dns-freenom:dns-freenom \
  --certbot-dns-freenom:dns-freenom-credentials /path/to/credentials.ini \
  --certbot-dns-freenom:dns-freenom-propagation-seconds 300 \
  -d "*.example.com" \
  -m admin@example.com \
  --agree-tos -n
```

## Using docker

```bash
docker run \
    -v /path/to/credentials.ini:/credentials.ini \
    -v /etc/letsencrypt:/etc/letsencrypt \
    -v /var/lib/letsencrypt:/var/lib/letsencrypt \
    -v /var/log/letsencrypt:/var/log/letsencrypt \
    shm013/certbot-dns-freenom:latest \
    certonly \
    -a certbot-dns-freenom:dns-freenom \
    --certbot-dns-freenom:dns-freenom-credentials /credentials.ini \
    --certbot-dns-freenom:dns-freenom-propagation-seconds 300 \
    -d '*.example.com' \
    -m 'admin@example.com' \
    --agree-tos -n"
```

# Possible problems

It take up to 30 minutes to update dns record.
You can rise parameter `certbot-dns-freenom:dns-freenom-propagation-seconds` if cause any trouble such as:

```
IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: youdomain.com
   Type:   dns
   Detail: DNS problem: NXDOMAIN looking up TXT for
   _acme-challenge.youdomain.com - check that a DNS record exists for this
   domain
```

[![Build Status](https://travis-ci.com/Shm013/certbot-dns-freenom.svg?branch=master)](https://travis-ci.com/Shm013/certbot-dns-freenom)

freenom DNS Authenticator plugin for Certbot
==============================================
A certbot dns plugin to obtain certificates using Freenom DNS.

## Install

pip install certbot-dns-freenom

## Credentials File

```
certbot_dns_freenom:dns_freenom_username = username
certbot_dns_freenom:dns_freenom_password = password
```

```bash
chmod 600 /path/to/credentials.ini
```

## Obtain Certificates

```bash
certbot certonly -a certbot-dns-freenom:dns-freenom \
  --certbot-dns-freenom:dns-freenom-credentials /path/to/credentials.ini \
  --certbot-dns-freenom:dns-freenom-propagation-seconds 300 \
  -d example.com \
  -d "*.example.com" \
  -m admin@example.com \
  --agree-tos -n
```

It take up to 30 minutes minut to update dns record.
You can rise parameter `certbot-dns-freenom:dns-freenom-propagation-seconds` if cause any trouble such as
```
IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: youdomain.com
   Type:   dns
   Detail: DNS problem: NXDOMAIN looking up TXT for
   _acme-challenge.youdomain.com - check that a DNS record exists for this
   domain
```

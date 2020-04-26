#   Copyright 2019 Nikolay Shamanovich shm013@yandex.ru
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
The `~certbot_dns_freenom.dns_freenom` plugin automates the process of completing
a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the freenom DNS API.


Named Arguments
---------------

=======================================================  =====================
``--certbot-dns-freenom:dns-freenom-credentials``        freenom credentials_
                                                         INI file.  (Required)
-------------------------------------------------------  ---------------------
``--certbot-dns-freenom:dns-freenom-propagation-         wait before perform
seconds``                                                challenge (sec)
=======================================================  =====================


Credentials
-----------

Use of this plugin requires a configuration file containing
freenom DNS API credentials, username and password

.. code-block:: ini
   :name: credentials.ini
   :caption: Example credentials file:

   # freenom API credentials used by Certbot
   certbot_dns_freenom:dns_freenom_username = username
   certbot_dns_freenom:dns_freenom_password = password

The path to this file can be provided interactively or using the
``--certbot-dns-freenom:dns-freenom-credentials`` command-line argument.
Certbot records the path to this file for use during renewal, but does not
store the file's contents.

.. caution::
   You should protect these API credentials as you would the password to your
   freenom account. Users who can read this file can take full acces of you
   freenon accaunt. Users who can cause Certbot to run using these credentials
   can complete a ``dns-01`` challenge to acquire new certificates or revoke
   existing certificates for associated domains, even if those domains aren't
   being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``

   certbot certonly -a certbot-dns-freenom:dns-freenom \\
     --certbot-dns-freenom:dns-freenom-credentials /path/to/credentials.ini \\
     --certbot-dns-freenom:dns-freenom-propagation-seconds 300 \\
     -d "*.example.com" \\
     -m admin@example.com \\
     --agree-tos -n

"""

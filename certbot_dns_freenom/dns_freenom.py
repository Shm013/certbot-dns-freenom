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

"""DNS Authenticator for Freenom DNS."""
import zope.interface
from freenom import Freenom

from certbot import interfaces
from certbot.plugins import dns_common

ACCOUNT_KEYS_URL = "https://my.Freenom.ru/profile/apikeys"


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Freenom DNS

    This Authenticator uses the Freenom DNS API to fulfill a dns-01 challenge.
    """

    description = (
        "Obtain certificates using a DNS TXT record (if you are using Freenom for "
        "DNS)."
    )

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.ttl = 300

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add("credentials", help="Freenom DNS API credentials file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return "This plugin configures a DNS TXT record to respond to a \
                dns-01 challenge using the Freenom DNS API."

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Freenom DNS credentials file",
            {
                "username": "Your username for Freenom",
                "password": "Your password for Freenom",
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_freenom_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_freenom_client().del_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _get_freenom_client(self):
        return _FreenomDNSClient(
            self.credentials.conf("username"), self.credentials.conf("password")
        )


class _FreenomDNSClient():
    """
    Encapsulates all communication with the Freenom API.
    """

    def __init__(self, username, password):
        self.freenom = Freenom(username, password)

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        """ Add txt record """
        if domain.count('.') > 1:
            print ("Subdomain is used")
            domain_list=domain.split('.')
            domain = ".".join(domain_list[-2:])
        print ("Add record: ",domain, record_name,record_content)
        self.freenom.setRecord(domain, record_name, 'TXT', record_content, record_ttl)

    def del_txt_record(self, domain, record_name, record_content, record_ttl):
        """ Delete txt record """
        if domain.count('.') > 1:
            domain_list=domain.split('.')
            domain = ".".join(domain_list[-2:])
        print ("Delete record: ",domain, record_name,record_content)
        self.freenom.delRecord(domain, record_name, 'TXT', record_content, record_ttl)

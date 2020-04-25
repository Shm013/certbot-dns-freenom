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
import logging

from freenom import Freenom

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

ACCOUNT_KEYS_URL = 'https://my.Freenom.ru/profile/apikeys'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Freenom DNS

    This Authenticator uses the Freenom DNS API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using Freenom for '
                   'DNS).')
    ttl = 120

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Freenom DNS API credentials file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Freenom DNS API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Freenom DNS credentials file',
            {
                'username': 'Your username for Freenom',
                'password': 'Your password for Freenom'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_Freenom_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        self._get_Freenom_client().del_txt_record(domain, validation_name, validation)

    def _get_Freenom_client(self):
        return  _FreenomDNSClient(self.credentials.conf('username'), self.credentials.conf('password'))

class NoRecordError(Exception):
    pass

class NoDomainZoneError(Exception):
    pass

class _FreenomDNSClient(object):
    """
    Encapsulates all communication with the Freenom API.
    """

    def __init__(self, username, password):
        self.freenom = Freenom(username, password)

    def add_txt_record(self, domain, record_name, record_content, record_ttl):

        body = Freenom_dns_api.NewOrUpdatedRecord(
            name = record_name,
            type = 'TXT',
            ttl = record_ttl,
            content = record_content
        )

        try:
            # Create resource records for domain
            api_response = self.records.add_resource_record(body, domain_id)
            self.freenom.setRecord('your domain', record_name, 'TXT', record_content)
        except ApiException as e:
            print("Exception when calling RecordsApi->add_resource_record: %s\n" % e)

    def del_txt_record(self, domain, record_name, record_content):

        try:
            # Deletes a resource record
            self.freenom.delRecord('your domain', record_name)
        except ApiException as e:
            print("Exception when calling RecordsApi->delete_resource_record: %s\n" % e)


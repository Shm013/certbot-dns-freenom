import sys
import pathlib
import os

sys.path.append(str(pathlib.Path().absolute()))
import certbot_dns_freenom.dns_freenom as certbot_dns_freenom

def test_perform():
    assert os.environ["FREENOM_USERNAME"]
    assert os.environ["FREENOM_PASSWORD"]
    assert os.environ["FREENOM_DOMAIN"]

    username = os.environ["FREENOM_USERNAME"]
    password = os.environ["FREENOM_PASSWORD"]
    domain   = os.environ["FREENOM_DOMAIN"]

    print(domain)

    authenticator = certbot_dns_freenom._FreenomDNSClient(username, password)
    authenticator.add_txt_record(domain, "_TEST", "_TARGET", 300)

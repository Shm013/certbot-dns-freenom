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
    domain = os.environ["FREENOM_DOMAIN"]

    record_target = "eaa7c9c1ca414552b504d1d6ddcd7715775ed507f8f136391c37846206b7df4d"
    record_name = "_TEST_CERTBOT"

    test_record = "{}.{}".format(record_name, domain)

    authenticator = certbot_dns_freenom._FreenomDNSClient(username, password)

    # Empty record
    authenticator.del_txt_record(domain, record_name, record_target, 300)

    nslookup_output = os.popen("nslookup -type=TXT {}".format(test_record)).read()
    print(nslookup_output)

    assert not record_target in nslookup_output

    # Add new record
    authenticator.add_txt_record(domain, record_name, record_target, 300)

    nslookup_output = os.popen("nslookup -type=TXT {}".format(test_record)).read()
    print(nslookup_output)

    assert record_target in nslookup_output

    # Clenup
    #authenticator.del_txt_record(domain, record_name, record_target, 300)

    #nslookup_output = os.popen("nslookup -type=TXT {}".format(test_record)).read()
    #print(nslookup_output)

    #assert not record_target in nslookup_output

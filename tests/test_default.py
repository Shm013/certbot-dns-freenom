import sys
import pathlib
import time
import os

sys.path.append(str(pathlib.Path().absolute()))
import certbot_dns_freenom.dns_freenom as certbot_dns_freenom


def test_FreenomDNSClient():
    assert os.environ["FREENOM_USERNAME"]
    assert os.environ["FREENOM_PASSWORD"]
    assert os.environ["FREENOM_DOMAIN"]

    username = os.environ["FREENOM_USERNAME"]
    password = os.environ["FREENOM_PASSWORD"]
    domain = os.environ["FREENOM_DOMAIN"]

    record_target = "eaa7c9c1ca414552b504d1d6ddcd7715775ed507f8f136391c37846206b7df4d"
    freenom_dns = "80.80.80.80"

    # Generate unique record
    record_name = "_TEST_CERTBOT_{}".format(os.environ["RECORD_ID"])
    test_record = "{}.{}".format(record_name, domain)

    # Login into Freenom
    authenticator = certbot_dns_freenom._FreenomDNSClient(username, password)

    # Empty record
    nslookup_output = os.popen(
        "nslookup -type=TXT {} - {}".format(test_record, freenom_dns)
    ).read()
    assert not record_target in nslookup_output

    # Add new record
    authenticator.add_txt_record(domain, record_name, record_target, 300)
    time.sleep(600)
    nslookup_output = os.popen(
        "nslookup -type=TXT {} - {}".format(test_record, freenom_dns)
    ).read()
    assert record_target in nslookup_output

    # Clenup
    authenticator.del_txt_record(domain, record_name, record_target, 300)
    time.sleep(600)
    nslookup_output = os.popen(
        "nslookup -type=TXT {} - {}".format(test_record, freenom_dns)
    ).read()
    assert not record_target in nslookup_output

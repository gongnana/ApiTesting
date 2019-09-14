import logging
import requests
import pytest
import json


class TestRequests(object):
    logging.basicConfig(level=logging.INFO)

    def test_get(self):
        r = requests.get('https://testerhome.com/api/v3/topics.json')
        logging.info(r)
        logging.info(r.text)
        logging.info(json.dumps(r.json(), indent=2))




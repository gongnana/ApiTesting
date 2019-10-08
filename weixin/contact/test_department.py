from weixin.contact.token import Weixin
import requests
import logging
import json
import pytest


class TestDepartment:
    @classmethod
    def setup_class(cls):
        print('\nsetup_class')
        Weixin.get_token()
        print(Weixin._token)

    def setup(self):
        print('setup...')

    def test_create_depth(self):
        parentid = 1
        for i in range(5):
            data = {
                "name": "广州研发中心分部_" + str(parentid),
                "parentid": parentid,
                "order": 1,
            }
            r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/department/create',
                          params={'access_token': Weixin.get_token()}, json=data).json()
            logging.debug(r)
            parentid = r['id']

    @pytest.mark.parametrize('name',
                             ['東京アニメーション研究所',
                              '도쿄 애니메이션 인스티튜트',
                              '東京動漫研究所'
                              'معهد طوكيو للرسوم المتحركة'])
    def test_create_order(self, name):
        data = {
            "name": name,
            "parentid": 1,
            "order": 1,
        }
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/department/create',
                          params={'access_token': Weixin.get_token()}, json=data).json()
        logging.debug(r)

    def test_get(self):
        r = requests.get('https://qyapi.weixin.qq.com/cgi-bin/department/list',
                         params={'access_token': Weixin.get_token()}).json()
        logging.debug(json.dumps(r, indent=2))

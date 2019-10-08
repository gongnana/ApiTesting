import logging
import time
import json

import pystache
import requests

from weixin.contact.token import Weixin


class TestUser:
    depart_id = 1
    @classmethod
    def setup_class(cls):
        # todo: create department
        pass

    def test_create(self):
        uid = str(time.time())
        data = {'userid': uid,
                'name': uid,
                'department': [self.depart_id],
                'email': uid + '@163.com'}
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/user/create',
                          params={'access_token': Weixin.get_token()}, json=data
                          ).json()
        logging.debug(json.dumps(r, indent=2))
        assert r['errcode'] == 0

    def test_list(self):
        params = {'access_token': Weixin.get_token(),
                  'department_id': 1,
                  'fetch_child': 0}
        r = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/simplelist',
                         params=params)
        logging.debug(json.dumps(r.json(), indent=2))

    def test_create_by_template(self):
        uid = 'eunice_' + str(time.time())
        mobile = str(time.time()).replace('.', '')[0:11]
        data = str(self.get_user({'name': uid,
                                  'title': '项目经理',
                                  'email': 'test@163.com',
                                  'mobile': mobile,
                                  'uid': uid}))
        data = data.encode('UTF-8')
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/user/create',
                          params={'access_token': Weixin.get_token()},
                          data=data,
                          headers={'content-type': 'application/json; charset=UTF-8'},
                          ).json()
        logging.debug(r)
        assert r['errcode'] == 0

    def get_user(self, dic):
        template = ''.join(open('create_user.json').readlines())
        logging.debug(template)
        return pystache.render(template, dic)

    def test_get_user(self):
        logging.debug(self.get_user({'name': 'welcome', 'title': '项目经理', 'email': 'test@163.com'}))

import logging
import time
import json
import requests

from weixin.contact.token import Weixin
from weixin.contact.user import User
from weixin.contact.utils import Utils


class TestUser:
    depart_id = 1
    @classmethod
    def setup_class(cls):
        # todo: create department
        cls.user = User()

    def test_create(self):
        uid = str(time.time())
        data = {'userid': uid,
                'name': uid,
                'department': [self.depart_id],
                'email': uid + '@163.com'}
        r = self.user.create_user(data)
        logging.debug(json.dumps(r, indent=2))
        assert r['errcode'] == 0

    def test_list(self):
        r = self.user.get_list()
        logging.debug(json.dumps(r, indent=2))

    def test_create_by_template(self):
        uid = 'eunice_' + str(time.time())
        mobile = str(time.time()).replace('.', '')[0:11]
        data = str(Utils.template_parse('create_user.json', {'name': uid,
                                                             'title': '项目经理',
                                                             'email': mobile+'@163.com',
                                                             'mobile': mobile,
                                                             'uid': uid}))
        data = data.encode('UTF-8')
        r = self.user.create_user(data=data)
        logging.debug(r)
        assert r['errcode'] == 0

    def test_get_user(self):
        logging.debug(Utils.template_parse('create_user.json',
                                           {'name': 'welcome', 'title': '项目经理', 'email': 'test@163.com'}))


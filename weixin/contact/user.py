import requests

from weixin.contact.token import Weixin


class User:

    def create_user(self, dic=None, data=None):
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/user/create',
                          params={'access_token': Weixin.get_token()},
                          json=dic,
                          data=data).json()
        return r

    def get_list(self, department_id=1, fetch_child=0, **kwargs):
        params = {'access_token': Weixin.get_token(),
                  'department_id': department_id,
                  'fetch_child': fetch_child}
        r = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/simplelist',
                         params=params).json()
        return r

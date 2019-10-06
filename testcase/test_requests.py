import logging
import requests
import pytest
import json
import jsonpath
from hamcrest import *
from jsonschema import validate


class TestRequests(object):
    logging.basicConfig(level=logging.INFO)
    url = "https://testerhome.com/api/v3/topics.json"

    def test_get(self):
        r = requests.get(self.url)
        logging.info(r)
        logging.info(r.text)
        logging.info(json.dumps(r.json(), indent=2))

    def test_post(self):
        r = requests.get(self.url,
                         params={"a": 1, "b": "string content"},
                         headers={"a": "1", "b": "2"},
                         proxies={"https": "http://127.0.0.1:8888"},
                         verify=False)
        logging.info(r.url)
        logging.info(r.text)
        logging.info(json.dumps(r.json(), indent=2))

    def test_cookies(self):
        r = requests.get("http://47.95.238.18:8090/cookies", cookies={"a": "111", "b": "222"})
        logging.info(r.text)

    def test_xueqiu(self):
        query = {"_t": "1UNKNOWNc60715cb4a61425b311034a49f4aa024.3446260779.1563002521424.1563005246620",
                 "_s": "8c6b2d",
                 "category": "1",
                 "pid": "-1",
                 "size": "10000",
                 "x": "1.3",
                 "page": "1"}
        cookies = {"xq_a_token": "5806a70c6bc5d5fb2b00978aeb1895532fffe502",
                   "u": "3446260779"}
        header = {"User-Agent": "Xueqiu Android 11.19",
                  "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4"}

        r = requests.get(url="https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json",
                         params=query, headers=header, cookies=cookies)
        logging.info(r.text)

    def test_xueqiu1(self):
        query = {'_t': '1UNKNOWNc60715cb4a61425b311034a49f4aa024.3446260779.1563002521424.1563005246620',
                 '_s': '8c6b2d',
                 'category': '1',
                 'pid': '-1',
                 'size': '10000',
                 'x': '1.3',
                 'page': '1'}

        r = requests.get('https://101.201.175.228/v5/stock/portfolio/stock/list.json',
                         params=query,
                         headers={'Host': 'stock.xueqiu.com',
                                  'User-Agent': 'Xueqiu Android 11.19'},
                         cookies={'xq_a_token': '9c3e6344848ecd7395bd629b6f8fdb4307ea940d',
                                  'u': '3446260779'}
                         )
        logging.info(json.dumps(r.json(), indent=2))

    def test_fund(self):
        query = {'type': '1002',
                 'order_by': '1m',
                 'size': '20',
                 'page': '1'}
        header = {'Host': 'danjuanapp.com',
                     'Pragma': 'no - cache',
                     'Cache - Control': 'no - cache',
                     'Accept': 'application/json, text/plain, */*',
                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                     'Sec-Fetch-Mode': 'cors',
                     'Sec - Fetch - Site': 'same - origin',
                     'Referer': 'https: // danjuanapp.com / rank / index',
                     'Accept-Encoding': 'gzip, deflate, br, utf-8',
                     'Accept-Language': 'zh-CN,zh;q=0.9'}
        cookies = {'xq_a_token': '9c3e6344848ecd7395bd629b6f8fdb4307ea940d'}
        r = requests.get('https://danjuanapp.com/djapi/v3/filter/fund', params=query,
                         headers=header,
                         cookies=cookies, proxies={'https': '101.132.168.235:8080'})
        logging.info(json.dumps(r.json(), indent=2))
        assert r.json()['data']['items'][0]['fd_code'] == '160420'
        assert r.json()['data']['items'][0]['fd_name'] == '华安创业板50指数'
        logging.info(jsonpath.jsonpath(r.json(), '$.data.items[6].[fd_name]'))
        assert jsonpath.jsonpath(r.json(),
                                        '$.data.items[?(@.fd_code=="160720")]'
                                        '.fd_name')[0] == '嘉实中证中期企业债指数A'
        assert_that(jsonpath.jsonpath(r.json(), '$.data.items[?(@.fd_code=="090010")].fd_name')[0], equal_to('大成中证红利指数A'))

    def test_hamcrest(self):
        assert_that(0.1 * 0.01, close_to(0.001, 10))
        assert_that([0, 'a', 1, 'b'], has_item('a'))
        assert_that(['a', 'b', 'c'], any_of(has_items(2, 'a', 7), has_items('b')))

    def test_schema(self):
        schema = {
            'type': 'object',
            'properties': {
                'price': {'type': 'number'},
                'name': {'type': 'string'},
            },
        }

        validate(instance={'name': 'Eggs', 'price': '34.99'}, schema=schema)

    def test_list_schema(self):
        session = requests.Session()
        session.headers = {'User - Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ' 
                                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                           }
        session.get('https://xueqiu.com/')

        query = {'size': 8,
                 '_type': 11,
                 'type': 11}
        # header = {
        #              'Accept': 'application / json, text / plain, * / *',
        #              'Origin': 'https: // xueqiu.com',
        #              'Referer': 'https: // xueqiu.com /',
        #              'Sec - Fetch - Mode': 'cors',
        #              'User - Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
        #                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        # }
        r = session.get('https://stock.xueqiu.com/v5/stock/hot_stock/list.json', headers=session.headers, params=query,
                         proxies={'http:': '222.66.94.130:80'}, verify=False)
        print(type(json.dumps(r.json())))

        logging.info(json.dumps(r.json(), indent=2))
        print('*' * 50)
        schema = json.load(open('list_schema.json'))
        validate(instance=json.dumps(r.json()), schema=schema)








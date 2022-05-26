#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
os.environ["EXECJS_RUNTIME"] = "Node"
os.environ["NODE_PATH"] = os.getcwd()+"\\node_modules"
import requests
import json
from bs4 import BeautifulSoup
import hashlib
import execjs
import logging


logging.basicConfig(level=logging.DEBUG,
                    filename="log.log",
                    filemode="w",
                    format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                    )

config_path = './my_info.json'
try:
    logging.debug("config path: {}".format(config_path))
    with open(config_path, 'r', encoding='utf8') as fp:
        headers = json.load(fp)
except Exception as e:
    logging.exception(e)

search_str = 'python'
url = '/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal'.format(search_str)
code_head = '{}+{}'.format(headers["x-zse-93"], url)
code = "+".join([code_head, headers['d_c0']])
fmd5 = hashlib.new('md5', code.encode()).hexdigest()
with open('encode.js', 'r', encoding="utf-8") as f:
    ctx1 = execjs.compile(f.read())
encrypt_str = ctx1.call('b', fmd5)
logging.debug("code to conduct md5: {}".format(code))
logging.debug("md5: {}".format(fmd5))
logging.debug("encrypt str: {}".format(encrypt_str))
s = requests.Session()
headers["x-zse-96"] = "2.0_{}".format(encrypt_str)
res=s.get("https://www.zhihu.com{}".format(url), headers=headers)

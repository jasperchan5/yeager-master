import requests as rq
from pyquery import PyQuery as pq

baseHeader = {
    # 'Host': 'www.pixiv.net'
    'Connection': 'keep-alive',
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://accounts.pixiv.net/login',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}
name = "B09705026@ntu.edu.tw"
password = "Db168245"

def login():
    global name, password
    url = "https://accounts.pixiv.net/api/login?lang=zh"
    session = set_PHPSESSID()
    post_key = get_post_key(session)
    data = {
        "pixiv_id": name,
        "password": password,
        "post_key": post_key,
        "source": "pc",
        "ref": "wwwtop_accounts_index",
    }
    session.post(url, data, headers=baseHeader)
    return session

def get_post_key(s):
    # """
    # 反爬措施：登录需要post_key参数
    # """
    url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
    data = {"lang": "zh",
            "source": "pc",
            "view_type": "page",
            "ref": "wwwtop_accounts_index"
            }
    page = s.get(url=url, data=data,headers=baseHeader).content
    doc = pq(page)
    post_key = doc('[name="post_key"]')[0].value
    return post_key

def set_PHPSESSID():
    # """
    # 反爬措施，访问页面获得phpsessid的cookie值
    # """
    s = rq.session()
    url = "https://www.pixiv.net/"
    s.get(headers=baseHeader, url=url)
    return s
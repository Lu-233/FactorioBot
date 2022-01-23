"""
    bili wiki bot

    thanks https://github.com/YorkSu/bwt
"""

import os
import json
import sqlite3
import warnings
from pathlib import Path

import requests
from base64 import b64decode
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    session = login_bili_wiki()


def login_bili_wiki(browser_name="Edge", wiki_name="factorio"):
    """
        get bili wiki session
        browser_name:  Edge or Chrome
        wiki_name: like "factorio","name"
    """

    print("You are trying use bili wiki support")
    print("you need first login to bilibili in browser, and access wiki page")
    print("then, this code will load your cookies to get session")

    url = f"https://wiki.biligame.com/{wiki_name}/api.php"

    session = requests.Session()
    session.cookies.update(_get_cookies(".biligame.com", "/", browser_name))
    session.cookies.update(_get_cookies("wiki.biligame.com", f"/{wiki_name}/", browser_name))

    response = session.get(url=url, params={
        "action": "query",
        "meta": "tokens",
        "format": "json",
    }).json()

    token = response["query"]["tokens"]["csrftoken"]

    # check login is valid
    response = session.post(url=url, data={
        "action": "checktoken",
        "type": "csrf",
        "token": token,
        "format": "json",
    }).json()

    if not response["checktoken"]["result"] == "valid":
        raise Exception("登录状态错误,请从浏览器打开一次wiki页面后再试, response=", response)
    else:
        print("login checked success.")

    return session


# noinspection SqlResolve
def _get_cookies(host: str, path: str, browser: str):
    """ get cookies from browser local file"""

    _local_appdata = os.environ['LOCALAPPDATA']
    if browser.lower() == 'edge':
        local_state = _local_appdata + r'\Microsoft\Edge\User Data\Local State'
        cookie_path = _local_appdata + r'\Microsoft\Edge\User Data\Default\Cookies'
    elif browser.lower() == 'chrome':
        local_state = _local_appdata + r'\Google\Chrome\User Data\Local State'
        cookie_path = _local_appdata + r'\Google\Chrome\User Data\Default\Cookies'
    else:
        raise KeyError("不支持的浏览器，目前只支持 edge and chrome。")

    with sqlite3.connect(cookie_path) as conn:
        cursor = conn.cursor()
        sql = f"select name,encrypted_value from cookies where host_key=? and path=?"
        data = cursor.execute(sql, [host, path]).fetchall()
        cursor.close()

    decoder = AESGCM(_get_key(local_state))
    cookies = {}
    for name, data in data:
        if data[0:3] != b'v10':  # data is bytes
            warnings.warn(f"encrypted_value 应以v10开头，实际是{data[0:3]}，这可能让Cookie解析失败，登录失败。")

        data = decoder.decrypt(data[3:15], data[15:], None)
        cookies[name] = data.decode("UTF8")

    return cookies


def _get_key(local_state):
    state_data = Path(local_state).read_text("UTF8")
    key = json.loads(state_data)['os_crypt']['encrypted_key']
    key = CryptUnprotectData(b64decode(key)[5:])[1]
    return key

if __name__ == '__main__':
    main()  # for test
""" for wiki.factorio.com """
import io
import json
from pathlib import Path

import requests

from tool.cfg import load_cfg

api_url = 'https://wiki.factorio.com/api.php'


def main():
    """ main func """
    print("hello factorio\n")


def get_all_pages(session=None, apnamespace=0, one_req_limit=500):
    if session is None:
        session = login()
    data = []
    req = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'assert': 'user',
        'list': 'allpages',
        'apnamespace': apnamespace,
        'aplimit': one_req_limit
    })

    print("first...", req.json())
    data += req.json()["query"]["allpages"]
    if "continue" in req.json():
        continue_data = req.json()["continue"]
        while True:
            req = session.get(api_url, params={
                'format': 'json',
                'action': 'query',
                'assert': 'user',
                'apcontinue': continue_data["apcontinue"],
                'apnamespace': apnamespace,
                'list': 'allpages',
                'aplimit': one_req_limit
            })
            print("continue...", req.json())
            data += req.json()["query"]["allpages"]
            if "continue" in req.json():
                continue_data = req.json()["continue"]
            else:
                break

    return data


def get_edit_token():
    """ get edit token.
        登录方式参考了 github.com/Bilka2/Wiki-scripts
    """
    session = login()

    get_token = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens'
    })

    token = get_token.json()['query']['tokens']['csrftoken']

    return token


def login():
    cfg = load_cfg()["wiki"]
    session = requests.Session()
    print("try to login...")
    login_token = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
    })

    login_token = login_token.json()['query']['tokens']['logintoken']

    login = session.post(api_url,
                         data={
                             'format': 'json',
                             'action': 'login',
                             'lgname': cfg["username"],
                             'lgpassword': cfg["password"],
                             'lgtoken': login_token
                         })

    if login.json()['login']['result'] != 'Success':
        raise Exception(login.json())

    print("login success!")
    return session

# The only entrance
if __name__ == '__main__':
    main()

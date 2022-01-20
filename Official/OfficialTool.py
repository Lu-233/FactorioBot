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

    pages = json.loads(Path("../data/all_page.json").read_text("UTF8"))

    session = login()

    for page in pages:
        title: str = page["title"]
        if title.endswith("/zh"):
            print(title)
            req = session.get(api_url, params={
                'format': 'json',
                'action': 'query',
                'prop': 'revisions',
                'rvlimit': 20,
                'rvprop': 'timestamp|user',
                'titles': title
            })
            print(req.json())
            print(req.text)
            break


def get_all_pages(session=None, apnamespace=0):
    if session is None:
        session = login()
    data = []
    req = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'assert': 'user',
        'list': 'allpages',
        'apnamespace': apnamespace,
        'aplimit': 500
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
                'aplimit': 500
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

    return session

# The only entrance
if __name__ == '__main__':
    main()

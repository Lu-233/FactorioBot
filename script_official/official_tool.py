import requests

from tool.cfg import load_cfg

api_url = 'https://wiki.factorio.com/api.php'


def login_official_wiki():
    """ login to wiki with username and password """
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
        print("Login Failed")
        raise Exception(login.json())

    print("login success!")
    return session
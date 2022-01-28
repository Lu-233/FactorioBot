""" check zh page name is chinsese"""
import requests
from tools import load_json


def main():
    """ main func
        print all zh page title, and manual check is chinese, if not, update the trans page
    """

    # 523
    zh_pages = load_json("../data/zh_pages.json")

    session = requests.session()

    for page in zh_pages:
        url = r"https://wiki.factorio.com/" + page['title']
        req = session.get(url)
        title = req.text.split("\n")[4]
        title = title.replace("<title>", "")
        title = title.replace(" - Factorio Wiki</title>", "")
        print(title)


if __name__ == '__main__':
    main()

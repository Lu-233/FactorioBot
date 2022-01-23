""" for wiki.factorio.com """
import json
from pathlib import Path

import requests

from Official.official_tool import login_official_wiki
from tools import load_json


def main():
    """ main func """
    print("hello factorio\n")
    tool = get_official_tool()

    # category_list = tool.all_categories()
    # print(json.dumps(category_list))
    # name2id = category_pages_filter(category_list)
    # print(json.dumps(name2id))
    # name2id = category_pages_filter(category_list, "/zh")
    # print(json.dumps(name2id))

    # working: add cache to all page

    data = tool.page_info(33685)
    print(json.dumps(data))
    # 33685


def category_pages_filter(data, trans_filter=''):

    if trans_filter:
        name2id = {page["title"]: page["pageid"] for page in data if page["title"].endswith(trans_filter)}
    else:
        name2id = {page["title"]: page["pageid"] for page in data if page["title"].find("/") < 0}

    return name2id


class WikiTool:
    """
        sample tool for get info from wiki.

        use for official factorio wiki: wiki.factorio.com
        use for bilibili factorio wiki: wiki.biligame.com/factorio

        thanks:
        - github.com/Bilka2/Wiki-scripts
        - github.com/YorkSu/bwt
    """
    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get(self, params) -> requests.Response:
        """ sorter get method """
        return self.session.get(self.api_url, params=params)

    def update_page(self, page_id):
        """ update page info cache """
        self.page_info(page_id, False)

    def page_info(self, page_id, use_cache=True):
        """
            return:
            {
              "revid": 146823,
              "parentid": 146820,
              "user": "lu",
              "userid": 2333,
              "timestamp": "2017-09-04T12:54:02Z",
              "comment": "Category overhaul, fixed description",
              "contentformat": "text/x-wiki",
              "contentmodel": "wikitext",
              "*": "{{Languages}}\n{{:Infobox:electronics}}\n\n ... \n{{TechNav}}"
            }
        """

        page_info_file = Path(f"../data/page_content/{page_id}.json")

        if use_cache and page_info_file.exists():
            print(f"Page {page_id} use cached data.")
            return load_json(page_info_file)

        data = self.get(params={
            'format': 'json',
            'action': 'query',
            'prop': 'revisions',
            'rvlimit': 1,
            'rvprop': 'ids|timestamp|flags|comment|user|userid|content',
            'pageids': page_id
        }).json()

        revision = data["query"]["pages"][str(page_id)]["revisions"][0]

        page_info_file.write_text(json.dumps(revision, ensure_ascii=False, indent=4), encoding="UTF8")

        return revision

    def category_pages(self, page_id=None) -> list:
        """ get category pages

            like:
            [{'pageid': 41257, 'ns': 14, 'title': 'Category:Ammo'}
            {'pageid': 41275, 'ns': 14, 'title': 'Category:Ammo/de'}
            {'pageid': 41276, 'ns': 14, 'title': 'Category:Ammo/zh'}
            {'pageid': 46080, 'ns': 14, 'title': 'Category:Archived'}
            {'pageid': 47731, 'ns': 14, 'title': 'Category:Archived/ru'}
            {'pageid': 41259, 'ns': 14, 'title': 'Category:Armor'}
            {'pageid': 41289, 'ns': 14, 'title': 'Category:Armor/de'}
            {'pageid': 41290, 'ns': 14, 'title': 'Category:Armor/it'}]

        """
        params = {
            'format': 'json',
            'action': 'query',
            'list': 'categorymembers',
            'cmlimit': 'max',
            'cmpageid': page_id,
            'cmnamespace': '*',
        }

        page_list = []

        while True:
            response = self.get(params).json()
            page_list += response["query"]["categorymembers"]
            if "continue" in response:
                params["cmcontinue"] = response["continue"]["cmcontinue"]
            else:
                break

        return page_list

    def all_categories(self):
        """ get all categories """
        return self.all_pages(apnamespace=14)

    def all_pages(self, apnamespace=0):
        """ get all page, list

            tested in bili, official
        """
        params = {
            'format': 'json',
            'aplimit': "max",
            'action': 'query',
            'apnamespace': apnamespace,
            'list': 'allpages',
        }

        data = []

        while True:
            response = self.get(params).json()
            data += response["query"]["allpages"]
            if "continue" in response:
                params["apcontinue"] = response["continue"]["apcontinue"]
            else:
                break

        return data

    def get_edit_token(self):
        """ get edit token. """
        get_token = self.get({
            'format': 'json',
            'action': 'query',
            'meta': 'tokens'
        })

        token = get_token.json()['query']['tokens']['csrftoken']

        return token


def get_bili_tool():
    """ WikiTool builder for bilibili factorio wiki """
    url = f"https://wiki.biligame.com/factorio/api.php"
    session = login_official_wiki()
    return WikiTool(session, url)


def get_official_tool():
    """ WikiTool builder for official factorio wiki """
    url = f"https://wiki.factorio.com/api.php"
    session = login_official_wiki()
    return WikiTool(session, url)


# for test
if __name__ == '__main__':
    main()

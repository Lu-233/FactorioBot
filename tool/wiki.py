""" for wiki.factorio.com """
import json
from pathlib import Path
import pandas as pd
import requests

from script_bili.bili_session import login_bili_wiki
from script_official.official_tool import login_official_wiki
from tools import load_json


def main():
    tool = get_bili_tool()

    # cats = tool.categories()
    # print(cats)
    #
    # for cat_id in cats.keys():
    #     data = tool.category_pages(cat_id)
    #     print(len(data), json.dumps(data, ensure_ascii=False))

    # {"pageid": 1694, "ns": 0, "title": "穿甲弹匣"}, {"pageid": 1697, "ns": 0, "title": "穿甲霰弹"},

    data = tool.page_info("1694")
    print(data)


def to_excel():
    """ main func """
    print("hello factorio\n")
    tool = get_official_tool()

    category_list = tool.categories(filters=["zh"])
    print(category_list)

    excel_file = Path('../data/zh_page.xlsx')
    writer = pd.ExcelWriter(str(excel_file), engine='xlsxwriter')

    for cat_id in category_list.keys():
        cat_name: str = category_list[cat_id]
        pages = tool.category_pages(cat_id)
        pages = [[page["title"], tool.page_info(page["pageid"])["timestamp"]] for page in pages]
        df = pd.DataFrame(pages)
        df.to_excel(writer, sheet_name=cat_name.replace("Category:", "").replace("/zh", ""))

    writer.save()


def check_zh_not_in_en():
    """ list such files: zh have, but en not

        last run result:
            ["Wave defense", "Rich text", "Military units and structures", "Railway/Train path finding", "Scenario system", "Log file", "Command line parameters", "Production statistics", "Shortcut bar", "Ghost", "Upgrade planner", "Map structure", "Quickbar"]
            ["Game-second", "Defense", "Chunk", "Modding overview", "Game-tick", "Game-day"]
    """
    tool = get_official_tool()
    # tool.pages(use_cache=False)
    en_pages = tool.pages_lang("en")
    zh_pages = tool.pages_lang("zh")

    en_pages = filter_no_trans_page(en_pages, tool)
    zh_pages = filter_no_trans_page(zh_pages, tool)

    en_pages = set([p["title"] for p in en_pages])
    zh_pages = set([p["title"].replace("/zh", "") for p in zh_pages])

    zh_not = list(en_pages - zh_pages)
    en_not = list(zh_pages - en_pages)

    print(json.dumps(zh_not))
    print(json.dumps(en_not))


def get_wanted_page():
    tool = get_official_tool()
    data = tool.get_wanted_pages()
    en_page = [d for d in data if d["title"][-6:].find("/") < 0]
    zh_page = [d for d in data if d["title"].endswith("/zh")]

    print(json.dumps(en_page))
    print(json.dumps(zh_page))


def filter_no_trans_page(pages, tool):
    """ filter unuseful page """
    # doing ...
    filtered_pages = []
    for page in pages:
        page_id = page["pageid"]
        page_name = page["title"]

        # base on wiki rule, page start with Prototype should not be translate
        if page_name.startswith("Prototype"):
            continue
        if page_name.startswith("Types/"):
            continue
        if page_name.startswith("Version history"):
            continue

        # some page no trans
        black_list = [
            "Main Page/sandbox",
            "Main Page/Latest versions",
            "Roadmap/History",
            "Uranium",  # 歧义页面，还没有提供中文翻译所以还不需要翻译
            "Fluids",  # 歧义页面，还没有提供中文翻译所以还不需要翻译
            "Data.raw",  # data
            "News",
            "Version history",
            "Glossary",
            "Version string format",
        ]

        if page_name in black_list:
            continue

        # for redirect page
        cache_file = Path(f"../data/page_content/{page_id}.json")
        if not cache_file.exists():
            print(f"file {cache_file} not found, name is {page_name}, id is {page_id}")
            tool.page_info(page_id)
            continue
        page_info = load_json(cache_file)
        content = page_info["*"]

        # for redirect page
        if content.startswith("#REDIRECT"):
            continue
        # for archive page {{Archive}}
        if content.find("{{archive}}") > -1 or content.find("{{Archive}}") > -1:
            continue
        # for Technical page, not need trans
        if content.find("[[Category:Technical]]") > 0:
            continue

        filtered_pages.append(page)
    return filtered_pages


class WikiTool:
    """
        sample tool for get info from wiki.

        use for official factorio wiki: wiki.factorio.com
        use for bilibili factorio wiki: wiki.biligame.com/factorio

        thanks:
        - github.com/Bilka2/Wiki-scripts
        - github.com/YorkSu/bwt
    """
    def __init__(self, session_func, api_url, cache_dir, no_i18n=False, **kwargs):
        self.api_url = api_url

        self.session_func = session_func
        self._session = None
        self._session_kwargs = kwargs

        self.cache_dir = Path(cache_dir)
        self.no_i18n = no_i18n

    @property
    def session(self) -> requests.Session:
        """ session, lazy login, unless need update cache
            tested in wiki and bili
        """
        if self._session is None:
            print("lazzzzzzzy getting session...")
            self._session = self.session_func(**self._session_kwargs)
        return self._session

    def _get(self, params) -> requests.Response:
        """ sorter get method
            tested in wiki and bili
        """
        return self.session.get(self.api_url, params=params)

    def get_linkshere(self, title):
        """
            tested in bili
        """
        res = self._get({
            'format': 'json',
            'action': 'query',
            'prop': 'linkshere',
            'titles': title
        })
        return res.json()["query"]["pages"]["-1"]["linkshere"]

    def get_wanted_pages(self, use_cache=True):
        """
            get wanted page
            tested in wiki and bili
        """

        cache_file = Path(self.cache_dir / f"api_wanted_page.json")

        if use_cache and cache_file.exists():
            return load_json(cache_file)

        params = {
            'format': 'json',
            'action': 'query',
            'assert': 'user',
            'list': 'querypage',
            'qppage': 'Wantedpages',
            'qplimit': 'max',
            'qpoffset': 0
        }

        wanted_pages = []

        while True:
            print(f"getting wanted pages ... {params['qpoffset']}")
            response = self._get(params).json()
            wanted_pages += response["query"]["querypage"]["results"]
            if "continue" in response:
                params["qpoffset"] = response["continue"]["qpoffset"]
            else:
                break

        print("cache file ...", cache_file)
        cache_file.write_text(json.dumps(wanted_pages, ensure_ascii=False, indent=4), encoding="UTF8")

        return wanted_pages

    def page_info(self, page_id=None, use_cache=True):
        """
            get page content and info
            tested in bili, official
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
        page_info_file = self.cache_dir / "page_content" / f"{page_id}.json"

        if use_cache and page_info_file.exists():
            return load_json(page_info_file)

        data = self._get(params={
            'format': 'json',
            'action': 'query',
            'prop': 'revisions',
            'rvlimit': 1,
            'rvprop': 'ids|timestamp|flags|comment|user|userid|content',
            'pageids': page_id
        }).json()

        revision = data["query"]["pages"][str(page_id)]["revisions"][0]

        print("update cache file: ", page_info_file)
        page_info_file.write_text(json.dumps(revision, ensure_ascii=False, indent=4), encoding="UTF8")

        return revision

    def page_info_by_title(self, title: str = None, use_cache=True):
        """
            get page content and info
            tested, in wiki and bili
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
        all_page = self.pages(use_cache=use_cache)
        title = title.strip()
        for page in all_page:
            if page["title"] == title:
                return self.page_info(page["pageid"], use_cache=use_cache)

        raise RuntimeError(f"Please check title, or update all_page cache. title: {title}.")

    def category_pages(self, cat_id=None, use_cache=True) -> list:
        """ get category pages
            tested in bili, official

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

        cache_file = self.cache_dir / "category_pages" / f"{cat_id}.json"

        if use_cache and cache_file.exists():
            return load_json(cache_file)

        params = {
            'format': 'json',
            'action': 'query',
            'list': 'categorymembers',
            'cmlimit': 'max',
            'cmpageid': cat_id,
            'cmnamespace': '*',
        }

        page_list = []

        while True:
            response = self._get(params).json()
            page_list += response["query"]["categorymembers"]
            if "continue" in response:
                params["cmcontinue"] = response["continue"]["cmcontinue"]
            else:
                break
        print("update cache ", cache_file)
        cache_file.write_text(json.dumps(page_list, ensure_ascii=False, indent=4), encoding="UTF8")

        return page_list

    @staticmethod
    def category_filter_2_dict(data, filters: list = None):
        """ filter pages, keep only one lang """
        if filters is None:
            return {p["pageid"]: p["title"] for p in data}

        id2name = {}
        for it in filters:
            if it:
                id2name.update({p["pageid"]: p["title"] for p in data if p["title"].endswith(it)})
            else:
                id2name.update({p["pageid"]: p["title"] for p in data if p["title"][-6:].find("/") < 0})

        return id2name

    def categories(self, filters: list = None, use_cache=True) -> dict:
        """ get all categories
            tested in bili, official
        """
        cats = self.pages(apnamespace=14, use_cache=use_cache)
        cats = self.category_filter_2_dict(cats, filters)
        return cats

    def pages_lang(self, lang='') -> list:
        """ get cached lang files list """

        if self.no_i18n:
            raise RuntimeError("wiki tool set to no_i18n, but trying call 'pages_lang'!")

        if lang == '':
            lang = 'en'
        if lang.startswith("/"):
            lang = lang.replace("/", '')

        cache_file = self.cache_dir / f"{lang}_pages.json"

        if not cache_file.exists():
            raise FileNotFoundError(f"can not found cached file {cache_file}")

        return load_json(cache_file)

    def pages(self, apnamespace=0, use_cache=True):
        """ get all page, list

            tested in bili, official
        """
        if apnamespace == 0:
            cache_file = self.cache_dir / "all_page.json"
        elif apnamespace == 14:
            cache_file = self.cache_dir / "all_categories.json"
        else:
            raise ValueError("apnamespace now only support 0, 14")

        if use_cache and cache_file.exists():
            return load_json(cache_file)

        params = {
            'format': 'json',
            'aplimit': "max",
            'action': 'query',
            'apnamespace': apnamespace,
            'list': 'allpages',
        }

        pages = []

        while True:
            response = self._get(params).json()
            pages += response["query"]["allpages"]
            if "continue" in response:
                params["apcontinue"] = response["continue"]["apcontinue"]
            else:
                break

        print("caching file ", cache_file)
        cache_file.write_text(json.dumps(pages, ensure_ascii=False, indent=4), encoding="UTF8")

        if apnamespace == 0 and not self.no_i18n:
            self._update_lang_page(pages, 'en')
            self._update_lang_page(pages, 'zh')

        return pages

    def _update_lang_page(self, pages, lang=''):
        """ update lang files cache
            only for wiki, no bili
        """
        if self.no_i18n:
            raise RuntimeError("wiki tool set to no_i18n, but trying call _update_lang_page")

        if lang == '' or lang == 'en':
            cache_file = self.cache_dir / "en_pages.json"
            pages = [page for page in pages if page["title"][-6:].find("/") < 0]
        else:
            if not lang.startswith("/"):
                lang = f"/{lang}"

            cache_file = self.cache_dir / f"{lang.replace('/','')}_pages.json"
            pages = [page for page in pages if page["title"].find("/zh") > 0]

        print("caching file ", cache_file)
        cache_file.write_text(json.dumps(pages, indent=4, ensure_ascii=False), encoding="UTF8")

    def edit_token(self):
        """ get edit token.
            tested in wiki and bili
        """
        get_token = self._get({
            'format': 'json',
            'action': 'query',
            'meta': 'tokens'
        })

        token = get_token.json()['query']['tokens']['csrftoken']

        return token


def get_bili_tool():
    """ WikiTool builder for bilibili factorio wiki """
    url = f"https://wiki.biligame.com/factorio/api.php"

    Path("../bili_data").mkdir(exist_ok=True)
    Path("../bili_data/category_pages").mkdir(exist_ok=True)
    Path("../bili_data/page_content").mkdir(exist_ok=True)
    Path("../bili_data/page_history").mkdir(exist_ok=True)

    return WikiTool(login_bili_wiki, url, cache_dir="../bili_data", no_i18n=True)


def get_official_tool():
    """ WikiTool builder for official factorio wiki """
    url = f"https://wiki.factorio.com/api.php"

    Path("../data").mkdir(exist_ok=True)

    return WikiTool(login_official_wiki, url, cache_dir="../data")


# for test
if __name__ == '__main__':
    main()

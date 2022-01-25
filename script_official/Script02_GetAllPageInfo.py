""" script: get all pages name """
import json

from tool.wiki import get_official_tool as get_tool


def main():
    """ save all page name """

    wiki = get_tool()

    zh_pages = wiki.pages_lang(lang='zh')

    for page in zh_pages:
        info = wiki.page_info(page_id=page["pageid"])
        print(json.dumps(info, ensure_ascii=False))

    en_pages = wiki.pages_lang(lang='en')

    for page in en_pages:
        info = wiki.page_info(page_id=page["pageid"])
        print(json.dumps(info, ensure_ascii=False))


if __name__ == '__main__':
    main()

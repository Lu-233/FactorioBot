""" script: get all pages name """
import json

from script_bili.S01_UpdateWantedPage import pages_to_cat_dict
from tool.wiki import get_bili_tool as get_tool


def main():
    """ save all page name """

    wiki = get_tool()

    all_page = wiki.pages(use_cache=True)
    pages: dict = pages_to_cat_dict(wiki, all_page)

    page_number = sum([len(pages[x]) for x in pages])

    assert page_number == 213  # 除非添加了新物品,否则这里的数量应当是 213

    done_page = 0
    for key in pages.keys():
        cat_done_page = len([x for x in pages[key] if not x["undone"]])
        done_page += cat_done_page
    print("{{进度条|{{#expr:floor(" + str(done_page) + "/213*100)}}%|3}}")
    print(f"* 总完成度：{done_page}/{page_number}")
    for key in pages.keys():
        cat_done_page = len([x for x in pages[key] if not x["undone"]])
        print(f"** [[{key}]]: {cat_done_page}/{len(pages[key])}")


if __name__ == '__main__':
    main()

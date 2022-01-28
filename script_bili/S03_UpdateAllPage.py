""" script: get all pages name """

from script_bili.S01_UpdateWantedPage import need_edit, pages_to_cat_dict
from tool.wiki import get_bili_tool as get_tool


def main():
    """
        更新物品页面 的 缓存
    """
    wiki = get_tool()

    # for item pages
    all_page = wiki.pages(use_cache=False)

    all_page = [page for page in all_page if need_edit(wiki, page)]

    pages: dict = pages_to_cat_dict(wiki, all_page)

    for key, items in pages.items():
        # if key != "零件":
        for item in items:
            wiki.page_info(item["pageid"], use_cache=False)


if __name__ == '__main__':
    main()

""" script: get all pages name """
from tool.wiki import get_bili_tool as get_tool
from script_bili.BiliTool import get_items_dict


def main():
    """
        更新物品页面 的 缓存
    """
    wiki = get_tool()

    # for item pages

    pages: dict = get_items_dict(wiki)

    for key, items in pages.items():
        # if key != "零件":
        for item in items:
            data = wiki.page_info(item["pageid"], use_cache=True)
            print(data)


if __name__ == '__main__':
    main()

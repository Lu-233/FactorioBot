"""
    bili wiki bot

    thanks https://github.com/YorkSu/bwt
"""
from collections import defaultdict

from tool.wiki import get_bili_tool as get_tool

url = f"https://wiki.biligame.com/factorio/api.php"


def main():
    """ main for test
        分割每一块页面内容
            根据标题分割

    """
    wiki = get_tool()

    pages = get_items(wiki)

    for key, value in pages.items():
        print(key, value)


def get_items(wiki, only_undone=False) -> list:
    """ all items page list """
    items = []
    for page in wiki.pages():
        content: str = wiki.page_info(page["pageid"])["*"]

        if content.startswith("{{面包屑|物品信息"):
            if only_undone and content.find("{{施工中}}") == -1:
                continue

            page["undone"] = content.find("{{施工中}}") > -1
            page["category"] = content[11:13]
            items.append(page)

    return items


def get_items_dict(wiki, only_undone=False) -> dict:
    """ all items page dict, key=cat name, value = list of page """
    items = defaultdict(list)
    for page in wiki.pages():
        content: str = wiki.page_info(page["pageid"])["*"]

        if content.startswith("{{面包屑|物品信息"):
            if only_undone and content.find("{{施工中}}") == -1:
                continue

            page["undone"] = content.find("{{施工中}}") > -1
            page["category"] = content[11:13]
            items[content[11:13]].append(page)

    return items


def get_pages_not_item(wiki, only_undone=False) -> list:
    """ get page list which are not items """
    pages = []
    for page in wiki.pages():
        content: str = wiki.page_info(page["pageid"])["*"]

        if content.startswith("{{面包屑|物品信息"):
            continue

        page["undone"] = content.find("{{施工中}}") > -1

        if only_undone and not page["undone"]:
            continue

        pages.append(page)

    return pages


if __name__ == '__main__':
    main()

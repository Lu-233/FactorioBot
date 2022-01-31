"""
    bili wiki bot

    thanks https://github.com/YorkSu/bwt
"""
from collections import defaultdict
from pathlib import Path

from tool.wiki import get_bili_tool as get_tool

url = f"https://wiki.biligame.com/factorio/api.php"


def main():
    """ main for test
        分割每一块页面内容
            根据标题分割

    """
    wiki = get_tool()

    pages = get_items_dict(wiki)  # 物流 零件 生产 武器


    cat = "物流"
    for page in pages[cat][:10]:
        page_id = page["pageid"]
        page_name = page["title"]
        page_content = wiki.page_info(page_id)["*"]

        page_content = process_page_content(page_content)

        rst_content = f"{cat}_{page_id}_{page_name}\n" \
                      f"=============================================\n\n" \
                      f".. include:: ../_static/{cat}_{page_id}_{page_name}.txt\n" \
                      f"    :literal:" \
                      f"\n\n"

        rst_file = Path(r"C:\Game\factorio_bili_wiki\source\page_content") / f"{cat}_{page_id}_{page_name}.rst"
        rst_file.write_text(rst_content, encoding="UTF8")

        txt_file = Path(r"C:\Game\factorio_bili_wiki\source\_static") / f"{cat}_{page_id}_{page_name}.txt"
        txt_file.write_text(page_content, encoding="UTF8")

def process_page_content(page_content: str):

    return page_content

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

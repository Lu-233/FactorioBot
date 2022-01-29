"""
    更新需求列表页面。需求列表是对标 wiki 的 wanted pages

    有三部分组成：
    - 物品页面 施工中
    - 文章 施工中
    - wiki api 的 wanted pages，是其他页面链接但是不存在的页面
"""
import json
import time
import warnings

from tool.wiki import get_bili_tool as get_tool
from script_bili.BiliTool import get_items, get_pages_not_item
from page_black_list import black_list, start_black_list, article_list


def main():

    confirm()  # 手动输入yes继续，以防止误运行

    wiki = get_tool()

    undone_pages = []
    for page in get_items(wiki, only_undone=True):
        if page["undone"]:
            page["value"] = 100
            page["reason"] = "物品页面处于施工中状态，需要优先维护"
            undone_pages.append(page)

    # for article pages
    for page in get_pages_not_item(wiki, only_undone=True):
        page["category"] = "文章"
        page["reason"] = "文章处于施工中状态，需要维护"
        page["value"] = "50"
        undone_pages.append(page)

    # for wanted pages
    # api 返回的需要添加的页面
    pages = wiki.get_wanted_pages(use_cache=True)
    filtered = wanted_pages_filter(pages)
    filtered = [p for p in filtered if int(p["value"]) > 1]
    for page in filtered:
        page["category"] = "未知"
        title: str = page['title'].replace(" ", "_")
        page["reason"] = f"由Wiki API计算，请先检查是否需要，请参考[[https://wiki.biligame.com/factorio/index.php?title=特殊:链入页面&target={title} 链入页面]]"
        undone_pages.append(page)
        # print(page['title'])

    # for wanted page from api
    update_need_pages(wiki, undone_pages)


def wanted_pages_filter(pages):
    filtered = []
    for p in pages:
        title: str = p["title"]
        if title.startswith("模块:"):
            continue
        if title.startswith("分类:"):
            continue
        if title.startswith("模板:"):
            continue
        if title.startswith("文件:"):
            continue
        if title.startswith("新闻"):
            continue
        if title.startswith("版本历史"):
            continue
        filtered.append(p)
    return filtered


def confirm():
    """ confirm by hand"""
    print("本程序会修改wiki页面：需求列表")
    is_confirm = input("请输入 yes 继续操作：")
    if not is_confirm == "yes":
        print("exiting...")
        exit(0)


def update_need_pages(wiki, page_list):
    """ 更新需求列表页面
        拼字符串组装页面
    """
    wanted_page_str = ""

    wanted_page_str += "{{面包屑||维护}}" + "\n"
    wanted_page_str += "{{文章时效}}" + "\n"
    wanted_page_str += "" + "\n"
    wanted_page_str += "= 需求列表 =" + "\n"
    wanted_page_str += "注意：本页面是自动生成的。" + "\n"
    wanted_page_str += f'更新时间：{time.strftime("%Y-%m-%d %H:%M:%S")}' + "\n"
    wanted_page_str += "" + "\n"
    wanted_page_str += f"需要维护的页面数量: {len(page_list)}" + "\n"
    wanted_page_str += "{|class=wikitable" + "\n"
    wanted_page_str += "!#" + "\n"
    wanted_page_str += "!页面" + "\n"
    wanted_page_str += "!类别" + "\n"
    wanted_page_str += "!权重" + "\n"
    wanted_page_str += "!原因" + "\n"
    for i, page in enumerate(page_list):
        wanted_page_str += "|-" + "\n"
        wanted_page_str += f"|{i+1}" + "\n"
        if page["category"] != "未知":
            wanted_page_str += f"|[[{page['title']}]]" + "\n"
        else:
            wanted_page_str += f"|{page['title']}" + "\n"
        wanted_page_str += f"|{page['category']}" + "\n"
        wanted_page_str += f"|{page['value']}" + "\n"
        wanted_page_str += f"|{page['reason']}" + "\n"
    wanted_page_str += "|}" + "\n"

    print(wanted_page_str)

    token = wiki.edit_token()
    res = wiki.session.post(wiki.api_url, data={
        'format': 'json',
        'action': 'edit',
        'title': '需求列表',
        'text': wanted_page_str,
        'summary': '自动更新需求列表',
        'bot': True,
        'token': token,
    })
    print(json.dumps(res.json(), ensure_ascii=False))


def normal_start(data: str):
    """ 粗暴的判断是否符合规则 """
    flag = False
    if data.startswith("{{面包屑|物品信息|物流}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|武器}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|生产}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|零件}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True

    if data.startswith("{{面包屑|物品信息|物流}}\n{{施工中}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|武器}}\n{{施工中}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|生产}}\n{{施工中}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    if data.startswith("{{面包屑|物品信息|零件}}\n{{施工中}}\n{{物品信息\n|物品名称={{PAGENAME}}\n}}\n"):
        flag = True
    return flag


if __name__ == '__main__':
    main()

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

from collections import defaultdict
from tool.wiki import get_bili_tool as get_tool
from page_black_list import black_list, start_black_list, article_list


def main():

    confirm()  # 手动输入yes继续，以防止误运行

    wiki = get_tool()

    # for item pages
    all_page = wiki.pages(use_cache=True)

    # 过滤，保留需要编辑的页面
    all_page = [page for page in all_page if need_edit(wiki, page)]

    pages: dict = pages_to_cat_dict(wiki, all_page)

    page_list = []
    for key, item in pages.items():
        for page in item:
            if page["undone"]:
                page["category"] = key
                page["value"] = 100
                page["reason"] = "物品页面处于施工中状态，需要优先维护"
                page_list.append(page)

    pages = wiki.get_wanted_pages(use_cache=True)
    filtered = [p for p in pages if need_edit(wiki, p)]

    # for article pages
    for title in article_list:
        data: str = wiki.page_info_by_title(title)["*"]
        if data.find("{{施工中}}") > -1:
            page_list.append({
                "title": title,
                "category": "文章",
                "reason": "文章处于施工中状态，需要维护",
                "value": "50",
            })

    # api 返回的需要添加的页面
    for page in filtered:
        page["category"] = "未知"
        title: str = page['title'].replace(" ", "_")
        page["reason"] = f"由Wiki API计算，请先检查是否需要，请参考[[https://wiki.biligame.com/factorio/index.php?title=特殊:链入页面&target={title} 链入页面]]"
        page_list.append(page)

    # for wanted page from api
    update_need_pages(wiki, page_list)


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


def pages_to_cat_dict(wiki, pages):
    """ classify pages, return class and undone"""
    filtered = defaultdict(list)
    for page in pages:
        content: str = wiki.page_info(page["pageid"])["*"]
        page["undone"] = (content.find("{{施工中}}") > -1)

        cat_name = get_cls(content)
        filtered[cat_name].append(page)

    return filtered


def need_edit(wiki, page):
    """ 判断是否需要编辑 """
    flag = True

    title: str = page["title"]

    # 不需要编辑
    if title in black_list:
        return False

    # 不需要编辑
    for item in start_black_list:
        if title.startswith(item):
            return False

    # 目前不编辑
    if title in article_list:
        return False

    # wiki api 返回的页面， 过滤掉 value 过低的，因为已经有太多页面缺失了
    if "value" in page and int(page["value"]) <= 1:
        return False

    # 获取页面内容，以进一步过滤编辑条件
    if "pageid" in page:  # 常规情况
        content: str = wiki.page_info(page["pageid"])["*"]  #
    else:
        try:  # 如果没有 pageid，就尝试通过 title 从缓存拿页面
            content: str = wiki.page_info_by_title(page["title"])["*"]
        except RuntimeError:
            return True  # 不存在的页面，需要编辑

    # 跳过重定向页面
    if content.find("#重定向 [[") != -1:
        return False

    # 跳过教程
    if content.find("{{面包屑|教程}}") != -1:
        return False

    # 非物品信息页面。之前已经过滤过其他页面了，到这里的非物品页面，一定是新页面，需要添加到 page black list 里边
    if content.find("{{面包屑|物品信息|") == -1:
        warnings.warn(f"异常页面: {title}, 可能是新页面，没有用面包屑物品信息开头")

    # 物品信息页面应当严格遵循格式
    if not normal_start(content):
        warnings.warn(repr(content))

    return flag


def get_cls(data: str):
    """ 粗暴的判断物品信息类别 """
    if data.startswith("{{面包屑|物品信息|物流}}"):
        return "物流"
    if data.startswith("{{面包屑|物品信息|武器}}"):
        return "武器"
    if data.startswith("{{面包屑|物品信息|生产}}"):
        return "生产"
    if data.startswith("{{面包屑|物品信息|零件}}"):
        return "零件"
    warnings.warn(f"未知类别 {data[:20]}")
    return "未知"


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

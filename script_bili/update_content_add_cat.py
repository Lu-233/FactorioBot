import json

from tool.wiki import get_bili_tool as get_tool, WikiTool
from script_bili.BiliTool import get_items_dict, get_items


def main():
    wiki = get_tool()

    pages = get_items_dict(wiki)  # 物流 零件 生产 武器
    pages = pages["武器"]

    append = "[[分类:武器]][[分类:物品信息]]"

    for page in pages:
        page_id = page["pageid"]
        title = page["title"]
        content: str = wiki.page_info(page_id, use_cache=True)["*"]

        if content.find(append) > -1:
            print(f" 跳过 {title}")
            continue
        print("处理 ", title, " ...")
        content = content.replace("{{武器导航}}", append+"\n{{武器导航}}")

        summary = f'bot: bot添加分类：[[分类:武器]][[分类:物品信息]]'
        wiki.update(page_id, content, summary)


if __name__ == '__main__':
    main()

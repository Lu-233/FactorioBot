""" 输出wiki施工进展

    输出的字符串需要手动更新到wiki上。

    在输出wiki用的字符串之前，还输出有哪些页面没有完成。
"""
from script_bili.S01_UpdateWantedPage import need_edit, pages_to_cat_dict
from tool.wiki import get_bili_tool as get_tool


def main():
    wiki = get_tool()

    all_page = wiki.pages(use_cache=True)
    all_page = [page for page in all_page if need_edit(wiki, page)]

    pages: dict = pages_to_cat_dict(wiki, all_page)

    page_number = sum([len(pages[x]) for x in pages])  # 这里应该是213，现在是212还不知道为啥少了谁。

    # 计算每个类别完成的页面数量，输出未完成的页面
    done_page = 0
    for key in pages.keys():
        done_page += len([x["title"] for x in pages[key] if not x["undone"]])

        undone_pages = [x["title"] for x in pages[key] if x["undone"]]
        print(key, undone_pages)

    #输出wiki字符串
    print("\n\n{{进度条|{{#expr:floor(" + str(done_page) + "/213*100)}}%|3}}")
    print(f"* 总完成度：{done_page}/{page_number}")
    for key in pages.keys():
        cat_done_page = len([x for x in pages[key] if not x["undone"]])
        print(f"** [[{key}]]: {cat_done_page}/{len(pages[key])}")


if __name__ == '__main__':
    main()

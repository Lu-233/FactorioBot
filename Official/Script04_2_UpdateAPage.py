import json
from pathlib import Path

from Official.OfficialTool import login
from tools import load_json
from Script04_GetPageContent import save_page
from Script03_GetPageHistory import get_page_history

session = login()

def main():
    """ main func """
    target_name = "Explosives (research)"

    pages = load_json("../data/all_page.json")
    name2page = {x["title"]: x for x in pages}

    update(target_name, name2page)
    update(target_name+"/zh", name2page)


def update(target_name, name2page):
    if target_name not in name2page:
        print("can not find page: ", target_name)
        exit(0)

    page = name2page[target_name]
    pageid = str(page["pageid"])


    save_page(pageid, session)  # update content
    get_page_history(page, session)  # update history


if __name__ == '__main__':
    main()

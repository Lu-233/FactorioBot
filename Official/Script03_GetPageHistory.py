""" script: update pages history """
import json
from pathlib import Path

from Official.OfficialTool import api_url, login
from tools import load_json


def main():
    """ main """
    # pages = get_all_history("../data/zh_pages.json")
    pages = get_all_history("../data/en_pages.json")
    # pages = Path("../data/en_pages.json")


def get_all_history(filepath):

    pages = load_json(filepath)
    # [{'pageid': 23, 'title': 'Acor/zh'}, ... , {'pageid': 2, 'title': 'Acts/zh'}]

    his_store = Path("../data/page_history")
    his_store.mkdir(exist_ok=True)

    session = login()

    for i, page in enumerate(pages):
        print(f"{i}/{len(pages)} get history for: ", page["title"], page["pageid"])

        save = his_store / f'{page["pageid"]}.json'
        revisions = get_page_history(session, page)
        revisions = {
            "page": page,
            "revisions": revisions
        }
        save.write_text(json.dumps(revisions, ensure_ascii=False, indent=4), encoding="UTF8")


def get_page_history(session, page):
    """ get history """
    pageid = str(page["pageid"])

    req = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'prop': 'revisions',
        'rvlimit': 25,
        'rvprop': 'timestamp|user|comment',
        'pageids': pageid
    })

    revisions = req.json()["query"]["pages"][pageid]["revisions"]

    return revisions


def split(data, length):
    """ split list to list of list
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-or-iterable-into-evenly-sized-chunks
    """
    length = max(1, length)
    return (data[i:i + length] for i in range(0, len(data), length))

if __name__ == '__main__':
    main()

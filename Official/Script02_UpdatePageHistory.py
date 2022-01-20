""" script: update pages history """
import json
from pathlib import Path

from Official.OfficialTool import api_url, login


def main():

    pages = Path("../data/all_page.json")
    pages = pages.read_text("UTF8")
    pages = json.loads(pages)

    session = login()

    for page in pages:
        title: str = page["title"]
        if title.endswith("/zh"):
            print(title)
            req = session.get(api_url, params={
                'format': 'json',
                'action': 'query',
                'prop': 'revisions',
                'rvlimit': 20,
                'rvprop': 'timestamp|user|comment',
                # 'rvprop': 'timestamp|user|comment|content',
                'titles': title
            })
            print(req.json())
            print(req.text)
            break


if __name__ == '__main__':
    main()
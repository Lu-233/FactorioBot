"""
前置项目 github.com/Lu-MPI/FactorioDataRaw2Json
需要其输出
"""
import json
from pathlib import Path

from game_info.item_data import rmkey
from tool.tools import load_json


def main():

    data = load_json(Path("v_1.1.53_data_part.json"))

    items = {}
    update_dict(items, data["recipe"])
    update_dict(items, data["item"])
    update_dict(items, data["ammo"])
    update_dict(items, data["capsule"])
    update_dict(items, data["gun"])
    update_dict(items, data["item-with-entity-data"])
    update_dict(items, data["blueprint-book"])
    update_dict(items, data["blueprint"])
    update_dict(items, data["module"])
    update_dict(items, data["rail-planner"])
    update_dict(items, data["spidertron-remote"])
    update_dict(items, data["tool"])
    update_dict(items, data["armor"])
    update_dict(items, data["repair-tool"])
    update_dict(items, data["fluid"])


    Path("items.json").write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding="UTF8")


def update_dict(all:dict,data:dict):
    for k,v in data.items():
        if k in all:
            all[k].update(v)
        else:
            all[k] = v



if __name__ == '__main__':
    main()

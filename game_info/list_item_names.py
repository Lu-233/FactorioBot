from pathlib import Path

from game_info.data_loader import load_base_cfg
from game_info.item_data import item2zh



def get_en2zh():

    data = {}
    items_str = Path("../game_info/game_data/items.txt").read_text("UTF8")
    items = items_str.split("\n")

    base_cfg_en = load_base_cfg(lang="en")
    base_cfg = load_base_cfg(lang="en")
    for it in items:
        if it in black_list:
            continue
        if it.startswith("spidertron-rocket-launcher"):
            it = "spidertron-rocket-launcher"
        data[item2zh(it, base_cfg)] = item2zh(it, base_cfg_en)
    return data

def main():
    pass

black_list = [
    "dummy-steel-axe",
    "heavy-oil-barrel",
    "light-oil-barrel",
    "lubricant-barrel",
    "petroleum-gas-barrel",
    "sulfuric-acid-barrel",
    "water-barrel",
    "item-unknown",
]


if __name__ == '__main__':
    main()
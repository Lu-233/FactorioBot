from pathlib import Path

from game_info.tech_loader import load_tech
from game_info.tech_data import tech2zh


def main():
    """
        icon_mipmaps = 4
        icon_size = 256
    """
    todo_ket = ["icon_mipmaps", "icon_size", "icons", "icon"]
    tech_data = load_tech("1.1.53")
    for i, (key, data) in enumerate(tech_data.items()):
        inside_name = data["name"]
        name = data["name"]
        if "localised_name" in data.keys():
            name: str = data["localised_name"][0]
            name = name.replace("technology-name.", "")

        if name in single_tech_page_black_list and name not in merge_tech_page_white_list:
            continue

        cn_name = tech2zh(name, pre_name="科技-")
        if "icons" in data:
            gen_icon(cn_name, data["icons"][0]["icon"], data["icons"][1]["icon"])
        else:
            gen_icon(cn_name, data["icon"])


def gen_icon(name, base_img: str, add_img: str = None):
    from PIL import Image
    pre_path = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Factorio\data")
    base_img = pre_path / base_img.replace("_", "")  # replace __core__ to core __base__ to base
    if add_img:
        add_img = pre_path / add_img.replace("_", "")  # replace __core__ to core __base__ to base

    base_img = Image.open(base_img).convert("RGBA")
    base_img = base_img.crop((0, 0, 256, 256))

    if add_img:
        add_img = Image.open(add_img).convert("RGBA")
        add_img = add_img.crop((0, 0, 128, 128))
        base_img.paste(add_img, (128+100-64, 128+100-64), add_img)

    img_file = f'z:/{name}.png'
    print(img_file)
    base_img.save(img_file)



merge_tech_page_white_list = [
    "artillery-shell-range-1",
    "artillery-shell-speed-1",
    "braking-force-1",
    "energy-weapons-damage-1",
    "follower-robot-count-1",
    "inserter-capacity-bonus-1",
    "laser-shooting-speed-1",
    "mining-productivity-1",
    "physical-projectile-damage-1",
    "refined-flammables-1",
    "research-speed-1",
    "stronger-explosives-1",
    "weapon-shooting-speed-1",
    "worker-robots-speed-1",
    "worker-robots-storage-1",
]

single_tech_page_black_list = [
    "artillery-shell-range-1",
    "artillery-shell-speed-1",
    "braking-force-1",
    "braking-force-2",
    "braking-force-3",
    "braking-force-4",
    "braking-force-5",
    "braking-force-6",
    "braking-force-7",
    "energy-weapons-damage-1",
    "energy-weapons-damage-2",
    "energy-weapons-damage-3",
    "energy-weapons-damage-4",
    "energy-weapons-damage-5",
    "energy-weapons-damage-6",
    "energy-weapons-damage-7",
    "follower-robot-count-1",
    "follower-robot-count-2",
    "follower-robot-count-3",
    "follower-robot-count-4",
    "follower-robot-count-5",
    "follower-robot-count-6",
    "follower-robot-count-7",
    "inserter-capacity-bonus-1",
    "inserter-capacity-bonus-2",
    "inserter-capacity-bonus-3",
    "inserter-capacity-bonus-4",
    "inserter-capacity-bonus-5",
    "inserter-capacity-bonus-6",
    "inserter-capacity-bonus-7",
    "laser-shooting-speed-1",
    "laser-shooting-speed-2",
    "laser-shooting-speed-3",
    "laser-shooting-speed-4",
    "laser-shooting-speed-5",
    "laser-shooting-speed-6",
    "laser-shooting-speed-7",
    "mining-productivity-1",
    "mining-productivity-2",
    "mining-productivity-3",
    "mining-productivity-4",
    "physical-projectile-damage-1",
    "physical-projectile-damage-2",
    "physical-projectile-damage-3",
    "physical-projectile-damage-4",
    "physical-projectile-damage-5",
    "physical-projectile-damage-6",
    "physical-projectile-damage-7",
    "refined-flammables-1",
    "refined-flammables-2",
    "refined-flammables-3",
    "refined-flammables-4",
    "refined-flammables-5",
    "refined-flammables-6",
    "refined-flammables-7",
    "research-speed-1",
    "research-speed-2",
    "research-speed-3",
    "research-speed-4",
    "research-speed-5",
    "research-speed-6",
    "stronger-explosives-1",
    "stronger-explosives-2",
    "stronger-explosives-3",
    "stronger-explosives-4",
    "stronger-explosives-5",
    "stronger-explosives-6",
    "stronger-explosives-7",
    "weapon-shooting-speed-1",
    "weapon-shooting-speed-2",
    "weapon-shooting-speed-3",
    "weapon-shooting-speed-4",
    "weapon-shooting-speed-5",
    "weapon-shooting-speed-6",
    "worker-robots-speed-1",
    "worker-robots-speed-2",
    "worker-robots-speed-3",
    "worker-robots-speed-4",
    "worker-robots-speed-5",
    "worker-robots-speed-6",
    "worker-robots-storage-1",
    "worker-robots-storage-2",
    "worker-robots-storage-3",
]


if __name__ == '__main__':
    main()
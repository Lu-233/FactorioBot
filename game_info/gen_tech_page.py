from game_info.tech_loader import load_tech


def main():
    """
        icons, icon
        name : str -数 结尾，本地化时，会忽略数字。
        upgrade : 包含升级，wiki需要只写一个
        unit : 研究点
            count : uint64 : 需要多少个研究点，指定了count_formula则可能不指定它
            count_formula : str : 公式，按BODMAS顺序执行
            time : 每个研究点需要多少时间，秒
            ingredients : 一个研究点需要的成分清单
        max_level : 最高等级 infinite
        prerequisites : 前置科技列表
        effects : 技术效果列表

        关注order，用于生成技术列表

        ignore_tech_cost_multiplier 忽略难度乘数

        localised_description 翻译时的解释
        localised_name 翻译时的名字

        upgrade：无参考意义，因为一些需要单独列出的科技也为true
    """

    keys = ["unit", "effects", "", "", ""]
    todo_ket = ["icon_mipmaps", "icon_size", "icons", "icon"]
    dismiss = ["order", "upgrade", "order"]
    done_keys = ["name", "max_level", "prerequisites", "ignore_tech_cost_multiplier", "", "", "", "", "", ""]

    tech_data = load_tech("1.1.53")
    tech_names = [t["name"] for k, t in tech_data.items()]
    print(len(tech_names))
    for i, (key, data) in enumerate(tech_data.items()):
        inside_name = data["name"]
        name = data["name"]
        if "localised_name" in data.keys():
            name: str = data["localised_name"][0]
            name = name.replace("technology-name.", "")

        count_formula = ""
        infinite_level = False
        if "max_level" in data:
            assert data["max_level"] == "infinite"
            infinite_level = True
            count_formula = data["unit"]["count_formula"]

        prerequisites = data["prerequisites"] if "prerequisites" in data else []
        from game_info.tech_data import tech2zh
        prerequisites = [tech2zh(p) for p in prerequisites]

        ignore = "ignore_tech_cost_multiplier"
        ignore = bool(data[ignore]) if ignore in data else False

        unit = data["unit"]
        # count may
        # count_formula may
        # time
        # ingredients
        # if inside_name in single_tech_page_black_list and inside_name not in merge_tech_page_white_list:
        #
        #     print(i, tech2zh(name), "\t", unit)

def gen_single_page(tech_data):

    pass

def check_infinite(name: str, tech_names: list, tech_data):
    # tech_inside_names
    names = name.split("-")
    if not names[-1].isnumeric():
        return False

    i = 1
    while name.replace(names[-1], str(i+1)) in tech_names:
        i += 1

    end_name = name.replace(names[-1], str(i))
    # tech_data = load_tech("1.1.53")

    if "max_level" in tech_data[end_name]:
        print(tech2zh(end_name), tech2zh(name))

    return True


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
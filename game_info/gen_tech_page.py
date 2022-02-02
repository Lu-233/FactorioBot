import json
from collections import defaultdict

from game_info.tech_data import tech2zh, tech_list, tech_group_dict
from game_info.data_loader import load_tech, load_base_cfg


def main():
    """ 生成技术页面 """

    keys = ["unit", "effects", "", "", ""]
    dismiss = ["order", "upgrade", "icon_mipmaps", "icon_size", "icons", "icon"]
    done_keys = ["name", "max_level", "prerequisites", "ignore_tech_cost_multiplier", "", "", "", "", "", ""]

    tech_data = load_tech("1.1.53")
    base_cfg = load_base_cfg()

    pages = []
    after_tech = defaultdict(list)

    for i, (_, data) in enumerate(tech_data.items()):
        inside_name: str = data["name"]
        if inside_name in single_tech_page_black_list:
            if inside_name not in merge_tech_page_white_list:
                continue
            builder = PageBuilder(tech_data, base_cfg, inside_name, False)
            i = 1
            while inside_name.replace("-1", f"-{i}") in single_tech_page_black_list:
                tmp_builder = PageBuilder(tech_data, base_cfg, inside_name.replace("-1", f"-{i}"))
                builder.buff_list.append(tmp_builder.buff)
                builder.unit_list.append(tmp_builder.unit)
                builder.prerequisites_list.append(tmp_builder.prerequisites)
                # print(tmp_builder.prerequisites)
                for tech in tmp_builder.prerequisites:
                    after_tech[tech].append(tmp_builder.name)
                i += 1
        else:
            builder = PageBuilder(tech_data, base_cfg, inside_name)
            for tech in builder.prerequisites:
                after_tech[tech].append(builder.name)
        pages.append(builder)

    for p in pages:
        if p.name in after_tech:
            p.after_tech = after_tech[p.name]

    from tool.wiki import get_bili_tool
    wiki = get_bili_tool()
    for p in pages:
        # if p.inside_name in merge_tech_page_white_list[:3]:
        #     page_str = p.gen_merge_page()
        #     print("update page ", p.name)
        if p.inside_name not in single_tech_page_black_list:
            # print(p.name)
            page_str = p.gen_page()

            token = wiki.edit_token()
            res = wiki.session.post(wiki.api_url, data={
                'format': 'json',
                'action': 'edit',
                'title': p.name,
                'text': page_str,
                'summary': 'bot: 更新技术页面：' + p.name + " 现在迁至科技和解锁科技以表格形式呈现",
                'bot': True,
                'token': token,
            })
            print(json.dumps(res.json(), ensure_ascii=False))

class PageBuilder:
    name: str
    desc: str
    ignore_tech_cost_multiplier: bool

    unit: dict  # {count time ingredients}
    prerequisites: list
    buff: list  # list of desc
    unlock: list  # list of zh name

    after_tech: list

    buff_list: list  # for multi level page
    unit_list: list  # for multi level page
    prerequisites_list: list  # for multi level page

    after_tech_list: list

    def __init__(self, tech_data, base_cfg, inside_name, single_page=True):
        self.inside_name = inside_name
        self.name = ""
        self.en_name = ""
        self.sub_cls = ""

        self.page_data = tech_data[inside_name]
        self.base_cfg = base_cfg

        self.init_page_info(inside_name)

        self.single_page = single_page
        self.after_tech = []

        if not single_page:
            self.buff_list: list = []
            self.unit_list: list = []
            self.prerequisites_list: list = []
            self.after_tech_list: list = []

    # noinspection DuplicatedCode
    def gen_merge_page(s):
        """ 生成多个等级的页面，buff页面 """
        if s.single_page:
            raise RuntimeError(" need use gen_page")
        # head
        page = "{{面包屑|科技}}" + "\n"
        page += "{{科技信息" + "\n"
        page += "|科技名称={{PAGENAME}}" + "\n"
        page += f"|英文={s.en_name}" + "\n"
        page += f"|内部名={s.inside_name}" + "\n"
        page += f"|分类=科技" + "\n"
        page += f"|子分类={s.sub_cls}" + "\n"
        page += f"|数据版本=1.1.53" + "\n"
        page += "}}" + "\n"
        page += f"" + "\n"

        # content

        page += f"'''{s.name}'''：{s.desc}" + "\n"
        page += f"" + "\n"
        page += f'{s.name.replace("科技:","")}包含多个等级，如下表所示：' + "\n"
        page += f"" + "\n"

        # skip unlock all is empty

        # 剩下的做一个大表
        # print(p.name, len(p.buff_list), len(p.unit_list), p.prerequisites_list)
        tech_names = [line[1] for line in tech_list]

        page += '{| class="wikitable"' + "\n"
        page += '! 科技 !! 成本 !! 加成 !! 前置科技' + "\n"
        for i, (buff, unit, pre) in enumerate(zip(s.buff_list,s.unit_list,s.prerequisites_list)):
            page += '|-' + "\n"

            unit_str = ""
            unit_str += "{{图标|时间|" + str(unit["time"]) + "||40}}"
            for it in unit["ingredients"]:
                unit_str += " {{图标|" + it + "|1||40}}"
            if unit["count_formula"]:
                unit_str += ' <br> <big> ✖ {{按键|' + unit["count_formula"] + '}}</big> 其中，{{按键|L}}为等级'
            else:
                unit_str += f' <big> ✖ {unit["count"]}</big>'

            buff_str = ""
            for it in buff:
                buff_str += it + "<br>"
            buff_str = buff_str.rstrip("<br>")

            pre_str = ""
            for it in pre:

                if it.replace("科技:", "") in tech_names and it != s.name:
                    pre_str += " [[" + it + "|" + it.replace("科技:", "") + "]]" + "<br>"
                    # pre_str += "{{图标|" + it.replace(":", "-") + "||" + it.replace("科技:", "") + "|48}} "
                else:
                    pre_str += " " + it.replace("科技:", "") + "<br>"
            pre_str = pre_str.rstrip("<br>")
            if unit["count_formula"]:
                level_str = f"{i+1}-&infin;"
            else:
                level_str = str(i+1)

            page += '| ' \
                    '<div style="text-align:center;">{{图标|' + s.name.replace(":","-") + '|' + level_str + '||48}}' \
                    '<br>' + s.name.replace("科技:", "") + f'{level_str}</div>' \
                    '||' \
                    f'{unit_str}' \
                    '|| ' \
                    f'{buff_str}' \
                    '|| ' \
                    f'{pre_str}' \
                    "\n"

        page += '|}' + "\n"

        page += f"" + "\n"

        page += "[[分类:科技]]" + "\n"
        page += "{{科技导航}}" + "\n"

        return page

    def gen_page(s):
        """
            页面描述
            前置科技
            研究效果，和影响的具体内容，是谁的前置科技
            研究成本
        """
        if not s.single_page:
            raise RuntimeError(" need use gen_merge_page")
        # head
        page = "{{面包屑|科技}}" + "\n"
        page += "{{科技信息" + "\n"
        page += "|科技名称={{PAGENAME}}" + "\n"
        page += f"|英文={s.en_name}" + "\n"
        page += f"|内部名={s.inside_name}" + "\n"
        page += f"|分类=科技" + "\n"
        page += f"|子分类={s.sub_cls}" + "\n"
        page += f"|数据版本=1.1.53" + "\n"
        page += "}}" + "\n"
        page += f"" + "\n"

        # content
        page += f"'''{s.name}'''：{s.desc}" + "\n"
        page += f"" + "\n"
        if len(s.unlock) > 0:
            page += f"== 解锁: ==" + "\n"
            page += f"" + "\n"
            page += f"科技解锁了以下配方：" + "\n"
            page += f"" + "\n"
            for u in s.unlock:
                page += "* {{图标|" + u + "|||32|frame=none}} [[" + u + "]]\n"

            page += f"" + "\n"

        if len(s.buff) > 0:
            page += f"== 加成: ==" + "\n"
            page += f"" + "\n"
            for u in s.buff:
                page += f"* {u}" + "\n"

            page += f"" + "\n"

        if s.unit:
            page += f"== 研究成本: ==" + "\n"
            page += f"" + "\n"
            page += f"在研究中心没有加成的情况下，研究成本如下所示。"
            if not s.ignore_tech_cost_multiplier:
                page += f"如果你选择了自定义研究难度系数，还要在当前的成本上乘以系数。" + "\n"
            else:
                page += f"即使你选择了自定义研究难度系数，此研究的成本也不会变化。" + "\n"
            page += f"" + "\n"
            page += f'{s.name.replace("科技:","")}共需要{s.unit["count"]*s.unit["time"]}秒研究时间'
            for it in s.unit["ingredients"]:
                page += f'，{s.unit["count"]}瓶{it}'
            page += f"。" + "\n"
            page += f"" + "\n"
            # page += "({{I|时间|" + str(s.unit["time"]) + "|64}}"
            page += "研究成本 = ( {{图标|时间|" + str(s.unit["time"]) + "}}"
            for it in s.unit["ingredients"]:
                page += " + {{图标|" + it + "|frame=none}}"
            page += ") ✖ " + str(s.unit["count"]) + "\n"
            page += f"" + "\n"

        if len(s.prerequisites) > 0:
            page += f"== 前置科技 ==" + "\n"
            page += f"" + "\n"
            page += f"只有掌握了前置科技，才能研究本科技。" + "\n"
            page += f"" + "\n"
            # for pre in s.prerequisites:
            #     page += "* {{图标|" + pre.replace(":","-") + "||" + pre + "|48}} [[" + pre + "|" + pre.replace("科技:","") +"]]" + "\n"

            page += '{| class="wikitable"' + "\n"
            for pre in s.prerequisites:
                page += '|'
                page += ' <div style="text-align:center;">{{图标|' + pre.replace(":", "-") + "||" + pre + "|48}}</div>  ||"
            page = page.rstrip("||")
            page += "\n" + '|-' + "\n"
            for pre in s.prerequisites:
                page += '| '
                page += ' <div style="text-align:center;">[[' + pre + "|" + pre.replace("科技:","") + "]]</div> ||"
            page = page.rstrip("||")
            page += '\n|}' + "\n"

            page += f"" + "\n"

        if len(s.after_tech) > 0:
            page += f"== 解锁科技 ==" + "\n"
            page += f"" + "\n"
            page += f"{s.name}是以下科技的前置科技，研究{s.name.replace('科技:','')}是它们的必要条件：" + "\n"
            page += f"" + "\n"
            page += '{| class="wikitable"' + "\n"
            page += '' + "\n"
            page += '' + "\n"
            for pre in s.after_tech:
                page += '|'
                page += ' <div style="text-align:center;">{{图标|' + pre.replace(":", "-") + "||" + pre + "|48}}</div>  ||"
            page = page.rstrip("||")
            page += "\n" + '|-' + "\n"
            for pre in s.after_tech:
                page += '| '
                page += ' <div style="text-align:center;">[[' + pre + "|" + pre.replace("科技:","") + "]]</div> ||"
            page = page.rstrip("||")
            page += '\n|}' + "\n"

        page += '' + "\n"

        page += "[[分类:科技]]" + "\n"
        page += "{{科技导航}}" + "\n"

        return page

    def init_page_info(self, inside_name):

        page = self.page_data

        # name and desc
        name_find_name = inside_name
        desc_find_name = inside_name
        if "localised_name" in page.keys():
            name_find_name: str = page["localised_name"][0]
            name_find_name = name_find_name.replace("technology-name.", "")
        if "localised_description" in page.keys():
            desc_find_name: str = page["localised_description"][0]
            desc_find_name = desc_find_name.replace("technology-description.", "")

        self.name = tech2zh(name_find_name, "科技:", self.base_cfg["technology-name"])
        self.desc = tech2zh(desc_find_name, "", self.base_cfg["technology-description"], False)

        for line in tech_list:
            if inside_name == line[2]:
                self.sub_cls = tech_group_dict[line[0]]
                self.en_name = line[3]

        u = page["unit"]
        self.unit = {
            "count": u["count"] if "count" in u else None,
            "count_formula": u["count_formula"] if "count_formula" in u else None,
            "time": u["time"],
            "ingredients": [self.item2zh(k) for k in u["ingredients"].keys()],
        }
        self.ignore_tech_cost_multiplier = "ignore_tech_cost_multiplier" in page
        self.prerequisites = [tech2zh(p, "科技:") for p in page["prerequisites"]] if "prerequisites" in page else []

        self.buff = []
        self.unlock = []
        if "effects" in page:
            for effects in page["effects"]:
                if effects["type"] == "unlock-recipe":
                    self.unlock.append(self.item2zh(effects['recipe']))
                else:
                    self.buff.append(self.get_effects_dict()[effects["type"]](effects))

    def get_effects_dict(self):
        ammo_category_dict = {
            "bullet": "子弹", "laser": "激光", "beam": "能量束", "electric": "电击",
            "shotgun-shell": "霰弹", "cannon-shell": "制式炮弹", "flamethrower": "火焰",
            "grenade": "手雷", "landmine": "地雷", "rocket": "火箭弹", "artillery-shell": "重炮炮弹"
        }
        turret_id_dict = {
            "gun-turret": "机枪炮塔射速",
            "flamethrower-turret": "火焰炮塔伤害",
        }
        effects_dict = {
            "ammo-damage": lambda e: ammo_category_dict[e["ammo_category"]] + f'伤害 +{int(e["modifier"] * 100)}%',
            "gun-speed": lambda e: ammo_category_dict[e["ammo_category"]] + f'射速 +{int(e["modifier"] * 100)}%',
            "worker-robot-storage": lambda e: f"作业机器人货物运量 +{e['modifier']}",
            "worker-robot-speed": lambda e: f"作业机器人移动速度 +{int(e['modifier'] * 100)}%",
            "artillery-range": lambda e: f"重炮炮弹射程 +{int(e['modifier'] * 100)}%",
            "train-braking-force-bonus": lambda e: f"火车制动力 +{int(e['modifier'] * 100)}%",
            "maximum-following-robots-count": lambda e: f"战斗无人机跟随上限 +{e['modifier']}",
            "stack-inserter-capacity-bonus": lambda e: f"集装机械臂搬运量 +{e['modifier']}",
            "inserter-stack-size-bonus": lambda e: f"常规机械臂搬运量 +{e['modifier']}",
            "ghost-time-to-live": lambda e: f"设施规划重建时限 +{int(e['modifier'] / 216000)}h",
            "character-logistic-requests": lambda e: f"解锁背包物流需求区",
            "character-logistic-trash-slots": lambda e: f"背包物流回收区 +{e['modifier']}",
            "mining-drill-productivity-bonus": lambda e: f"采矿产能 +{int(e['modifier'] * 100)}%",
            "laboratory-speed": lambda e: f"研究中心研发速度 +{int(e['modifier'] * 100)}%",
            "character-mining-speed": lambda e: f"人工采矿速度 +{int(e['modifier'] * 100)}%",
            "character-inventory-slots-bonus": lambda e: f"背包容量 +{e['modifier']}",
            "turret-attack": lambda e: turret_id_dict[e["turret_id"]] + f" +{e['modifier']}",
        }
        return effects_dict

    def item2zh(self, in_name):
        if in_name in ["solid-fuel-from-light-oil", "solid-fuel-from-heavy-oil", "solid-fuel-from-petroleum-gas"]:
            in_name = "solid-fuel"
        if in_name in self.base_cfg['item-name']:
            return self.base_cfg['item-name'][in_name]
        if in_name in self.base_cfg['entity-name']:
            return self.base_cfg['entity-name'][in_name]
        if in_name in self.base_cfg['recipe-name']:
            return self.base_cfg['recipe-name'][in_name]
        if in_name in self.base_cfg['equipment-name']:
            return self.base_cfg['equipment-name'][in_name]
        if in_name in self.base_cfg['fluid-name']:
            return self.base_cfg['fluid-name'][in_name]
        if in_name in self.base_cfg['recipe-name']:
            return self.base_cfg['recipe-name'][in_name]
        raise ValueError(f"can not find name {in_name}")


def check_infinite(name: str, tech_names: list, tech_data):
    # tech_inside_names
    names = name.split("-")
    if not names[-1].isnumeric():
        return False

    i = 1
    while name.replace(names[-1], str(i + 1)) in tech_names:
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

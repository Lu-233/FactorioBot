"""
 gen nav
"""
from game_info.tech_data import tech_dict, tech_group_dict


def main():

    tech_nav = "<noinclude>{{面包屑|导航|科技}}</noinclude>" + "\n" \
               "{{导航盒" + "\n" \
               "|名称= 模板:科技导航" + "\n" \
               "|标题= 科技" + "\n" \
               "|折叠 = uncollapsed" + "\n"

    for cls, techs in tech_dict.items():
        group_name = tech_group_dict[cls]
        tech_nav += f"\n"
        tech_nav += f"|分组{cls} = {group_name}" + "\n"
        tech_nav += f"|列表{cls} = " + "\n"
        for tech in techs:
            title: str = tech[1]
            show_title = ""
            if title.endswith("MK2"):
                show_title = "MK2"
            elif title.endswith("2"):
                show_title = "2"
            elif title.endswith("3"):
                show_title = "3"
            elif title.endswith("4"):
                show_title = "4"

            if show_title:
                tech_nav += "**[[科技-" + title + "|" + show_title + "]]" + "\n"
            else:
                # {{图标|科技-电能储存||科技:电能储存|16|frame=none}}
                tech_nav += "*{{图标|科技-" + title + "||科技:" + title + "|16|frame=none}}"
                tech_nav += "[[科技:" + title + "|" + title + "]]" + "\n"
                # tech_nav += "*[[" + title + "|" + title + "]]" + "\n"
            # if show_title:
            #     tech_nav += "**[[" + tech[3] + "|" + show_title + "]]" + "\n"
            # else:
            #     tech_nav += "*{{I|" + tech[3] + "|" + title + "}}" + "\n"
    tech_nav += "\n"
    tech_nav += "|分组10 = [[模板:物品配方|导航]]" + "\n"
    tech_nav += "|列表10 =" + "\n"
    tech_nav += "* [[模板:物流导航|物流]]" + "\n"
    tech_nav += "* [[模板:生产导航|生产]]" + "\n"
    tech_nav += "* [[模板:零件导航|零件]]" + "\n"
    tech_nav += "* [[模板:武器导航|武器]]" + "\n"
    tech_nav += "* [[模板:科技导航|科技]]" + "\n"
    tech_nav += "" + "\n"
    tech_nav += "}}<noinclude>{{文献资料}}</noinclude>" + "\n"
    print(tech_nav)


if __name__ == '__main__':
    main()
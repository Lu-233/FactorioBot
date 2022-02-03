import json
from pathlib import Path

from game_info.data_loader import load_base_cfg
from game_info.item_data import item2zh
from script_bili.BiliTool import get_items_dict, get_items

from tool.wiki import get_bili_tool as get_tool
import shutil

def main2():
    icon_path = Path(r"C:\Game\Java-Factorio-Data-Wrapper\FactorioDataWrapper\output\icons")

    lang_dict = get_en2zh()
    print(lang_dict)
    for icon_file in icon_path.iterdir():
        if not icon_file.is_file():
            continue
        item_name = icon_file.name.replace(".png","")
        item_name = lang_dict[item_name]
        if item_name.endswith(" 1") or item_name.endswith(" 2") or item_name.endswith(" 3"):
            item_name = item_name.replace(" ", "")

        new_file = Path(r"z:/items") / f"{item_name}.png"
        print(icon_file.name,"\t",new_file.name)
        shutil.copy(icon_file, new_file)


def get_en2zh():
    data = {}
    items_str = Path("../game_info/game_data/items.txt").read_text("UTF8")
    items = items_str.split("\n")

    base_cfg_en = load_base_cfg(lang="en")
    base_cfg = load_base_cfg()
    for it in items:
        if it in black_list:
            continue
        if it.startswith("spidertron-rocket-launcher"):
            it = "spidertron-rocket-launcher"
        data[item2zh(it, base_cfg_en)] = item2zh(it, base_cfg)
    """
    advanced-oil-processing=高等原油处理
    basic-oil-processing=基础原油处理
    coal-liquefaction=煤炭液化
    empty-crude-oil-barrel=倒出原油
    empty-filled-barrel=倾倒__1__桶
    fill-barrel=灌装__1__桶
    fill-crude-oil-barrel=灌装原油
    heavy-oil-cracking=重油裂解
    kovarex-enrichment-process=铀增殖处理
    light-oil-cracking=轻油裂解
    nuclear-fuel-reprocessing=乏燃料后处理
    uranium-processing=铀浓缩处理
    """
    data["Advanced"] = "高等"
    data["Advanced"] = "高等"
    data["Advanced"] = "高等"
    data["Advanced"] = "高等"
    data["Advanced"] = "高等"
    data["Used up uranium fuel cell"] = "乏燃料棒"

    data["Uranium processing"] = "铀浓缩处理"
    data["Solid fuel from petroleum gas"] = "固体燃料(石油气配方)"
    data["Solid fuel from light oil"] = "固体燃料(轻油配方)"
    data["Solid fuel from heavy oil"] = "固体燃料(重油配方)"
    data["Nuclear fuel reprocessing"] = "乏燃料后处理"
    data["Light oil cracking"] = "轻油裂解"
    data["Kovarex enrichment process"] = "铀增殖处理"
    data["Heavy oil cracking"] = "重油裂解"

    data["Water barrel"] = "水桶"
    data["Sulfuric acid barrel"] = "硫酸桶"
    data["Petroleum gas barrel"] = "石油气桶"
    data["Lubricant barrel"] = "润滑油桶"
    data["Light oil barrel"] = "轻油桶"
    data["Heavy oil barrel"] = "重油桶"
    data["Crude oil barrel"] = "原油桶"

    data["Fill water barrel"] = "灌装水桶"
    data["Fill sulfuric acid barrel"] = "灌装硫酸桶"
    data["Fill petroleum gas barrel"] = "灌装石油气桶"
    data["Fill lubricant barrel"] = "灌装润滑油桶"
    data["Fill light oil barrel"] = "灌装轻油桶"
    data["Fill heavy oil barrel"] = "灌装重油桶"
    data["Fill crude oil barrel"] = "灌装原油桶"

    data["Empty water barrel"] = "倾倒水桶"
    data["Empty sulfuric acid barrel"] = "倾倒硫酸桶"
    data["Empty petroleum gas barrel"] = "倾倒石油气桶"
    data["Empty lubricant barrel"] = "倾倒润滑油桶"
    data["Empty light oil barrel"] = "倾倒轻油桶"
    data["Empty heavy oil barrel"] = "倾倒重油桶"
    data["Empty crude oil barrel"] = "倾倒原油桶"
    data["Advanced oil processing"] = "高等原油处理"
    data["Basic oil processing"] = "基础原油处理"
    data["Coal liquefaction"] = "煤炭液化"
    data["Crude oil"] = "原油"
    data["Heavy oil"] = "重油"
    data["Light oil"] = "轻油"
    data["Lubricant"] = "润滑油"
    data["Petroleum gas"] = "石油气"
    data["Steam"] = "蒸汽"
    data["Sulfuric acid"] = "硫酸"
    data["Water"] = "水"
    return data

black_list = [
    "dummy-steel-axe",
    "heavy-oil-barrel",
    "light-oil-barrel",
    "lubricant-barrel",
    "petroleum-gas-barrel",
    "sulfuric-acid-barrel",
    "water-barrel",
    "item-unknown",
    "",
]


def main():

    wiki = get_tool()
    pages = get_items(wiki)
    for p in pages:
        # print(p["pageid"], p["title"])
        # print(get_new_name(p["title"]))

        title:str = p["title"]

        if title.startswith("物品"):
            continue

        new_name = get_new_name(p["title"])
        # content: str = wiki.page_info(p["pageid"])["*"]
        print(p["title"], ">", "重定向")

        content = f"#重定向 [[{new_name}]]" + "\n"
        content += '<br>' + "\n"
        content += "'''注意：'''" + "\n"
        content += f"'''{title}'''页面仅用于重定向。" + "\n"
        content += '' + "\n"
        content += f'读者、编者请直接访问：[[{new_name}]]。' + "\n"
        content += '<!-- 本页是自动生成的重定向页面，非必要勿编辑，除非你知道你在做什么。 -->' + "\n"

        token = wiki.edit_token()
        res = wiki.session.post(wiki.api_url, data={
            'format': 'json',
            'action': 'edit',
            'title': title,
            'text': content,
            'summary': f'bot: 标记重定向，重定向到新物品页面：{new_name}。',
            'bot': True,
            'token': token,
        })
        print(json.dumps(res.json(), ensure_ascii=False))


def get_new_name(name: str):
    if name == "灯":
        name = "照明灯"
    if name.endswith(" 1") or name.endswith(" 2") or name.endswith(" 3"):
        name = name.replace(" ", "")
    return "物品:"+name


"""
创建重定向页面
物品:灯 > 物品:照明灯
物品:产能插件 1 > 物品:产能插件1
物品:产能插件 2 > 物品:产能插件2
物品:产能插件 3 > 物品:产能插件3
物品:节能插件 1 > 物品:节能插件1
物品:节能插件 2 > 物品:节能插件2
物品:节能插件 3 > 物品:节能插件3
物品:速度插件 1 > 物品:速度插件1
物品:速度插件 2 > 物品:速度插件2
物品:速度插件 3 > 物品:速度插件3
物品:主动供货箱 > 物品:主动供货箱 (紫箱)
物品:紫箱 > 物品:主动供货箱 (紫箱)
物品:主动存货箱 > 物品:主动存货箱 (绿箱)
物品:绿箱 > 物品:主动存货箱 (绿箱)
物品:优先集货箱 > 物品:优先集货箱 (蓝箱)
物品:蓝箱 > 物品:优先集货箱 (蓝箱)
物品:军备研究包 > 物品:军备研究包 (灰瓶)
物品:灰瓶 > 物品:军备研究包 (灰瓶)
物品:化工研究包 > 物品:化工研究包 (蓝瓶)
物品:蓝瓶 > 物品:化工研究包 (蓝瓶)
物品:太空研究包 > 物品:太空研究包 (白瓶)
物品:白瓶 > 物品:太空研究包 (白瓶)
物品:效能研究包 > 物品:效能研究包 (黄瓶)
物品:黄瓶 > 物品:效能研究包 (黄瓶)
物品:机自研究包 > 物品:机自研究包 (红瓶)
物品:红瓶 > 物品:机自研究包 (红瓶)
物品:物流研究包 > 物品:物流研究包 (绿瓶)
物品:绿瓶 > 物品:物流研究包 (绿瓶)
物品:生产研究包 > 物品:生产研究包 (紫瓶)
物品:紫瓶 > 物品:生产研究包 (紫瓶)
物品:红图 > 物品:红图 (拆除规划)
物品:拆除规划 > 物品:红图 (拆除规划)
物品:绿图 > 物品:绿图 (升级规划)
物品:升级规划 > 物品:绿图 (升级规划)
物品:蓝图 > 物品:蓝图 (建设规划)
物品:建设规划 > 物品:蓝图 (建设规划)
物品:被动供货箱 > 物品:被动供货箱 (红箱)
物品:红箱 > 物品:被动供货箱 (红箱)
物品:被动存货箱 > 物品:被动存货箱 (黄箱)
物品:黄箱 > 物品:被动存货箱 (黄箱)
中型电线杆 > 物品:中型电线杆
主动供货箱 (紫箱) > 物品:主动供货箱 (紫箱)
主动存货箱 (绿箱) > 物品:主动存货箱 (绿箱)
乏燃料后处理 > 物品:乏燃料后处理
乏燃料棒 > 物品:乏燃料棒
产能插件 1 > 物品:产能插件1
产能插件 2 > 物品:产能插件2
产能插件 3 > 物品:产能插件3
优先集货箱 (蓝箱) > 物品:优先集货箱 (蓝箱)
供水泵 > 物品:供水泵
修理包 > 物品:修理包
储液罐 > 物品:储液罐
内燃机 > 物品:内燃机
内燃机车 > 物品:内燃机车
军备研究包 (灰瓶) > 物品:军备研究包 (灰瓶)
冲锋枪 > 物品:冲锋枪
冲锋霰弹枪 > 物品:冲锋霰弹枪
减速胶囊 > 物品:减速胶囊
判断运算器 > 物品:判断运算器
剧毒胶囊 > 物品:剧毒胶囊
加长机械臂 > 物品:加长机械臂
化工厂 > 物品:化工厂
化工研究包 (蓝瓶) > 物品:化工研究包 (蓝瓶)
卫星 > 物品:卫星
原子火箭弹 > 物品:原子火箭弹
原油 > 物品:原油
原油桶 > 物品:原油桶
固体燃料 > 物品:固体燃料
地下管道 > 物品:地下管道
地雷 > 物品:地雷
坦克 > 物品:坦克
基础传送带 > 物品:基础传送带
基础分流器 > 物品:基础分流器
基础地下传送带 > 物品:基础地下传送带
塑料 > 物品:塑料
填海料 > 物品:填海料
墙壁 > 物品:墙壁
处理器 > 物品:处理器
外骨骼模块 > 物品:外骨骼模块
夜视模块 > 物品:夜视模块
太空研究包 (白瓶) > 物品:太空研究包 (白瓶)
太阳能板 > 物品:太阳能板
太阳能模块 > 物品:太阳能模块
小型电线杆 > 物品:小型电线杆
常规铁路信号 > 物品:常规铁路信号
常量运算器 > 物品:常量运算器
广域配电站 > 物品:广域配电站
建设机器人 > 物品:建设机器人
悬崖炸药 > 物品:悬崖炸药
手枪 > 物品:手枪
抽油机 > 物品:抽油机
换热器 > 物品:换热器
掩护无人机胶囊 > 物品:掩护无人机胶囊
插件效果分享塔 > 物品:插件效果分享塔
放电防御模块 > 物品:放电防御模块
放电防御瞄准器 > 物品:放电防御瞄准器
效能研究包 (黄瓶) > 物品:效能研究包 (黄瓶)
木制箱 > 物品:木制箱
木材 > 物品:木材
机器人指令平台 > 物品:机器人指令平台
机器人指令模块 > 物品:机器人指令模块
机器人指令模块MK2 > 物品:机器人指令模块MK2
机器人构架 > 物品:机器人构架
机枪炮塔 > 物品:机枪炮塔
机自研究包 (红瓶) > 物品:机自研究包 (红瓶)
极速传送带 > 物品:极速传送带
极速分流器 > 物品:极速分流器
极速地下传送带 > 物品:极速地下传送带
标准弹匣 > 物品:标准弹匣
标准手雷 > 物品:标准手雷
标准混凝土 > 物品:标准混凝土
标准混凝土 (标识) > 物品:标准混凝土 (标识)
标准火箭弹 > 物品:标准火箭弹
标准炮弹 > 物品:标准炮弹
标准霰弹 > 物品:标准霰弹
核反应堆 > 物品:核反应堆
核能燃料 > 物品:核能燃料
模块装甲 > 物品:模块装甲
水 > 物品:水
水桶 > 物品:水桶
汽车 > 物品:汽车
汽轮机 > 物品:汽轮机
油料储罐 > 物品:油料储罐
润滑油 > 物品:润滑油
润滑油桶 > 物品:润滑油桶
液罐车厢 > 物品:液罐车厢
激光炮塔 > 物品:激光炮塔
激光防御模块 > 物品:激光防御模块
火焰喷射器 > 物品:火焰喷射器
火焰炮塔 > 物品:火焰炮塔
火箭发射井 > 物品:火箭发射井
火箭控制器 > 物品:火箭控制器
火箭燃料 > 物品:火箭燃料
火箭筒 > 物品:火箭筒
火箭组件 > 物品:火箭组件
火车站 > 物品:火车站
灯 > 物品:照明灯
炸药 > 物品:炸药
炼油厂 > 物品:炼油厂
热管 > 物品:热管
热能机械臂 > 物品:热能机械臂
热能采矿机 > 物品:热能采矿机
煤矿 > 物品:煤矿
爆破火箭弹 > 物品:爆破火箭弹
爆破炮弹 > 物品:爆破炮弹
爆破贫铀炮弹 > 物品:爆破贫铀炮弹
物流机器人 > 物品:物流机器人
物流研究包 (绿瓶) > 物品:物流研究包 (绿瓶)
生产研究包 (紫瓶) > 物品:生产研究包 (紫瓶)
电力机械臂 > 物品:电力机械臂
电力采矿机 > 物品:电力采矿机
电动机 > 物品:电动机
电池 > 物品:电池
电池组模块 > 物品:电池组模块
电池组模块MK2 > 物品:电池组模块MK2
电炉 > 物品:电炉
电路板 > 物品:电路板
电闸 > 物品:电闸
石油气 > 物品:石油气
石油气桶 > 物品:石油气桶
石炉 > 物品:石炉
石矿 > 物品:石矿
石砖 > 物品:石砖
研究中心 > 物品:研究中心
硫磺 > 物品:硫磺
硫酸 > 物品:硫酸
硫酸桶 > 物品:硫酸桶
离心机 > 物品:离心机
程控扬声器 > 物品:程控扬声器
空桶 > 物品:空桶
穿甲弹匣 > 物品:穿甲弹匣
穿甲霰弹 > 物品:穿甲霰弹
筛选机械臂 > 物品:筛选机械臂
算术运算器 > 物品:算术运算器
管道 > 物品:管道
管道泵 > 物品:管道泵
红图 (拆除规划) > 物品:红图 (拆除规划)
红线缆 > 物品:红线缆
组装机1型 > 物品:组装机1型
组装机2型 > 物品:组装机2型
组装机3型 > 物品:组装机3型
绿图 (升级规划) > 物品:绿图 (升级规划)
绿线缆 > 物品:绿线缆
联锁铁路信号 > 物品:联锁铁路信号
聚变堆模块 > 物品:聚变堆模块
能量盾模块 > 物品:能量盾模块
能量盾模块MK2 > 物品:能量盾模块MK2
能量装甲 > 物品:能量装甲
能量装甲MK2 > 物品:能量装甲MK2
节能插件 1 > 物品:节能插件1
节能插件 2 > 物品:节能插件2
节能插件 3 > 物品:节能插件3
蒸汽 > 物品:蒸汽
蒸汽机 > 物品:蒸汽机
蓄电器 > 物品:蓄电器
蓝图 (建设规划) > 物品:蓝图 (建设规划)
蓝图簿 > 物品:蓝图簿
被动供货箱 (红箱) > 物品:被动供货箱 (红箱)
被动存货箱 (黄箱) > 物品:被动存货箱 (黄箱)
货运车厢 > 物品:货运车厢
贫铀弹匣 > 物品:贫铀弹匣
贫铀炮弹 > 物品:贫铀炮弹
轻型护甲 > 物品:轻型护甲
轻油 > 物品:轻油
轻油桶 > 物品:轻油桶
轻质框架 > 物品:轻质框架
进攻无人机胶囊 > 物品:进攻无人机胶囊
远程输电塔 > 物品:远程输电塔
速度插件 1 > 物品:速度插件1
速度插件 2 > 物品:速度插件2
速度插件 3 > 物品:速度插件3
重型护甲 > 物品:重型护甲
重油 > 物品:重油
重油桶 > 物品:重油桶
重炮炮塔 > 物品:重炮炮塔
重炮炮弹 > 物品:重炮炮弹
重炮袭击瞄准器 > 物品:重炮袭击瞄准器
重炮车厢 > 物品:重炮车厢
钢制箱 > 物品:钢制箱
钢材 > 物品:钢材
钢炉 > 物品:钢炉
钢筋混凝土 > 物品:钢筋混凝土
钢筋混凝土 (标识) > 物品:钢筋混凝土 (标识)
铀-235 > 物品:铀-235
铀-238 > 物品:铀-238
铀增殖处理 > 物品:铀增殖处理
铀浓缩处理 > 物品:铀浓缩处理
铀燃料棒 > 物品:铀燃料棒
铀矿 > 物品:铀矿
铁制箱 > 物品:铁制箱
铁板 > 物品:铁板
铁棒 > 物品:铁棒
铁矿 > 物品:铁矿
铁轨 > 物品:铁轨
铁齿轮 > 物品:铁齿轮
铜板 > 物品:铜板
铜矿 > 物品:铜矿
铜线 > 物品:铜线
锅炉 > 物品:锅炉
锚定模块 > 物品:锚定模块
闸门 > 物品:闸门
防御无人机胶囊 > 物品:防御无人机胶囊
集成电路 > 物品:集成电路
集束手雷 > 物品:集束手雷
集装机械臂 > 物品:集装机械臂
集装筛选机械臂 > 物品:集装筛选机械臂
雷达 > 物品:雷达
霰弹枪 > 物品:霰弹枪
高速传送带 > 物品:高速传送带
高速分流器 > 物品:高速分流器
高速地下传送带 > 物品:高速地下传送带
高速机械臂 > 物品:高速机械臂
鲜鱼 > 物品:鲜鱼
"""


if __name__ == '__main__':
    main()
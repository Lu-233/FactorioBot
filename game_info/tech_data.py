""" 科技信息，分区，中文，内部，英文 """
from collections import defaultdict

tech_group_dict = {
    "1": "机器",
    "2": "军工/武器",
    "3": "加成",
    "4": "玩家强化",
    "5": "防御",
    "6": "生产制造",
    "7": "交通运输",
    "8": "装备模块",
    "9": "插件",

}

tech_list = [
    ["1", "高等电学", "advanced-electronics", "Advanced electronics"],
    ["1", "高等电学2", "advanced-electronics-2", "Advanced electronics 2"],
    ["1", "自动化", "automation", "Automation"],
    ["1", "自动化2", "automation-2", "Automation 2"],
    ["1", "自动化3", "automation-3", "Automation 3"],
    ["1", "电能储存", "electric-energy-accumulators-1", "Electric energy accumulators"],
    ["1", "电能传输", "electric-energy-distribution-1", "Electric energy distribution"],
    ["1", "电能传输2", "electric-energy-distribution-2", "Electric energy distribution 2"],
    ["1", "高速机械臂", "fast-inserter", "Fast inserter"],
    ["1", "流体操作", "fluid-handling", "Fluid handling"],
    ["1", "物流学", "logistics", "Logistics"],
    ["1", "物流学2", "logistics-2", "Logistics 2"],
    ["1", "物流学3", "logistics-3", "Logistics 3"],
    ["1", "核能", "nuclear-power", "Nuclear power"],
    ["1", "基础原油处理", "oil-processing", "Oil processing"],
    ["1", "火箭发射井", "rocket-silo", "Rocket silo"],
    ["1", "太阳能", "solar-energy", "Solar energy"],
    ["1", "集装机械臂", "stack-inserter", "Stack inserter"],
    ["2", "原子弹", "atomic-bomb", "Atomic bomb"],
    ["2", "防御无人机", "defender", "Defender"],
    ["2", "进攻无人机", "destroyer", "Destroyer"],
    ["2", "掩护无人机", "distractor", "Distractor"],
    ["2", "爆破火箭弹", "explosive-rocketry", "Explosive rocketry"],
    ["2", "火焰喷射", "flamethrower", "Flamethrower"],
    ["2", "军工学", "military", "Military"],
    ["2", "军工学2", "military-2", "Military 2"],
    ["2", "军工学3", "military-3", "Military 3"],
    ["2", "军工学4", "military-4", "Military 4"],
    ["2", "火箭弹", "rocketry", "Rocketry"],
    ["2", "贫铀弹", "uranium-ammo", "Uranium ammo"],
    ["3", "重炮炮弹射程", "artillery-shell-range-1", "Artillery shell range"],
    ["3", "重炮炮弹射速", "artillery-shell-speed-1", "Artillery shell shooting speed"],
    ["3", "制动技术", "braking-force-1", "Braking force"],
    ["3", "能量武器伤害", "energy-weapons-damage-1", "Energy weapons damage"],
    ["3", "无人机跟随数量", "follower-robot-count-1", "Follower robot count"],
    ["3", "机械臂搬运量加成", "inserter-capacity-bonus-1", "Inserter capacity bonus"],
    ["3", "激光射速", "laser-shooting-speed-1", "Laser shooting speed"],
    ["3", "采矿产能", "mining-productivity-1", "Mining productivity"],
    ["3", "动能武器伤害", "physical-projectile-damage-1", "Physical projectile damage"],
    ["3", "精炼燃料制备", "refined-flammables-1", "Refined flammables"],
    ["3", "研究中心研发速度", "research-speed-1", "Lab research speed"],
    ["3", "烈性炸药", "stronger-explosives-1", "Stronger explosives"],
    ["3", "动能武器射速", "weapon-shooting-speed-1", "Weapon shooting speed"],
    ["3", "作业机器人移动速度", "worker-robots-speed-1", "Worker robot speed"],
    ["3", "作业机器人货物运量", "worker-robots-storage-1", "Worker robot cargo size"],
    ["4", "建设机器人", "construction-robotics", "Construction robotics"],
    ["4", "物流机器人", "logistic-robotics", "Logistic robotics"],
    ["4", "钢斧镐", "steel-axe", "Steel axe"],
    ["4", "工具腰带", "toolbelt", "Toolbelt"],
    ["5", "重型火炮", "artillery", "Artillery"],
    ["5", "闸门", "gate", "Gate"],
    ["5", "机枪炮塔", "gun-turret", "Gun turret"],
    ["5", "重型护甲", "heavy-armor", "Heavy armor"],
    ["5", "地雷", "land-mine", "Land mines"],
    ["5", "激光炮塔", "laser-turret", "Laser turret"],
    ["5", "模块装甲", "modular-armor", "Modular armor"],
    ["5", "能量装甲", "power-armor", "Power armor"],
    ["5", "能量装甲MK2", "power-armor-mk2", "Power armor MK2"],
    ["5", "石墙", "stone-wall", "Stone wall"],
    ["6", "高等冶炼技术", "advanced-material-processing", "Advanced material processing"],
    ["6", "高等冶炼技术2", "advanced-material-processing-2", "Advanced material processing 2"],
    ["6", "高等原油处理", "advanced-oil-processing", "Advanced oil processing"],
    ["6", "电池", "battery", "Battery"],
    ["6", "化工研究包 (蓝瓶)", "chemical-science-pack", "Chemical science pack"],
    ["6", "信号网络", "circuit-network", "Circuit network"],
    ["6", "悬崖炸药", "cliff-explosives", "Cliff explosives"],
    ["6", "煤炭液化", "coal-liquefaction", "Coal liquefaction"],
    ["6", "混凝土", "concrete", "Concrete"],
    ["6", "电动机", "electric-engine", "Electric engine"],
    ["6", "基础电学", "electronics", "Electronics"],
    ["6", "内燃机", "engine", "Engine"],
    ["6", "炸药", "explosives", "Explosives"],
    ["6", "燃料制备", "flammables", "Flammables"],
    ["6", "铀增殖处理", "kovarex-enrichment-process", "Kovarex enrichment process"],
    ["6", "填海料", "landfill", "Landfill"],
    ["6", "激光", "laser", "Laser"],
    ["6", "物流研究包 (绿瓶)", "logistic-science-pack", "Logistic science pack"],
    ["6", "物流系统", "logistic-system", "Logistic system"],
    ["6", "轻质框架", "low-density-structure", "Low density structure"],
    ["6", "润滑油", "lubricant", "Lubricant"],
    ["6", "军备研究包 (灰瓶)", "military-science-pack", "Military science pack"],
    ["6", "乏燃料后处理", "nuclear-fuel-reprocessing", "Nuclear fuel reprocessing"],
    ["6", "基础光学", "optics", "Optics"],
    ["6", "塑料", "plastics", "Plastics"],
    ["6", "生产研究包 (紫瓶)", "production-science-pack", "Production science pack"],
    ["6", "机器人技术", "robotics", "Robotics"],
    ["6", "火箭控制器", "rocket-control-unit", "Rocket control unit"],
    ["6", "火箭燃料", "rocket-fuel", "Rocket fuel"],
    ["6", "太空研究包 (白瓶)", "space-science-pack", "Space science pack"],
    ["6", "炼钢技术", "steel-processing", "Steel processing"],
    ["6", "硫磺", "sulfur-processing", "Sulfur processing"],
    ["6", "铀浓缩处理", "uranium-processing", "Uranium processing"],
    ["6", "效能研究包 (黄瓶)", "utility-science-pack", "Utility science pack"],
    ["7", "铁路自动运输系统", "automated-rail-transportation", "Automated rail transportation"],
    ["7", "汽车", "automobilism", "Automobilism"],
    ["7", "液罐车厢", "fluid-wagon", "Fluid wagon"],
    ["7", "铁路信号", "rail-signals", "Rail signals"],
    ["7", "铁路", "railway", "Railway"],
    ["7", "蜘蛛机甲", "spidertron", "Spidertron"],
    ["7", "坦克", "tank", "Tank"],
    ["8", "电池组模块", "battery-equipment", "Personal battery"],
    ["8", "电池组模块MK2", "battery-mk2-equipment", "Personal battery MK2"],
    ["8", "锚定模块", "belt-immunity-equipment", "Belt immunity equipment"],
    ["8", "放电防御模块", "discharge-defense-equipment", "Discharge defense"],
    ["8", "能量盾模块", "energy-shield-equipment", "Energy shield equipment"],
    ["8", "能量盾模块MK2", "energy-shield-mk2-equipment", "Energy shield MK2 equipment"],
    ["8", "外骨骼模块", "exoskeleton-equipment", "Exoskeleton equipment"],
    ["8", "聚变堆模块", "fusion-reactor-equipment", "Portable fusion reactor"],
    ["8", "夜视模块", "night-vision-equipment", "Nightvision equipment"],
    ["8", "激光防御模块", "personal-laser-defense-equipment", "Personal laser defense"],
    ["8", "机器人指令模块", "personal-roboport-equipment", "Personal roboport"],
    ["8", "机器人指令模块MK2", "personal-roboport-mk2-equipment", "Personal roboport MK2"],
    ["8", "太阳能模块", "solar-panel-equipment", "Portable solar panel"],
    ["9", "节能插件", "effectivity-module", "Efficiency module"],
    ["9", "节能插件2", "effectivity-module-2", "Efficiency module 2"],
    ["9", "节能插件3", "effectivity-module-3", "Efficiency module 3"],
    ["9", "插件效果分享", "effect-transmission", "Effect transmission"],
    ["9", "插件", "modules", "Modules"],
    ["9", "产能插件", "productivity-module", "Productivity module"],
    ["9", "产能插件2", "productivity-module-2", "Productivity module 2"],
    ["9", "产能插件3", "productivity-module-3", "Productivity module 3"],
    ["9", "速度插件", "speed-module", "Speed module"],
    ["9", "速度插件2", "speed-module-2", "Speed module 2"],
    ["9", "速度插件3", "speed-module-3", "Speed module 3"],
]


def get_tech_dict():
    data = defaultdict(list)
    for t in tech_list:
        data[t[0]].append(t)
    return data


tech_dict = get_tech_dict()


def tech2zh(name: str, pre_name="科技:") -> str:
    for line in tech_list:
        if name == line[2]:
            return pre_name + line[1]

    # try xx-3 > xx and xx-3 > xx-1
    names = name.split("-")
    if names[-1].isnumeric():
        name2 = name.replace(f"-{names[-1]}", "")

        # try xx
        for line in tech_list:
            if name2 == line[2]:
                return pre_name + line[1] + names[-1]

        # try xx-1
        name3 = name.replace(f"-{names[-1]}", "-1")

        for line in tech_list:
            if name3 == line[2]:
                return pre_name + line[1] + names[-1]
    # try xx-1
    name4 = name + "-1"

    for line in tech_list:
        if name4 == line[2]:
            return pre_name + line[1]

    raise ValueError(f"未知的物品名 {name}")

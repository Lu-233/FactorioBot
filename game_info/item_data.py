import json
from collections import OrderedDict
from pathlib import Path

from lupa import LuaRuntime



def item2zh(in_name, base_cfg):
    if in_name in ["solid-fuel-from-light-oil", "solid-fuel-from-heavy-oil", "solid-fuel-from-petroleum-gas"]:
        in_name = "solid-fuel"
    if in_name in base_cfg['item-name']:
        return base_cfg['item-name'][in_name]
    if in_name in base_cfg['entity-name']:
        return base_cfg['entity-name'][in_name]
    if in_name in base_cfg['recipe-name']:
        return base_cfg['recipe-name'][in_name]
    if in_name in base_cfg['equipment-name']:
        return base_cfg['equipment-name'][in_name]
    if in_name in base_cfg['fluid-name']:
        return base_cfg['fluid-name'][in_name]
    if in_name in base_cfg['recipe-name']:
        return base_cfg['recipe-name'][in_name]
    print(repr(in_name))
    raise ValueError(f"can not find name {in_name}")



"""
known key
    icon
    icons
    icon_size
    icon_mipmaps
    dark_background_icon
    pictures
    order
    type = item
    
    subgroup
    stack_size # 堆叠大小
    name 名称
    place_result
    place_as_tile
    placed_as_equipment_result
    flags = hidden     some
    fuel_category  chemical,nuclear
    fuel_value
    fuel_acceleration_multiplier
    fuel_top_speed_multiplier
    burnt_result
    rocket_launch_product
    wire_count = 1
    default_request_amount  1/5
    
    localised_description
        
"""


def main():

    # ammo 弹药相关


    raw: dict = get_data_raw()
    for k,v in raw.items():
        print(k)
    # for k,v in raw["explosion"].items():
    #     print(k)
    # Path("z:/data.json").write_text(json.dumps(raw,ensure_ascii=False,indent=4),encoding="UTF8")


def get_data_raw():
    lua = LuaRuntime()
    ver = "1.1.53"
    folder = ver.replace(".", "/")

    # like require "game_data/1/1/53/technology"

    data_path = Path(__file__).parent.parent / "game_info" / "game_data" / folder

    data_path = str(data_path).replace("\\","/")
    get_data = lua.eval(f"""
    function()
        package.path = "{data_path}/?.lua;" .. package.path 
        package.path = "{data_path}/core/lualib/?.lua;" .. package.path 
        
        package.path = "{data_path}/core/?.lua;" .. package.path 
        package.path = "{data_path}/__base__/?.lua;" .. package.path 
    """ + """
        function math.pow(a, b)
            return a ^ b
        end
        defines = {
            direction = {
              east = 2,
              north = 0,
              northeast = 1,
              northwest = 7,
              south = 4,
              southeast = 3,
              southwest = 5,
              west = 6
            },
            difficulty_settings = {
                recipe_difficulty = {
                    expensive = 1,
                    normal = 0
                },
                technology_difficulty = {
                    expensive = 1,
                    normal = 0
                }
            },
        }
        require "util"
        require "dataloader"
        
        -- require("prototypes.fonts")
        -- require("prototypes.noise-layers")
        -- require("prototypes.style")
        -- require("prototypes.utility-constants")
        -- require("prototypes.utility-sounds")
        -- require("prototypes.utility-sprites")
        -- require("prototypes.god-controller")
        -- require("prototypes.editor-controller")
        -- require("prototypes.spectator-controller")
        require("prototypes.noise-programs") -- + noise-expression
        -- require("prototypes.cursors")
        -- require("prototypes.unknown")

        
        -- require "core.data"
        
            -- require("prototypes.ambient-sounds")  -- 一小点声音
    -- require("prototypes.entity.factorio-logo")  -- logo物品 + tile + container
    -- require("prototypes.entity.entities")
    -- require("prototypes.entity.explosions") -- 爆炸相关，只添加 raw["explosion"]
    -- require("prototypes.entity.crash-site") -- 坠机现场 + custom-input fire 依赖entities
    -- require("prototypes.entity.mining-drill") -- 依赖 entities 加了mining-drill
            -- require("prototypes.particles") -- 看起来是碎片 + optimized-particle particle-source
            -- require("prototypes.entity.spitter-projectiles") -- 看起来是虫子攻击 + fire sticker stream
    -- require("prototypes.entity.resources")  -- + resource
        require("prototypes.entity.turrets") -- + ammo-turret、artillery-turret、corpse、electric-turret、explosion、fire、noise-expression、sticker、stream、turret
        -- require("prototypes.entity.enemies")
        -- require("prototypes.entity.trains")
        -- require("prototypes.entity.remnants")
        -- require("prototypes.entity.trees")
        -- require("prototypes.entity.smoke")
        -- require("prototypes.entity.flying-robots")
        -- require("prototypes.item")
        -- require("prototypes.item-groups")
        -- require("prototypes.recipe")
        -- require("prototypes.fluid")
        -- require("prototypes.signal")
        -- require("prototypes.tile.noise-layers")
        -- require("prototypes.autoplace-controls")
        -- require("prototypes.map-settings")
        -- require("prototypes.map-gen-presets")
        -- require("prototypes.tile.tiles")
        -- require("prototypes.decorative.decoratives")
        -- require("prototypes.damage-type")
        -- require("prototypes.categories.ammo-category")
        -- require("prototypes.categories.fuel-category")
        -- require("prototypes.categories.recipe-category")
        -- require("prototypes.categories.resource-category")
        -- require("prototypes.categories.module-category")
        -- require("prototypes.equipment-grid")
        -- require("prototypes.categories.equipment-category")
        -- require("prototypes.shortcuts")
        -- require("prototypes.trigger-target-types")
        -- require("prototypes.entity.projectiles")
        -- require("prototypes.entity.beams")
        -- require("prototypes.utility-sprites")
        -- require("prototypes.technology")
        -- require("prototypes.tips-and-tricks")
        -- require("prototypes.achievements")
        -- require("prototypes.entity.entities")
        -- require("prototypes.entity.explosions")
        -- require("prototypes.entity.projectiles")
        -- require("prototypes.entity.beams")
        -- require("prototypes.entity.turrets")
        -- require("prototypes.entity.enemies")
        -- require("prototypes.entity.mining-drill")
        -- require("prototypes.entity.fire")
        -- require("prototypes.entity.remnants")
        -- require("prototypes.entity.circuit-network")
        -- require("prototypes.entity.atomic-bomb")
        -- require("prototypes.entity.resources")
        -- require("prototypes.equipment") -- equipment
        
        -- require("prototypes.tutorials")
        -- require("prototypes.legacy.legacy-entities") -- smoke
        -- require("prototypes.custom-inputs")  -- 用户输入
        
        -- require "__base__.data"  
        -- require "__base__.data-updates"  
                          
        return data
    end
                """)
    data = get_data()

    from data_loader import table2dict
    raw = OrderedDict(sorted(table2dict(data["raw"]).items()))
    return raw


def rmkey(data, key):
    if key in data:
        del data[key]
    return data

if __name__ == '__main__':
    main()
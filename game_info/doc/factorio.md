
# 读取 Factorio 游戏数据

## 数据来源

- 游戏目录
  * 游戏目录下的data文件夹。
- github.com/wube/factorio-data
  * factorio-data项目保存了游戏所有版本的数据

## 汉化

有两个文件，
* data\base\locale\zh-CN\base.cfg
* data\core\locale\zh-CN\core.cfg

## 从lua中加载数据

可以用 lupa，在python中运行lua代码并返回python可处理的对象

```python
from lupa import LuaRuntime
lua = LuaRuntime()
# like require "game_data/1/1/53/technology"
get_data = lua.eval(f"""
                function()
                    require "game_data/1/1/53/dataloader"
                    require "game_data/1/1/53/util"
                    require "game_data/1/1/53/technology"
                    return data
                end
            """)
data: dict = get_data()["raw"]["technology"]
```

## 技术

数据格式的官方文档：https://wiki.factorio.com/Prototype/Technology

### icons, icon, icon_size : IconSpecification

图标

### name : str

如果名字以 -数 结尾，本地化时，会忽略数字。

### upgrade : bool

如果为True，技术将包含多个升级

写wiki时，需要只写一个

### enabled : bool

Default: true

### hidden : bool

Default: false

Hides the technology from the tech screen.

### visible_when_disabled : bool

Default: false

Controls whether the technology is shown in the tech GUI when it is disabled (enabled = false).

### unit : table(dict)

一系列键值对

count : uint64 : 需要多少个研究点，大于0。指定了count_formula则可能不指定它
count_formula : str : 公式，按BODMAS顺序执行
    
    +  Addition
    -  Subtraction
    *  Multiplication
    ^  Power, raise the preceding base number by the following exponent number
    ()  Brackets for order, supported nested brackets
    l or L  The current level of the technology
    Digits  Are treated as numbers
    .  Decimal point in number
    SPACE  Space characters are ignored

time : double : 每个研究点需要多少时间，在制作速度为 1 的实验室中是秒。

ingredients : table :  一个研究点需要的成分清单。 项目类型必须都是工具。

     ingredients =
      {
        {"automation-science-pack", 1},
        {"logistic-science-pack", 1},
        {"chemical-science-pack", 1},
        {"production-science-pack", 1},
        {"utility-science-pack", 1},
        {"space-science-pack", 1}
      },



### max_level : uint32 or str 

目前都是 infinite

默认值：与科技等级相同，不升级为0，升级为升级等级。
“infinite”表示无限技术，否则为 uint。


### prerequisites : table of string
    
前置科技列表

    prerequisites = {"explosives", "military-2"}

### effects : table of Types/ModifierPrototype

技术效果列表（在研究技术时应用）。

    {
      {
        type  = "unlock-recipe",
        recipe = "land-mine"
      }
    }

### 关于 ModifierPrototype

文档： https://wiki.factorio.com/Types/ModifierPrototype





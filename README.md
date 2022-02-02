# FactorioBot


自用wiki机器人。My bot to automate the wiki operations instead of me.

用于 Use for:

- 官方Wiki: wiki.factorio.com 
- Bilibili Wiki:  wiki.biligame.com/factorio 

## 已有功能

对 MediaWiki 的通用基础操作，/tool/wiki.py

基本设计： 
- 通用操作抽象到 tool
- 尽量缓存，缓存在 bili_data 和 data文件夹中
  - page_content/*.json 缓存所有页面信息，每个页面一个json，page_id当文件名
  - all_page.json 缓存所有页面列表
  - xx_page.json 缓存中英文页面列表
  - exclude_page_list.json 排除的文章列表
  - category_pages 缓存每个分类的页面列表。



### bilibili factorio wiki : script_bili

- bili_session.py 从浏览器的登录cookie获取登录session（biliwiki没有密码/邮件）
- S01: 更新需求列表。对标官方wiki的wanted page。``
- S02：计算物品信息的”施工中“状态，按类别统计数量，并输出需要施工的页面，输出更新”wiki施工进度“的wiki字符串
- S03：更新页面缓存，可以更新一个，也可以更新全部


### 官方 official wiki : script_official

- official_tool.py 登录，获取session
- S01: 页面列表
- S02：获取每个页面的类别和单词数量
- S03： 获取页面历史 【老代码】
- S04_1: 更新 exclude_page_list
- S04_2: 更新一个页面 【以前需要一堆代码，现在只要几行了】
- S04： 获取页面信息 【以前需要一堆代码，现在只要几行了】
- S05：对比页面更新时间
- S06：输出所有中文页面标题（用来检查翻译表是否需要增加）

### 数据读取、页面生成：game_info

- tech_data.py 读取所有科技
- gen_tech_nav 生成科技导航条（用于 bili. fact. wiki）

- gen_tech_icon.py 根据科技原型代码合成科技图标
- gen_tech_nav.py 生成科技导航栏，需要手动更新到页面
- gen_tech_page.py ！！生成科技页面，自动修改页面内容
- tech_data.py  科技数据，和相关处理如翻译
- tech_loader.py 解析游戏科技文件

## Plan

- 从factorio游戏读取物品信息和配方
- 完善科技页面
- 自动编辑页面
  - 按照手工计划添加节
- 修改所有物品页面，新标题为：物品:木箱，老页面重定向
- 添加现有的物品、科技英文名重定向




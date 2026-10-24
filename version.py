"""单一版本 / 程序名来源：界面标题、任务栏、关于信息、打包都从这里读，避免到处硬编码、版本漂移。

改版本只改这里一处；编辑器(webhost)、旧版工具(main/gui_app)均引用本模块。
"""

__version__ = "3.3.0"

# 程序名（面向用户的功能名，而非“节点编辑器”这种实现名）。
APP_NAME = "AoE4 Flow · 帝国时代 4 自动化助手"
PRODUCT_NAME = "AoE4 Flow"
LEGACY_APP_NAME = "AoE4 Flow · 经典出农工具"

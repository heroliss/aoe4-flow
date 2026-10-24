"""
启动 AoE4 Flow 帝国时代 4 自动化助手（LiteGraph.js + pywebview 可视化流程编辑器）。

    python run_editor.py [flow.json]   # 打开网页编辑器；不给位置参数则新建空白流程

诊断：设环境变量 AOE4_FLOW_EDITOR_DEBUG=1 可在网页编辑器中打开 WebView2 开发者工具。
"""
from __future__ import annotations

import argparse
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flow.core import Graph
import flow.nodes  # noqa: F401  注册全部节点


def main():
    from version import APP_NAME, __version__
    ap = argparse.ArgumentParser(description=f"{APP_NAME} v{__version__}：图像识别与输入操作的可视化流程")
    ap.add_argument("file", nargs="?", help="要打开的流程图 JSON")
    ap.add_argument("--no-elevate", action="store_true", help="以普通权限编辑（输入屏蔽不可用）")
    ap.add_argument("--version", action="version", version=f"AoE4 Flow {__version__}")
    args = ap.parse_args()

    # 输入屏蔽(BlockInput)需要管理员权限；非管理员则尝试自提升重启（成功则本进程退出）。
    # 用户拒绝 UAC 时带警告继续，编辑仍可用、仅“输入屏蔽”不生效。
    if args.no_elevate:
        os.environ["AOE4_FLOW_NO_ELEVATE"] = "1"
    from admin_util import ensure_admin_or_warn
    ensure_admin_or_warn()

    path = args.file if args.file and os.path.exists(args.file) else None
    graph = Graph.load(path) if path else None

    from flow.editor.webhost import launch
    launch(graph, path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ShinyHunter-AutoCapture - S2赛季异色精灵自动捕捉系统
入口文件：初始化各模块、启动状态机、注册热键
"""

import sys
import time
import threading
import yaml
import logging
from pathlib import Path

# 添加项目根目录到sys.path（确保能导入core和utils）
sys.path.insert(0, str(Path(__file__).parent))

from core.fsm.state_machine import StateMachine
from core.fsm.context import SharedContext
from utils.logger import setup_logger
from utils.hotkey_listener import HotkeyListener

def main():
    # 1. 加载配置
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 2. 设置日志
    logger = setup_logger(
        level=getattr(logging, config["log"]["level"].upper()),
        log_file=config["log"]["file"]
    )
    logger.info("ShinyHunter-AutoCapture 启动 (S2赛季)")

    # 3. 创建全局上下文（用于共享精灵列表、剩余球数等）
    ctx = SharedContext(config)

    # 4. 创建状态机，并注入配置和上下文
    fsm = StateMachine(config, ctx)

    # 5. 初始化热键监听
    hotkey = HotkeyListener(config)

    def on_start():
        logger.info("用户按下开始热键，启动自动捕捉流程")
        fsm.start()

    def on_stop():
        logger.info("用户按下停止热键，暂停自动捕捉流程")
        fsm.stop()

    def on_exit():
        logger.info("用户按下退出热键，程序即将退出")
        fsm.stop()
        sys.exit(0)

    hotkey.register_start_callback(on_start)
    hotkey.register_stop_callback(on_stop)
    hotkey.register_exit_callback(on_exit)
    hotkey.start()

    logger.info(f"热键已注册：开始={config['hotkeys']['start']}, 暂停={config['hotkeys']['stop']}, 退出={config['hotkeys']['exit']}")

    # 6. 主线程保持运行，等待热键或Ctrl+C
    try:
        while True:
            time.sleep(0.2)
            # 可选：每5秒打印一次状态（调试用）
            # if int(time.time()) % 5 == 0:
            #     logger.debug(f"当前状态: {fsm.current_state}")
    except KeyboardInterrupt:
        logger.info("收到Ctrl+C，退出程序")
        fsm.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号内容生成系统 - 主入口文件

这是应用程序的主入口点，负责初始化系统并启动GUI界面。

Author: Your Name
Date: 2025-07-17
Version: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入必要的模块
try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon
except ImportError:
    print("错误：未找到PyQt6库，请先安装：pip install PyQt6")
    sys.exit(1)

from config.settings import AppConfig
from utils.logger import setup_logging, get_logger
from ui.main_window import MainWindow


class WechatContentGenApp:
    """微信公众号内容生成系统主应用类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.app = None
        self.main_window = None
        self.logger = None
        
    def initialize(self):
        """初始化应用程序组件"""
        try:
            # 设置日志系统
            setup_logging()
            self.logger = get_logger(__name__)
            self.logger.info("正在启动微信公众号内容生成系统...")
            
            # 创建QApplication实例
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("微信公众号内容生成系统")
            self.app.setApplicationVersion("1.0.0")
            self.app.setOrganizationName("WechatContentGen")
            
            # 设置应用程序图标
            icon_path = PROJECT_ROOT / "assets" / "images" / "icons" / "app_icon.ico"
            if icon_path.exists():
                self.app.setWindowIcon(QIcon(str(icon_path)))
            
            # 设置高DPI支持
            self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
            
            # 加载应用程序配置
            config = AppConfig()
            
            # 创建主窗口
            self.main_window = MainWindow()
            
            self.logger.info("应用程序初始化完成")
            return True
            
        except Exception as e:
            error_msg = f"应用程序初始化失败: {str(e)}"
            print(error_msg)
            if self.logger:
                self.logger.error(error_msg, exc_info=True)
            
            # 显示错误对话框
            if self.app:
                QMessageBox.critical(None, "初始化错误", error_msg)
            
            return False
    
    def run(self):
        """运行应用程序"""
        if not self.initialize():
            return 1
        
        try:
            # 显示主窗口
            self.main_window.show()
            
            # 记录启动信息
            self.logger.info("应用程序启动成功，主窗口已显示")
            
            # 进入事件循环
            return self.app.exec()
            
        except Exception as e:
            error_msg = f"应用程序运行时错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            
            QMessageBox.critical(
                self.main_window if self.main_window else None,
                "运行时错误",
                error_msg
            )
            return 1
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.logger:
                self.logger.info("正在清理应用程序资源...")
            
            # 清理主窗口
            if self.main_window:
                self.main_window.cleanup()
                self.main_window = None
            
            # 清理应用程序
            if self.app:
                self.app.quit()
                self.app = None
                
            if self.logger:
                self.logger.info("应用程序资源清理完成")
                
        except Exception as e:
            print(f"清理资源时发生错误: {str(e)}")


def check_dependencies():
    """检查必要的依赖项"""
    missing_deps = []
    
    # 检查必要的Python包
    required_packages = [
        'PyQt6',
        'requests',
        'Pillow',
        'openai',
    ]
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing_deps.append(package)
    
    if missing_deps:
        print("错误：缺少以下必要依赖项：")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n请运行以下命令安装依赖项：")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    return True


def create_directories():
    """创建必要的目录结构"""
    directories = [
        "data/cache",
        "data/exports", 
        "data/user_data",
        "assets/images/icons",
        "assets/images/templates",
        "assets/fonts",
        "assets/audio",
        "assets/templates/article_templates",
        "assets/templates/layout_templates",
    ]
    
    for directory in directories:
        dir_path = PROJECT_ROOT / directory
        dir_path.mkdir(parents=True, exist_ok=True)


def main():
    """主函数"""
    print("微信公众号内容生成系统 v1.0.0")
    print("=" * 50)
    
    # 检查依赖项
    if not check_dependencies():
        return 1
    
    # 创建必要的目录
    create_directories()
    
    # 创建并运行应用程序
    app = WechatContentGenApp()
    
    try:
        exit_code = app.run()
        return exit_code
        
    except KeyboardInterrupt:
        print("\n用户中断，正在退出...")
        return 0
        
    except Exception as e:
        print(f"未处理的异常: {str(e)}")
        return 1
        
    finally:
        app.cleanup()


if __name__ == "__main__":
    # 设置异常处理
    sys.excepthook = lambda exc_type, exc_value, exc_tb: print(
        f"未捕获的异常: {exc_type.__name__}: {exc_value}"
    )
    
    # 运行主程序
    exit_code = main()
    sys.exit(exit_code)

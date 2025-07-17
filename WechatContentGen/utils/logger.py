"""
日志工具模块

提供统一的日志记录功能。
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

from config.settings import AppConfig


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        """格式化日志记录"""
        # 添加颜色
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}"
                f"{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        
        return super().format(record)


def setup_logging():
    """设置日志系统"""
    config = AppConfig()
    
    # 创建日志目录
    log_dir = config.PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # 日志文件路径
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 根日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.LOG_FILE_MAX_SIZE,
        backupCount=config.LOG_FILE_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # 记录启动信息
    logger = logging.getLogger(__name__)
    logger.info(f"日志系统初始化完成，日志文件：{log_file}")


def get_logger(name: str = None) -> logging.Logger:
    """获取日志器实例
    
    Args:
        name: 日志器名称，通常使用 __name__
        
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)


class LoggerMixin:
    """日志器混入类"""
    
    @property
    def logger(self) -> logging.Logger:
        """获取当前类的日志器"""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")


# 便捷函数
def debug(msg, *args, **kwargs):
    """记录调试信息"""
    get_logger().debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """记录信息"""
    get_logger().info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """记录警告"""
    get_logger().warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """记录错误"""
    get_logger().error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """记录严重错误"""
    get_logger().critical(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """记录异常"""
    get_logger().exception(msg, *args, **kwargs)

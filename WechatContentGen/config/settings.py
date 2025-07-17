"""
应用程序主配置文件

包含应用程序的所有配置项。
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

class AppConfig:
    """应用程序配置类"""
    
    # 应用程序基本信息
    APP_NAME = "微信公众号内容生成系统"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "WechatContentGen Team"
    
    # 窗口配置
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    
    # 主题配置
    DEFAULT_THEME = "light"
    AVAILABLE_THEMES = ["light", "dark", "auto"]
    
    # 文件路径配置
    DATA_DIR = PROJECT_ROOT / "data"
    CACHE_DIR = DATA_DIR / "cache"
    EXPORTS_DIR = DATA_DIR / "exports"
    USER_DATA_DIR = DATA_DIR / "user_data"
    
    ASSETS_DIR = PROJECT_ROOT / "assets"
    IMAGES_DIR = ASSETS_DIR / "images"
    FONTS_DIR = ASSETS_DIR / "fonts"
    AUDIO_DIR = ASSETS_DIR / "audio"
    TEMPLATES_DIR = ASSETS_DIR / "templates"
    
    # 缓存配置
    CACHE_SIZE_MB = 100
    CACHE_EXPIRE_DAYS = 7
    
    # 内容生成配置
    MAX_CONTENT_LENGTH = 10000
    DEFAULT_LANGUAGE = "zh-CN"
    
    # 图片配置
    IMAGE_MAX_WIDTH = 1920
    IMAGE_MAX_HEIGHT = 1080
    IMAGE_QUALITY = 85
    SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    
    # 音频配置
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_BITRATE = 128
    SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".ogg"]
    
    # 导出配置
    EXPORT_FORMATS = ["html", "markdown", "docx", "pdf"]
    DEFAULT_EXPORT_FORMAT = "html"
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_FILE_BACKUP_COUNT = 5
    
    @classmethod
    def get_config_value(cls, key, default=None):
        """获取配置值"""
        return getattr(cls, key, default)
    
    @classmethod
    def update_config(cls, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

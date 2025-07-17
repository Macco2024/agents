# API 文档

## 核心模块 API

### ContentGenerator 类

内容生成器，负责生成文章内容。

#### 初始化

```python
from core.content_generator import ContentGenerator

generator = ContentGenerator(api_key="your_api_key", model="gpt-3.5-turbo")
```

#### 方法

##### generate_content()

生成文章内容。

**参数：**
- `topic` (str): 文章主题
- `style` (str, 可选): 写作风格，默认"专业"
- `length` (str, 可选): 文章长度，默认"中等"
- `keywords` (List[str], 可选): 关键词列表
- `outline` (bool, 可选): 是否生成大纲，默认True

**返回值：**
```python
{
    "title": "生成的标题",
    "outline": ["大纲项1", "大纲项2", ...],  # 如果outline=True
    "content": "生成的正文内容",
    "summary": "内容摘要"
}
```

**示例：**
```python
import asyncio

async def main():
    generator = ContentGenerator()
    result = await generator.generate_content(
        topic="人工智能的发展趋势",
        style="专业",
        length="中等",
        keywords=["AI", "机器学习", "深度学习"],
        outline=True
    )
    print(result["title"])
    print(result["content"])

asyncio.run(main())
```

### ImageGenerator 类

图片生成器，负责生成配图。

#### 初始化

```python
from core.image_generator import ImageGenerator

generator = ImageGenerator(api_key="your_api_key")
```

#### 方法

##### generate_image()

生成图片。

**参数：**
- `prompt` (str): 图片描述
- `style` (str, 可选): 图片风格
- `size` (str, 可选): 图片尺寸
- `quality` (str, 可选): 图片质量

**返回值：**
```python
{
    "image_path": "生成的图片路径",
    "thumbnail_path": "缩略图路径",
    "metadata": {
        "size": "1024x1024",
        "format": "PNG",
        "created_at": "2025-07-17T10:30:00"
    }
}
```

### VoiceGenerator 类

语音生成器，负责文本转语音。

#### 初始化

```python
from core.voice_generator import VoiceGenerator

generator = VoiceGenerator(api_key="your_api_key")
```

#### 方法

##### generate_voice()

生成语音。

**参数：**
- `text` (str): 要转换的文本
- `voice` (str, 可选): 语音类型
- `speed` (float, 可选): 语音速度
- `pitch` (float, 可选): 音调

**返回值：**
```python
{
    "audio_path": "生成的音频文件路径",
    "duration": 30.5,  # 音频时长（秒）
    "format": "mp3",
    "metadata": {
        "sample_rate": 44100,
        "bitrate": 128,
        "created_at": "2025-07-17T10:30:00"
    }
}
```

## UI 模块 API

### MainWindow 类

主窗口类，应用程序的主界面。

#### 信号

- `content_generated(str)`: 内容生成完成信号
- `image_generated(str)`: 图片生成完成信号
- `voice_generated(str)`: 语音生成完成信号

#### 方法

##### new_document()

创建新文档。

##### open_document()

打开文档。

##### save_document()

保存文档。

##### generate_content()

生成内容。

##### generate_image()

生成配图。

##### generate_voice()

生成语音。

## 工具模块 API

### Logger

日志工具。

#### 函数

##### get_logger(name)

获取日志器实例。

**参数：**
- `name` (str): 日志器名称

**返回值：**
- `logging.Logger`: 日志器实例

**示例：**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
```

##### setup_logging()

设置日志系统。

**示例：**
```python
from utils.logger import setup_logging

setup_logging()
```

## 配置模块 API

### AppConfig 类

应用程序配置类。

#### 类属性

- `APP_NAME`: 应用程序名称
- `APP_VERSION`: 应用程序版本
- `WINDOW_WIDTH`: 窗口宽度
- `WINDOW_HEIGHT`: 窗口高度
- `DEFAULT_THEME`: 默认主题

#### 方法

##### get_config_value(key, default)

获取配置值。

##### update_config(**kwargs)

更新配置。

## 错误处理

所有API方法都会返回包含错误信息的字典，当发生错误时：

```python
{
    "error": "错误描述",
    "error_code": "ERROR_CODE",
    "details": "详细错误信息"
}
```

## 异步支持

大部分生成功能都支持异步操作，使用 `async/await` 语法：

```python
import asyncio

async def generate_all():
    # 并发生成内容和图片
    content_task = generator.generate_content("AI发展")
    image_task = image_generator.generate_image("AI概念图")
    
    content_result, image_result = await asyncio.gather(
        content_task, 
        image_task
    )
    
    return content_result, image_result

# 运行异步函数
result = asyncio.run(generate_all())
```

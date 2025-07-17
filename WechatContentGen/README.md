# 微信公众号内容生成系统

一个现代化的微信公众号内容生成系统，集成智能文本生成、配图生成、语音输出和富文本预览功能。

## 功能特性

### 🤖 智能内容生成
- AI驱动的文章内容生成
- 多种写作风格和语调选择
- 关键词优化和SEO建议
- 自动标题生成

### 🎨 智能配图
- AI图片生成和编辑
- 图片风格转换
- 自动配图建议
- 图片尺寸优化

### 🔊 语音输出
- 文本转语音功能
- 多种语音风格选择
- 语音预览和编辑
- 音频格式导出

### 📝 富文本预览
- 实时富文本预览
- 微信公众号格式适配
- 多种排版模板
- 导出多种格式

## 系统要求

- Python 3.8+
- Windows 10/11
- 4GB+ RAM
- 网络连接（用于AI服务）

## 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd WechatContentGen
```

### 2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置API密钥
编辑 `config/api_keys.py` 文件，添加您的API密钥：
```python
# OpenAI API密钥
OPENAI_API_KEY = "your_openai_api_key"

# 其他服务API密钥
STABILITY_AI_KEY = "your_stability_ai_key"
ELEVENLABS_API_KEY = "your_elevenlabs_api_key"
```

## 快速开始

### 启动应用
```bash
python main.py
```

### 基本使用流程
1. **创建新文章**：点击"新建文章"按钮
2. **输入主题**：在主题输入框中输入文章主题
3. **生成内容**：点击"生成内容"，AI将自动生成文章
4. **添加配图**：使用"生成配图"功能添加相关图片
5. **语音输出**：选择文本片段，生成语音版本
6. **预览导出**：在富文本预览中查看最终效果，导出所需格式

## 项目结构

```
WechatContentGen/
├── core/           # 核心业务逻辑
├── ui/             # 用户界面
├── services/       # 外部服务接口
├── utils/          # 工具函数
├── assets/         # 静态资源
├── config/         # 配置文件
├── data/           # 数据目录
├── tests/          # 测试文件
└── docs/           # 文档
```

## 配置说明

### 主配置文件 (config/settings.py)
- 应用基本设置
- UI主题配置
- 缓存设置
- 导出格式配置

### API配置 (config/api_keys.py)
- OpenAI API配置
- 图片生成服务配置
- 语音合成服务配置

## 开发指南

### 环境设置
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest tests/

# 代码格式化
black .
flake8 .
```

### 添加新功能
1. 在 `core/` 目录下添加核心逻辑
2. 在 `ui/components/` 下添加UI组件
3. 在 `services/` 下添加外部服务接口
4. 编写相应的测试用例

## 常见问题

### Q: 如何更换AI服务提供商？
A: 修改 `services/ai_service.py` 中的服务接口实现。

### Q: 如何自定义文章模板？
A: 在 `assets/templates/article_templates/` 目录下添加新的模板文件。

### Q: 如何添加新的语音风格？
A: 在 `core/voice_generator.py` 中添加新的语音配置。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- 项目主页：<project-url>
- 问题反馈：<issues-url>
- 邮箱：<contact-email>

---

**注意**：使用本系统前请确保您已获得相关AI服务的使用许可，并遵守相应的服务条款。

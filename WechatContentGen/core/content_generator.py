"""
内容生成模块

负责生成文章内容的核心模块。
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple

from config.api_keys import OPENAI_API_KEY, OPENAI_MODEL
from utils.logger import get_logger


class ContentGenerator:
    """内容生成器类"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """初始化内容生成器
        
        Args:
            api_key: OpenAI API密钥，默认使用配置文件中的密钥
            model: 使用的模型名称，默认使用配置文件中的模型
        """
        self.logger = get_logger(__name__)
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_MODEL
        
        # 验证API密钥
        if not self.api_key:
            self.logger.warning("未配置API密钥，内容生成功能将不可用")
    
    async def generate_content(
        self, 
        topic: str, 
        style: str = "专业", 
        length: str = "中等", 
        keywords: List[str] = None,
        outline: bool = True
    ) -> Dict[str, Any]:
        """生成文章内容
        
        Args:
            topic: 文章主题
            style: 写作风格，如"专业"、"幽默"、"严肃"等
            length: 文章长度，如"短"、"中等"、"长"
            keywords: 需要包含的关键词列表
            outline: 是否生成大纲
            
        Returns:
            Dict: 包含生成内容的字典，格式如下：
                {
                    "title": "生成的标题",
                    "outline": ["大纲项1", "大纲项2", ...],  # 如果outline=True
                    "content": "生成的正文内容",
                    "summary": "内容摘要"
                }
        """
        self.logger.info(f"开始生成内容，主题：{topic}，风格：{style}，长度：{length}")
        
        if not self.api_key:
            self.logger.error("未配置API密钥，无法生成内容")
            return {
                "error": "未配置API密钥",
                "title": f"关于{topic}的文章",
                "content": "请先配置API密钥以启用内容生成功能。",
                "summary": "API密钥未配置"
            }
        
        try:
            # 构建提示词
            prompt = self._build_prompt(topic, style, length, keywords, outline)
            
            # 调用AI服务生成内容
            result = await self._call_ai_service(prompt)
            
            # 解析结果
            parsed_result = self._parse_result(result, outline)
            
            self.logger.info(f"内容生成成功，标题：{parsed_result.get('title', '未生成标题')}")
            return parsed_result
            
        except Exception as e:
            self.logger.exception(f"内容生成失败：{str(e)}")
            return {
                "error": str(e),
                "title": f"关于{topic}的文章",
                "content": f"内容生成失败：{str(e)}",
                "summary": "生成过程中出现错误"
            }
    
    def _build_prompt(
        self, 
        topic: str, 
        style: str, 
        length: str, 
        keywords: List[str] = None,
        outline: bool = True
    ) -> str:
        """构建提示词
        
        Args:
            topic: 文章主题
            style: 写作风格
            length: 文章长度
            keywords: 关键词列表
            outline: 是否生成大纲
            
        Returns:
            str: 构建的提示词
        """
        # 长度映射
        length_map = {
            "短": "500-800字",
            "中等": "1000-1500字",
            "长": "2000-3000字"
        }
        
        # 构建关键词部分
        keywords_text = ""
        if keywords and len(keywords) > 0:
            keywords_text = f"，并确保包含以下关键词：{', '.join(keywords)}"
        
        # 构建大纲部分
        outline_text = ""
        if outline:
            outline_text = "首先提供一个结构化的大纲，然后再生成完整内容。"
        
        # 构建完整提示词
        prompt = (
            f"请以{style}的风格，撰写一篇关于"{topic}"的微信公众号文章，"
            f"长度大约{length_map.get(length, '1000-1500字')}{keywords_text}。"
            f"{outline_text}"
            f"文章应当包含引人入胜的标题、内容丰富的正文和简短的总结。"
            f"请确保内容原创、有深度、有价值，适合在微信公众号发布。"
            f"返回格式应为JSON，包含title、content字段"
            f"{', outline' if outline else ''}和summary字段。"
        )
        
        return prompt
    
    async def _call_ai_service(self, prompt: str) -> str:
        """调用AI服务
        
        Args:
            prompt: 提示词
            
        Returns:
            str: AI生成的结果
        """
        # 这里应该实现实际的API调用
        # 为了演示，我们返回一个模拟的结果
        self.logger.debug(f"调用AI服务，提示词：{prompt[:100]}...")
        
        # 模拟API调用延迟
        await asyncio.sleep(2)
        
        # 返回模拟结果
        return json.dumps({
            "title": "模拟生成的标题",
            "outline": ["第一部分", "第二部分", "第三部分"],
            "content": "这是模拟生成的内容。实际实现时，这里应该是AI服务返回的真实内容。",
            "summary": "这是内容摘要。"
        })
    
    def _parse_result(self, result: str, outline: bool) -> Dict[str, Any]:
        """解析AI服务返回的结果
        
        Args:
            result: AI服务返回的结果
            outline: 是否包含大纲
            
        Returns:
            Dict: 解析后的结果
        """
        try:
            # 尝试解析JSON
            parsed = json.loads(result)
            
            # 验证必要字段
            if "title" not in parsed or "content" not in parsed:
                raise ValueError("返回结果缺少必要字段")
            
            # 如果需要大纲但结果中没有，添加空大纲
            if outline and "outline" not in parsed:
                parsed["outline"] = []
            
            # 如果没有摘要，添加空摘要
            if "summary" not in parsed:
                parsed["summary"] = ""
            
            return parsed
            
        except json.JSONDecodeError:
            # 如果不是JSON格式，尝试从文本中提取信息
            self.logger.warning("返回结果不是有效的JSON格式，尝试从文本中提取信息")
            
            lines = result.split("\n")
            title = next((line for line in lines if line.strip()), "未能提取标题")
            
            return {
                "title": title,
                "outline": [] if outline else None,
                "content": result,
                "summary": "未能提取摘要"
            }
        except Exception as e:
            self.logger.error(f"解析结果时出错：{str(e)}")
            return {
                "title": "解析错误",
                "outline": [] if outline else None,
                "content": result,
                "summary": f"解析结果时出错：{str(e)}"
            }

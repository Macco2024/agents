"""
内容生成器测试模块
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

from core.content_generator import ContentGenerator


class TestContentGenerator:
    """内容生成器测试类"""
    
    def setup_method(self):
        """测试前的设置"""
        self.generator = ContentGenerator(api_key="test_key")
    
    def test_init(self):
        """测试初始化"""
        assert self.generator.api_key == "test_key"
        assert self.generator.model is not None
    
    def test_init_without_api_key(self):
        """测试无API密钥初始化"""
        generator = ContentGenerator()
        assert generator.api_key == ""  # 假设配置文件中没有密钥
    
    @pytest.mark.asyncio
    async def test_generate_content_success(self):
        """测试成功生成内容"""
        with patch.object(self.generator, '_call_ai_service') as mock_call:
            mock_call.return_value = '{"title": "测试标题", "content": "测试内容", "summary": "测试摘要"}'
            
            result = await self.generator.generate_content("测试主题")
            
            assert "error" not in result
            assert result["title"] == "测试标题"
            assert result["content"] == "测试内容"
            assert result["summary"] == "测试摘要"
    
    @pytest.mark.asyncio
    async def test_generate_content_no_api_key(self):
        """测试无API密钥时的内容生成"""
        generator = ContentGenerator(api_key="")
        
        result = await generator.generate_content("测试主题")
        
        assert "error" in result
        assert result["error"] == "未配置API密钥"
    
    def test_build_prompt(self):
        """测试提示词构建"""
        prompt = self.generator._build_prompt(
            topic="AI发展",
            style="专业",
            length="中等",
            keywords=["机器学习", "深度学习"],
            outline=True
        )
        
        assert "AI发展" in prompt
        assert "专业" in prompt
        assert "机器学习" in prompt
        assert "深度学习" in prompt
        assert "大纲" in prompt
    
    def test_parse_result_valid_json(self):
        """测试解析有效JSON结果"""
        result_json = '{"title": "标题", "content": "内容", "summary": "摘要"}'
        
        parsed = self.generator._parse_result(result_json, outline=False)
        
        assert parsed["title"] == "标题"
        assert parsed["content"] == "内容"
        assert parsed["summary"] == "摘要"
    
    def test_parse_result_invalid_json(self):
        """测试解析无效JSON结果"""
        result_text = "这不是JSON格式的文本"
        
        parsed = self.generator._parse_result(result_text, outline=False)
        
        assert parsed["content"] == result_text
        assert "title" in parsed
        assert "summary" in parsed


if __name__ == "__main__":
    pytest.main([__file__])

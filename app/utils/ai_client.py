import requests
import json
import re
from typing import Optional, Dict, Any
from app.config import settings

class AIClient:
    """AI模型客户端，支持OpenAI格式的API"""
    
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.base_url = settings.AI_API_BASE_URL
        self.model = settings.AI_MODEL
        # 中文到英文的键名映射
        self.key_mapping = {
            '姓名': 'name',
            '电话': 'phone',
            '邮箱': 'email',
            '地址': 'address',
            '求职意向': 'career_objective',
            '期望薪资': 'expected_salary',
            '工作年限': 'work_experience_years',
            '学历背景': 'education',
            '项目经历': 'project_experience',
            '学历': 'education',
            '工作经验': 'work_experience_years',
            '专业': 'education'
        }
        print(f"AI Client initialized - Model: {self.model}, Base URL: {self.base_url}")
    
    def clean_json_response(self, text: str) -> str:
        """清理AI返回的文本，去除markdown代码块标记"""
        text = re.sub(r'```(json)?\s*', '', text.strip())
        text = re.sub(r'\s*```$', '', text.strip())
        return text
    
    def translate_keys(self, data: Dict) -> Dict:
        """将中文键名转换为英文键名"""
        result = {}
        for key, value in data.items():
            # 映射键名
            new_key = self.key_mapping.get(key, key)
            # 如果值是字典，递归处理
            if isinstance(value, dict):
                result[new_key] = self.translate_keys(value)
            # 如果值是列表，处理每个元素
            elif isinstance(value, list):
                result[new_key] = [self.translate_keys(item) if isinstance(item, dict) else item for item in value]
            else:
                result[new_key] = value
        return result
    
    def generate(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """调用AI模型生成文本（OpenAI格式）"""
        if not self.api_key:
            print("AI API Key not configured")
            return None
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个专业的简历分析助手。请直接输出JSON格式结果，不要包含markdown代码块标记。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            print(f"Sending request to {self.base_url}/chat/completions...")
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API Error: {response.text}")
                return None
                
            result = response.json()
            print(f"Response received: {json.dumps(result)[:500]}...")
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"Extracted content (first 300 chars): {content[:300]}...")
                return content
            return None
        except Exception as e:
            print(f"AI API调用失败: {str(e)}")
            return None
    
    def extract_resume_info(self, text: str) -> Dict[str, Any]:
        """从简历文本中提取关键信息"""
        print(f"Extracting resume info from text (length: {len(text)})...")
        
        prompt = f"""
请从以下简历文本中提取关键信息，以JSON格式输出：

简历内容：
{text[:3000]}

需要提取的信息包括：
1. 基本信息：姓名(name)、电话(phone)、邮箱(email)、地址(address)
2. 求职信息：求职意向(career_objective)、期望薪资(expected_salary)
3. 背景信息：工作年限(work_experience_years)、学历背景(education)、项目经历(project_experience)

请确保输出格式为标准JSON，只输出JSON内容，不要包含其他任何文本。
"""
        result = self.generate(prompt)
        if result:
            cleaned_result = self.clean_json_response(result)
            print(f"Cleaned result: {cleaned_result[:200]}...")
            
            try:
                parsed = json.loads(cleaned_result)
                flat_result = {}
                
                # 可能的键名映射
                possible_keys = [
                    ("basic_info", "basic_information", "基本信息"),
                    ("job_info", "career_info", "career_information", "求职信息"),
                    ("background_info", "background_information", "背景信息")
                ]
                
                # 扁平化处理
                for key_group in possible_keys:
                    for key in key_group:
                        if key in parsed and isinstance(parsed[key], dict):
                            flat_result.update(parsed[key])
                            break
                
                # 如果没有找到嵌套结构，直接使用原数据
                if not flat_result:
                    flat_result = parsed
                
                # 将中文键名转换为英文
                flat_result = self.translate_keys(flat_result)
                
                print(f"Parsed AI result: {json.dumps(flat_result, ensure_ascii=False)}")
                return flat_result
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {str(e)} - Cleaned result: {cleaned_result}")
                return {}
        print("AI returned None")
        return {}
    
    def analyze_job_requirement(self, job_description: str) -> Dict[str, Any]:
        """分析岗位需求，提取关键词"""
        prompt = f"""
请分析以下岗位需求描述，提取关键信息：

岗位描述：
{job_description}

请提取：
1. 主要技能要求(skills)
2. 学历要求(education_requirement)
3. 工作经验要求(experience_requirement)
4. 关键词列表(keywords)

输出格式为JSON，只输出JSON内容。
"""
        result = self.generate(prompt)
        if result:
            cleaned_result = self.clean_json_response(result)
            try:
                parsed = json.loads(cleaned_result)
                return self.translate_keys(parsed)
            except json.JSONDecodeError:
                print(f"JSON解析失败: {cleaned_result}")
                return {}
        return {}
    
    def calculate_match_score(self, resume_info: Dict, job_requirement: Dict) -> float:
        """计算简历与岗位的匹配度"""
        prompt = f"""
请计算以下简历与岗位需求的匹配度，输出一个0-100的分数。

简历信息：
{json.dumps(resume_info, ensure_ascii=False)}

岗位需求：
{json.dumps(job_requirement, ensure_ascii=False)}

请考虑：
1. 技能匹配程度
2. 工作经验相关性
3. 学历背景匹配
4. 项目经历相关性

只输出分数数字，不要其他内容。
"""
        result = self.generate(prompt)
        if result:
            try:
                return float(result.strip())
            except ValueError:
                return 0.0
        return 0.0

ai_client = AIClient()
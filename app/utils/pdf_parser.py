from PyPDF2 import PdfReader
import re
from typing import Optional

def extract_text_from_pdf(file_path: str) -> str:
    """从PDF文件中提取文本内容"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"PDF解析失败: {str(e)}")

def clean_text(text: str) -> str:
    """清洗文本，去除冗余字符（保留中文）"""
    # 去除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 去除特殊控制字符但保留中文
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
    # 去除多余的标点
    text = re.sub(r'([.,;!?])\1+', r'\1', text)
    # 去除首尾空白
    text = text.strip()
    return text

def extract_contact_info(text: str) -> dict:
    """从文本中提取联系信息（基础方法）"""
    result = {
        "name": None,
        "phone": None,
        "email": None,
        "address": None
    }
    
    # 匹配手机号
    phone_pattern = r'1[3-9]\d{9}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        result["phone"] = phone_match.group()
    
    # 匹配邮箱
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    if email_match:
        result["email"] = email_match.group()
    
    return result

def parse_resume(file_path: str) -> dict:
    """解析简历文件，返回结构化数据"""
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)
    contact_info = extract_contact_info(cleaned_text)
    
    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "contact_info": contact_info
    }
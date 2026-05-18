import sys
sys.path.insert(0, '.')

from app.utils.pdf_parser import parse_resume
from app.utils.ai_client import ai_client

# 测试PDF解析
pdf_path = r"d:\pro1\温星慧简历(1).pdf"

print(f"正在解析PDF: {pdf_path}")
try:
    result = parse_resume(pdf_path)
    print(f"\n=== PDF原始文本 (前500字符) ===")
    print(result["raw_text"][:500])
    print(f"\n=== 清洗后的文本 (前500字符) ===")
    print(result["cleaned_text"][:500])
    print(f"\n=== 提取的联系信息 ===")
    print(result["contact_info"])
    
    # 测试AI提取
    print("\n=== 测试AI提取 ===")
    ai_result = ai_client.extract_resume_info(result["cleaned_text"])
    print(f"AI提取结果: {ai_result}")
    
except Exception as e:
    print(f"解析失败: {str(e)}")
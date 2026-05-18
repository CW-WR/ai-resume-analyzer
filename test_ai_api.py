import sys
sys.path.insert(0, '.')

from app.utils.ai_client import ai_client

# 测试AI API是否正常工作
test_text = """
张三
电话：18070106229
邮箱：zhangsan@163.com
地址：北京市朝阳区

求职意向：Python开发工程师
期望薪资：20K-30K

工作经验：3年
学历：本科
项目经历：完成多个Python项目开发
"""

print("测试AI信息提取...")
result = ai_client.extract_resume_info(test_text)
print(f"AI返回结果: {result}")

if result:
    print("AI API工作正常！")
else:
    print("AI API调用失败，请检查配置")
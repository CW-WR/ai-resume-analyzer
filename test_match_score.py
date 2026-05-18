import sys
sys.path.insert(0, '.')

from app.utils.ai_client import ai_client

# 模拟简历信息
resume_info = {
    "basic_info": {
        "name": "温星慧",
        "phone": "18070106229",
        "email": "18070106229@163.com"
    },
    "background_info": {
        "work_experience_years": "0",
        "education": "东华理工大学 本科 软件工程 2023-2027",
        "project_experience": "周边游平台、写作助手、YOLO道路识别"
    },
    "cleaned_text": "温星慧 东华理工大学 本科 软件工程 2023-2027 Python项目经验 AI开发 深度学习 YOLO"
}

# 模拟岗位需求
job_requirement = {
    "keywords": ["Python", "AI", "深度学习", "本科", "软件工程"],
    "skills": ["Python", "AI开发", "深度学习"],
    "education_requirement": "本科",
    "experience_requirement": "不限"
}

print("测试AI匹配度计算...")
score = ai_client.calculate_match_score(resume_info, job_requirement)
print(f"AI返回的匹配度分数: {score}")

if score == 0.0:
    print("警告：AI返回了0分，可能有问题")
else:
    print(f"匹配度: {score}分")
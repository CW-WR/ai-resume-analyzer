from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import re
import json
from app.utils.ai_client import ai_client
from app.utils.cache import cache_manager
from app.schemas.job import JobMatchRequest
from app.schemas.resume import MatchScore

router = APIRouter(prefix="/api/match", tags=["岗位匹配"])

def simple_keyword_match(resume_text: str, keywords: list) -> tuple:
    """简单的关键词匹配"""
    found = []
    missing = []
    resume_lower = resume_text.lower()
    
    for keyword in keywords:
        if keyword.lower() in resume_lower:
            found.append(keyword)
        else:
            missing.append(keyword)
    
    return found, missing

def calculate_simple_score(resume_info: dict, job_requirement: dict) -> dict:
    """计算简单匹配分数"""
    resume_text = resume_info.get("cleaned_text", "")
    keywords = job_requirement.get("keywords", [])
    
    found, missing = simple_keyword_match(resume_text, keywords)
    
    skill_match = len(found) / len(keywords) * 100 if keywords else 0
    
    experience_match = 50
    if resume_info.get("background_info", {}).get("work_experience_years"):
        experience_match = 70
    
    education_match = 50
    if resume_info.get("background_info", {}).get("education"):
        education_match = 70
    
    overall_score = (skill_match + experience_match + education_match) / 3
    
    return {
        "overall_score": overall_score,
        "skill_match": skill_match,
        "experience_match": experience_match,
        "education_match": education_match,
        "keywords_found": found,
        "keywords_missing": missing
    }

@router.post("/score")
async def match_resume(request: JobMatchRequest):
    """计算简历与岗位的匹配度"""
    print(f"=== 匹配评分开始 ===")
    print(f"简历ID: {request.resume_id}")
    print(f"岗位描述: {request.job_description[:100]}...")
    
    # 获取简历信息
    resume_data = cache_manager.get(f"resume:{request.resume_id}")
    print(f"缓存中的简历数据: {'存在' if resume_data else '不存在'}")
    
    if not resume_data:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    # 分析岗位需求
    job_analysis = ai_client.analyze_job_requirement(request.job_description)
    print(f"AI岗位分析结果: {json.dumps(job_analysis)[:200]}...")
    
    # 如果AI分析失败，使用简单方法提取关键词
    if not job_analysis or not job_analysis.get("keywords"):
        print("AI分析失败，使用简单关键词提取")
        keywords = re.findall(r'[\u4e00-\u9fa5]{2,}|[a-zA-Z]+', request.job_description)
        job_analysis["keywords"] = list(set(keywords))[:20]
    
    print(f"最终关键词列表: {job_analysis['keywords']}")
    
    # 计算匹配度
    ai_score = 0.0
    simple_result = calculate_simple_score(resume_data, job_analysis)
    print(f"简单匹配结果: {simple_result}")
    
    if ai_client.api_key:
        # 使用AI计算匹配度
        print("调用AI计算匹配度...")
        ai_score = ai_client.calculate_match_score(resume_data, job_analysis)
        print(f"AI返回的匹配度分数: {ai_score}")
        
        # 如果AI计算失败（返回0），使用简单匹配的综合分数
        final_overall_score = ai_score if ai_score > 0 else simple_result["overall_score"]
        
        match_score = MatchScore(
            overall_score=final_overall_score,
            skill_match=simple_result["skill_match"],
            experience_match=simple_result["experience_match"],
            education_match=simple_result["education_match"],
            keywords_found=simple_result["keywords_found"],
            keywords_missing=simple_result["keywords_missing"]
        )
    else:
        # 使用简单匹配算法
        match_score = MatchScore(**simple_result)
    
    print(f"最终匹配分数: {match_score.dict()}")
    
    # 缓存匹配结果
    result = {
        "resume_id": request.resume_id,
        "match_score": match_score.dict(),
        "job_requirement": request.job_description
    }
    cache_manager.set(f"match:{request.resume_id}", result)
    
    print(f"=== 匹配评分结束 ===")
    return JSONResponse(content=result, status_code=200)
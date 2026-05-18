from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class BasicInfo(BaseModel):
    """基本信息"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class JobInfo(BaseModel):
    """求职信息"""
    career_objective: Optional[str] = None
    expected_salary: Optional[str] = None

class BackgroundInfo(BaseModel):
    """背景信息"""
    work_experience_years: Optional[str] = None
    education: Optional[str] = None
    project_experience: Optional[str] = None

class ResumeParseResult(BaseModel):
    """简历解析结果"""
    resume_id: str
    raw_text: str
    cleaned_text: str
    basic_info: BasicInfo
    job_info: JobInfo
    background_info: BackgroundInfo

class MatchScore(BaseModel):
    """匹配度评分"""
    overall_score: float = Field(description="综合匹配度")
    skill_match: float = Field(description="技能匹配率")
    experience_match: float = Field(description="经验匹配率")
    education_match: float = Field(description="学历匹配率")
    keywords_found: List[str] = Field(description="匹配的关键词")
    keywords_missing: List[str] = Field(description="缺失的关键词")

class ResumeMatchResult(BaseModel):
    """简历匹配结果"""
    resume_id: str
    match_score: MatchScore
    job_requirement: str
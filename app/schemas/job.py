from pydantic import BaseModel, Field
from typing import Optional, List

class JobRequirement(BaseModel):
    """岗位需求"""
    description: str = Field(description="岗位描述文本")
    skills: Optional[List[str]] = Field(default_factory=list)
    education_requirement: Optional[str] = None
    experience_requirement: Optional[str] = None
    keywords: Optional[List[str]] = Field(default_factory=list)

class JobMatchRequest(BaseModel):
    """岗位匹配请求"""
    resume_id: str = Field(description="简历ID")
    job_description: str = Field(description="岗位需求描述")
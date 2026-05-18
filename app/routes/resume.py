from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os
import json
from app.utils.pdf_parser import parse_resume
from app.utils.ai_client import ai_client
from app.utils.cache import cache_manager
from app.schemas.resume import ResumeParseResult, BasicInfo, JobInfo, BackgroundInfo

router = APIRouter(prefix="/api/resume", tags=["简历管理"])

TEMP_DIR = "temp"

def format_value(value):
    """格式化AI返回的值，确保转换为字符串"""
    if value is None:
        return None
    if isinstance(value, dict):
        # 将字典转换为可读字符串
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        # 将列表转换为可读字符串
        return "\n".join([str(item) if not isinstance(item, dict) else json.dumps(item, ensure_ascii=False) for item in value])
    # 其他类型（int, str等）直接转换为字符串
    return str(value)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """上传简历并解析"""
    # 验证文件类型
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支持PDF格式的简历文件")
    
    # 生成简历ID
    resume_id = str(uuid.uuid4())
    
    # 创建临时目录
    os.makedirs(TEMP_DIR, exist_ok=True)
    file_path = os.path.join(TEMP_DIR, f"{resume_id}.pdf")
    
    # 保存上传的文件
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    # 解析PDF
    try:
        parse_result = parse_resume(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"PDF解析失败: {str(e)}")
    
    # 使用AI提取关键信息
    ai_result = ai_client.extract_resume_info(parse_result["cleaned_text"])
    
    # 构建响应（处理类型转换）
    result = ResumeParseResult(
        resume_id=resume_id,
        raw_text=parse_result["raw_text"],
        cleaned_text=parse_result["cleaned_text"],
        basic_info=BasicInfo(
            name=ai_result.get("name") or parse_result["contact_info"].get("name"),
            phone=ai_result.get("phone") or parse_result["contact_info"].get("phone"),
            email=ai_result.get("email") or parse_result["contact_info"].get("email"),
            address=ai_result.get("address")
        ),
        job_info=JobInfo(
            career_objective=ai_result.get("career_objective"),
            expected_salary=ai_result.get("expected_salary")
        ),
        background_info=BackgroundInfo(
            work_experience_years=format_value(ai_result.get("work_experience_years")),
            education=format_value(ai_result.get("education")),
            project_experience=format_value(ai_result.get("project_experience"))
        )
    )
    
    # 缓存结果
    cache_manager.set(f"resume:{resume_id}", result.dict())
    
    # 删除临时文件
    os.remove(file_path)
    
    return JSONResponse(content=result.dict(), status_code=200)

@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    """获取简历详情"""
    # 从缓存获取
    cached_data = cache_manager.get(f"resume:{resume_id}")
    if not cached_data:
        raise HTTPException(status_code=404, detail="简历不存在或已过期")
    
    return JSONResponse(content=cached_data, status_code=200)

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    """删除简历"""
    cache_manager.delete(f"resume:{resume_id}")
    cache_manager.delete(f"match:{resume_id}")
    return JSONResponse(content={"message": "简历已删除"}, status_code=200)
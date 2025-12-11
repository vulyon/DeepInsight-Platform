"""
文件上传API
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE_DIR
from utils.file_handler import save_uploaded_file, load_csv_file, validate_csv_format

router = APIRouter(prefix="/upload", tags=["upload"])


class UploadResponse(BaseModel):
    """上传响应模型"""
    file_id: str
    message: str


@router.post("", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    上传CSV文件
    
    Args:
        file: 上传的文件
        
    Returns:
        文件ID和成功消息
    """
    # 验证文件类型
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="只支持CSV格式文件")
    
    try:
        # 读取文件内容
        file_content = await file.read()
        
        # 保存文件
        file_id = save_uploaded_file(file_content, file.filename)
        
        # 验证CSV格式
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from config import UPLOAD_DIR
        file_path = None
        for path in UPLOAD_DIR.glob(f"{file_id}.*"):
            if path.exists():
                file_path = path
                break
        
        if file_path:
            df = load_csv_file(file_path)
            is_valid, error_msg = validate_csv_format(df)
            if not is_valid:
                # 删除无效文件
                from utils.file_handler import cleanup_file
                cleanup_file(file_id)
                raise HTTPException(status_code=400, detail=error_msg)
        
        return UploadResponse(
            file_id=file_id,
            message="上传成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传文件时出错: {str(e)}")


@router.post("/demo/load", response_model=UploadResponse)
async def load_demo_data():
    """
    加载示例数据
    
    Returns:
        文件ID和成功消息
    """
    try:
        # 示例数据文件路径
        demo_file = BASE_DIR / "demo" / "数据集" / "reviews.csv"
        
        if not demo_file.exists():
            raise HTTPException(status_code=404, detail="示例数据文件不存在")
        
        # 读取示例文件
        with open(demo_file, 'rb') as f:
            file_content = f.read()
        
        # 保存文件
        file_id = save_uploaded_file(file_content, "demo_reviews.csv")
        
        # 验证CSV格式
        from config import UPLOAD_DIR
        file_path = None
        for path in UPLOAD_DIR.glob(f"{file_id}.*"):
            if path.exists():
                file_path = path
                break
        
        if file_path:
            df = load_csv_file(file_path)
            is_valid, error_msg = validate_csv_format(df)
            if not is_valid:
                from utils.file_handler import cleanup_file
                cleanup_file(file_id)
                raise HTTPException(status_code=400, detail=error_msg)
        
        return UploadResponse(
            file_id=file_id,
            message="示例数据加载成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载示例数据时出错: {str(e)}")


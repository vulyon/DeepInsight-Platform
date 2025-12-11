"""
文件处理工具
"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import UPLOAD_DIR, RESULT_DIR


def save_uploaded_file(file_content: bytes, filename: str) -> str:
    """
    保存上传的文件
    
    Args:
        file_content: 文件内容（字节）
        filename: 原始文件名
        
    Returns:
        文件ID（UUID字符串）
    """
    file_id = str(uuid.uuid4())
    file_ext = Path(filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    return file_id


def get_uploaded_file_path(file_id: str) -> Optional[Path]:
    """
    获取上传文件的路径
    
    Args:
        file_id: 文件ID
        
    Returns:
        文件路径，如果不存在返回None
    """
    # 尝试查找匹配的文件
    for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
        if file_path.exists():
            return file_path
    return None


def load_csv_file(file_path: Path) -> pd.DataFrame:
    """
    加载CSV文件
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        DataFrame
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        # 尝试其他编码
        df = pd.read_csv(file_path, encoding='gbk')
        return df


def validate_csv_format(df: pd.DataFrame) -> tuple[bool, str]:
    """
    验证CSV格式是否符合要求
    
    Args:
        df: DataFrame
        
    Returns:
        (是否有效, 错误信息)
    """
    required_columns = ['content', 'content_type']
    
    if df.empty:
        return False, "CSV文件为空"
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"缺少必需的列: {', '.join(missing_columns)}"
    
    # 验证content_type值
    valid_types = {'pos', 'neg'}
    invalid_types = df[~df['content_type'].isin(valid_types)]
    if not invalid_types.empty:
        return False, f"content_type列包含无效值，只允许 'pos' 或 'neg'"
    
    return True, ""


def save_result(task_id: str, result: dict):
    """
    保存分析结果
    
    Args:
        task_id: 任务ID
        result: 结果字典
    """
    import json
    result_path = RESULT_DIR / f"{task_id}.json"
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def load_result(task_id: str) -> Optional[dict]:
    """
    加载分析结果
    
    Args:
        task_id: 任务ID
        
    Returns:
        结果字典，如果不存在返回None
    """
    import json
    result_path = RESULT_DIR / f"{task_id}.json"
    if result_path.exists():
        with open(result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def cleanup_file(file_id: str):
    """
    清理上传的文件
    
    Args:
        file_id: 文件ID
    """
    file_path = get_uploaded_file_path(file_id)
    if file_path and file_path.exists():
        file_path.unlink()


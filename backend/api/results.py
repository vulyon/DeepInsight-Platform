"""
结果查询API
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from utils.file_handler import load_result

router = APIRouter(prefix="/results", tags=["results"])
# 为了符合设计文档，添加一个额外的路由
reviews_router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewItem(BaseModel):
    """评论项模型"""
    id: int
    content: str
    sentiment: str
    confidence: float


class ReviewsResponse(BaseModel):
    """评论列表响应模型"""
    total: int
    page: int
    page_size: int
    data: List[ReviewItem]


@router.get("/{task_id}")
async def get_results(task_id: str):
    """
    获取分析结果
    
    Args:
        task_id: 任务ID
        
    Returns:
        分析结果
    """
    result = load_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="结果不存在")
    
    return result


@router.get("/{task_id}/reviews", response_model=ReviewsResponse)
async def get_reviews(
    task_id: str,
    sentiment: Optional[str] = Query(None, description="情感类型: positive/negative"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """
    获取评论列表
    
    Args:
        task_id: 任务ID
        sentiment: 情感类型过滤（可选）
        page: 页码
        page_size: 每页数量
        
    Returns:
        评论列表
    """
    result = load_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="结果不存在")
    
    reviews = result.get('reviews', [])
    
    # 情感过滤
    if sentiment:
        sentiment_map = {'positive': 'pos', 'negative': 'neg'}
        target_sentiment = sentiment_map.get(sentiment.lower())
        if target_sentiment:
            reviews = [r for r in reviews if r.get('sentiment') == target_sentiment]
    
    # 分页
    total = len(reviews)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_reviews = reviews[start:end]
    
    return ReviewsResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=[ReviewItem(**r) for r in paginated_reviews]
    )


# 为了符合设计文档，添加符合设计文档的路由别名
@reviews_router.get("/{task_id}", response_model=ReviewsResponse)
async def get_reviews_by_task_id(
    task_id: str,
    sentiment: Optional[str] = Query(None, description="情感类型: positive/negative"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量")
):
    """
    获取评论列表（符合设计文档的路由）
    
    Args:
        task_id: 任务ID
        sentiment: 情感类型过滤（可选）
        page: 页码
        page_size: 每页数量
        
    Returns:
        评论列表
    """
    # 复用上面的逻辑
    return await get_reviews(task_id, sentiment, page, page_size)


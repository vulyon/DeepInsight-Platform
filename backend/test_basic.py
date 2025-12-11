"""
基本功能测试脚本
用于验证后端代码的基本功能是否正常
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """测试所有模块是否能正常导入"""
    print("测试模块导入...")
    try:
        from config import BASE_DIR, DATA_DIR, MODEL_DIR
        print(f"✓ 配置模块导入成功")
        print(f"  - BASE_DIR: {BASE_DIR}")
        print(f"  - DATA_DIR: {DATA_DIR}")
        print(f"  - MODEL_DIR: {MODEL_DIR}")
        
        from utils.file_handler import save_uploaded_file
        print("✓ 文件处理模块导入成功")
        
        from services.data_processor import DataProcessor
        print("✓ 数据预处理模块导入成功")
        
        from services.sentiment_analyzer import SentimentAnalyzer
        print("✓ 情感分析模块导入成功")
        
        from services.visualizer import Visualizer
        print("✓ 可视化模块导入成功")
        
        from models.lstm_model import LSTMModel
        print("✓ LSTM模型模块导入成功")
        
        from api import upload, analyze, results
        print("✓ API模块导入成功")
        
        from app import app
        print("✓ 主应用模块导入成功")
        
        print("\n所有模块导入成功！")
        return True
        
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """测试配置"""
    print("\n测试配置...")
    try:
        from config import (
            DATA_DIR, MODEL_DIR, UPLOAD_DIR, RESULT_DIR,
            POSITIVE_COMMENT_FILE, STOPWORDS_FILE
        )
        
        print(f"✓ 数据目录: {DATA_DIR} (存在: {DATA_DIR.exists()})")
        print(f"✓ 模型目录: {MODEL_DIR} (存在: {MODEL_DIR.exists()})")
        print(f"✓ 上传目录: {UPLOAD_DIR} (存在: {UPLOAD_DIR.exists()})")
        print(f"✓ 结果目录: {RESULT_DIR} (存在: {RESULT_DIR.exists()})")
        print(f"✓ 正面词典: {POSITIVE_COMMENT_FILE} (存在: {POSITIVE_COMMENT_FILE.exists()})")
        print(f"✓ 停用词表: {STOPWORDS_FILE} (存在: {STOPWORDS_FILE.exists()})")
        
        return True
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("后端代码基本功能测试")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_config()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ 所有基本测试通过！")
        print("\n提示: 运行 'python app.py' 或 './run.sh' 启动服务")
    else:
        print("✗ 部分测试失败，请检查错误信息")
    print("=" * 50)


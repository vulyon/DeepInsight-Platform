"""
配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "demo" / "数据集"
MODEL_DIR = BASE_DIR / "backend" / "models"
UPLOAD_DIR = BASE_DIR / "backend" / "uploads"
RESULT_DIR = BASE_DIR / "backend" / "results"

# 创建必要的目录
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 词典文件路径
POSITIVE_COMMENT_FILE = DATA_DIR / "正面评价词语（中文）.txt"
NEGATIVE_COMMENT_FILE = DATA_DIR / "负面评价词语（中文）.txt"
POSITIVE_EMOTION_FILE = DATA_DIR / "正面情感词语（中文）.txt"
NEGATIVE_EMOTION_FILE = DATA_DIR / "负面情感词语（中文）.txt"
STOPWORDS_FILE = DATA_DIR / "stoplist.txt"
NOT_DICT_FILE = DATA_DIR / "not.csv"

# 模型文件路径
LSTM_MODEL_FILE = MODEL_DIR / "sentiment_lstm.h5"
TOKENIZER_FILE = MODEL_DIR / "tokenizer.pkl"

# LSTM模型参数
MAX_FEATURES = 10000
MAX_LEN = 100
EMBEDDING_DIM = 128
LSTM_OUT = 128

# 词云图配置 - 中文字体路径
# 自动检测中文字体，如果找不到则使用默认字体
import os
from pathlib import Path

def find_chinese_font():
    """自动查找中文字体"""
    # 常见的中文字体路径
    font_paths = [
        # Linux 常见路径
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
        "/usr/share/fonts/truetype/arphic/ukai.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf",
        # Windows
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        # 备用字体
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    
    # 如果都找不到，尝试使用系统默认字体
    try:
        import matplotlib.font_manager as fm
        # 查找支持中文的字体
        for font in fm.fontManager.ttflist:
            if any(keyword in font.name.lower() for keyword in ['song', 'hei', 'kai', 'ming', 'noto', 'wqy']):
                if os.path.exists(font.fname):
                    return font.fname
    except:
        pass
    
    # 最后使用DejaVu字体（虽然不支持中文，但至少不会报错）
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FONT_PATH = find_chinese_font()

# API配置
API_PREFIX = "/api"


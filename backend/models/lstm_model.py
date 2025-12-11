"""
LSTM模型加载和预测
"""
import os
import pickle
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import jieba
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import LSTM_MODEL_FILE, TOKENIZER_FILE, MAX_FEATURES, MAX_LEN


class LSTMModel:
    """LSTM模型类"""
    
    def __init__(self):
        """初始化LSTM模型"""
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """加载LSTM模型和tokenizer"""
        # 如果模型文件不存在，创建一个占位模型
        if not LSTM_MODEL_FILE.exists():
            print(f"警告: LSTM模型文件 {LSTM_MODEL_FILE} 不存在，将创建占位模型")
            self._create_placeholder_model()
            return
        
        try:
            # 加载模型
            self.model = load_model(str(LSTM_MODEL_FILE))
            
            # 加载tokenizer
            if TOKENIZER_FILE.exists():
                with open(TOKENIZER_FILE, 'rb') as f:
                    self.tokenizer = pickle.load(f)
            else:
                print(f"警告: Tokenizer文件 {TOKENIZER_FILE} 不存在，将创建新的tokenizer")
                self.tokenizer = None
                
        except Exception as e:
            print(f"加载模型时出错: {e}")
            self._create_placeholder_model()
    
    def _create_placeholder_model(self):
        """创建占位模型（用于测试，实际应该训练模型）"""
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Embedding, LSTM, Dense
        from tensorflow.keras.preprocessing.text import Tokenizer
        
        # 创建简单的tokenizer
        self.tokenizer = Tokenizer(num_words=MAX_FEATURES)
        
        # 创建占位模型
        self.model = Sequential([
            Embedding(MAX_FEATURES, 128, input_length=MAX_LEN),
            LSTM(128, dropout=0.2, recurrent_dropout=0.2),
            Dense(2, activation='softmax')
        ])
        
        # 编译模型（不训练，仅用于结构）
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        print("已创建占位LSTM模型，实际使用时需要训练或加载训练好的模型")
    
    def preprocess_text(self, text: str) -> np.ndarray:
        """
        预处理文本
        
        Args:
            text: 原始文本
            
        Returns:
            序列化的文本数组
        """
        # 分词
        words = jieba.cut(text)
        text_seg = ' '.join(words)
        
        # 序列化
        if self.tokenizer is None:
            # 如果没有tokenizer，返回零向量
            return np.zeros((1, MAX_LEN))
        
        sequences = self.tokenizer.texts_to_sequences([text_seg])
        padded = pad_sequences(sequences, maxlen=MAX_LEN)
        
        return padded
    
    def predict(self, text: str) -> Tuple[int, float]:
        """
        预测文本情感
        
        Args:
            text: 输入文本
            
        Returns:
            (预测类别: 0=负面, 1=正面, 置信度)
        """
        if self.model is None:
            # 如果没有模型，返回随机预测（用于测试）
            return 1, 0.5
        
        try:
            # 预处理文本
            processed = self.preprocess_text(text)
            
            # 预测
            prediction = self.model.predict(processed, verbose=0)
            
            # 获取预测类别和置信度
            pred_class = int(np.argmax(prediction[0]))
            confidence = float(prediction[0][pred_class])
            
            return pred_class, confidence
            
        except Exception as e:
            print(f"预测时出错: {e}")
            # 返回默认值
            return 1, 0.5
    
    def batch_predict(self, texts: list) -> list:
        """
        批量预测
        
        Args:
            texts: 文本列表
            
        Returns:
            预测结果列表，每个元素为(类别, 置信度)
        """
        results = []
        for text in texts:
            pred, conf = self.predict(text)
            results.append((pred, conf))
        return results


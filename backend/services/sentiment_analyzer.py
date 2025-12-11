"""
情感分析服务（结合词典和LSTM模型）
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    POSITIVE_COMMENT_FILE, NEGATIVE_COMMENT_FILE,
    POSITIVE_EMOTION_FILE, NEGATIVE_EMOTION_FILE,
    NOT_DICT_FILE
)
from services.data_processor import DataProcessor
from models.lstm_model import LSTMModel


class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        """初始化情感分析器"""
        self.data_processor = DataProcessor()
        self.lstm_model = LSTMModel()
        self.positive_words, self.negative_words = self._load_sentiment_dicts()
        self.not_dict = self._load_not_dict()
    
    def _load_sentiment_dicts(self) -> Tuple[set, set]:
        """加载情感词典"""
        def load_dict_file(file_path: Path) -> List[str]:
            """加载词典文件"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip()]
                return lines
            except FileNotFoundError:
                print(f"警告: 词典文件 {file_path} 不存在")
                return []
        
        # 加载正面和负面评价词、情感词
        pos_comment = load_dict_file(POSITIVE_COMMENT_FILE)
        pos_emotion = load_dict_file(POSITIVE_EMOTION_FILE) if POSITIVE_EMOTION_FILE.exists() else []
        neg_comment = load_dict_file(NEGATIVE_COMMENT_FILE)
        neg_emotion = load_dict_file(NEGATIVE_EMOTION_FILE) if NEGATIVE_EMOTION_FILE.exists() else []
        
        # 合并
        positive = set(pos_comment) | set(pos_emotion)
        negative = set(neg_comment) | set(neg_emotion)
        
        # 去除交集
        intersection = positive & negative
        positive = positive - intersection
        negative = negative - intersection
        
        return positive, negative
    
    def _load_not_dict(self) -> List[str]:
        """加载否定词表"""
        try:
            not_df = pd.read_csv(NOT_DICT_FILE)
            return not_df['term'].tolist()
        except FileNotFoundError:
            print(f"警告: 否定词文件 {NOT_DICT_FILE} 不存在")
            return []
    
    def analyze_with_dict(self, word_df: pd.DataFrame) -> pd.DataFrame:
        """
        使用情感词典进行情感分析
        
        Args:
            word_df: 分词结果DataFrame
            
        Returns:
            包含情感分析结果的DataFrame
        """
        # 创建情感词权重DataFrame
        positive_df = pd.DataFrame({
            "word": list(self.positive_words),
            "weight": [1] * len(self.positive_words)
        })
        negative_df = pd.DataFrame({
            "word": list(self.negative_words),
            "weight": [-1] * len(self.negative_words)
        })
        posneg = pd.concat([positive_df, negative_df], ignore_index=True)
        
        # 合并分词结果与情感词表
        data_posneg = posneg.merge(word_df, left_on='word', right_on='word', how='right')
        data_posneg = data_posneg.sort_values(by=['index_content', 'index_word'])
        
        # 处理否定词修正
        data_posneg['amend_weight'] = data_posneg['weight']
        data_posneg['id'] = np.arange(0, len(data_posneg))
        
        # 只保留有情感值的词语
        only_inclination = data_posneg.dropna().reset_index(drop=True)
        
        if only_inclination.empty:
            # 如果没有情感词，返回空结果
            return pd.DataFrame(columns=['index_content', 'a_type', 'amend_weight'])
        
        index = only_inclination['id']
        
        # 否定词修正
        for i in range(len(only_inclination)):
            review = data_posneg[data_posneg['index_content'] == only_inclination['index_content'].iloc[i]]
            review = review.reset_index(drop=True)
            affective = only_inclination['index_word'].iloc[i]
            
            if affective == 0:
                # 第一个词，检查前一个词（如果有）
                ne = 0
            elif affective == 1:
                # 检查前一个词
                prev_word = review['word'].iloc[affective - 1] if len(review) > affective - 1 else ""
                ne = sum([w in self.not_dict for w in [prev_word]]) % 2
            else:
                # 检查前两个词
                prev_words = review['word'].iloc[affective - 2:affective].tolist() if len(review) >= affective else []
                ne = sum([w in self.not_dict for w in prev_words]) % 2
            
            if ne == 1:
                idx_value = index.iloc[i] if isinstance(index, pd.Series) else index[i]
                data_posneg.loc[idx_value, 'amend_weight'] = -data_posneg.loc[idx_value, 'weight']
        
        # 更新只保留情感值的数据
        only_inclination = data_posneg.loc[data_posneg['id'].isin(index)].dropna()
        
        # 计算每条评论的情感值
        emotional_value = only_inclination.groupby(['index_content'], as_index=False)['amend_weight'].sum()
        
        # 去除情感值为0的评论
        emotional_value = emotional_value[emotional_value['amend_weight'] != 0]
        
        # 给情感值分类
        emotional_value['a_type'] = ''
        emotional_value.loc[emotional_value['amend_weight'] > 0, 'a_type'] = 'pos'
        emotional_value.loc[emotional_value['amend_weight'] < 0, 'a_type'] = 'neg'
        
        return emotional_value[['index_content', 'a_type', 'amend_weight']]
    
    def analyze_with_lstm(self, reviews_df: pd.DataFrame) -> pd.DataFrame:
        """
        使用LSTM模型进行情感分析
        
        Args:
            reviews_df: 原始评论DataFrame，包含content列
            
        Returns:
            包含LSTM预测结果的DataFrame
        """
        predictions = []
        confidences = []
        
        for content in reviews_df['content']:
            pred, conf = self.lstm_model.predict(content)
            predictions.append('pos' if pred == 1 else 'neg')
            confidences.append(float(conf))
        
        result_df = reviews_df.copy()
        result_df['lstm_pred'] = predictions
        result_df['lstm_confidence'] = confidences
        
        return result_df
    
    def analyze(self, df: pd.DataFrame) -> Dict:
        """
        完整的情感分析流程（结合词典和LSTM）
        
        Args:
            df: 原始评论DataFrame
            
        Returns:
            包含分析结果的字典
        """
        # 1. 数据预处理
        word_df = self.data_processor.preprocess(df)
        
        # 2. 词典分析
        dict_result = self.analyze_with_dict(word_df)
        
        # 3. LSTM分析
        lstm_result = self.analyze_with_lstm(df)
        
        # 4. 合并结果
        # 将词典分析结果映射回原始评论
        reviews_with_dict = lstm_result.copy()
        reviews_with_dict['dict_pred'] = 'unknown'
        
        # 创建index_content到a_type的映射
        if not dict_result.empty:
            dict_map = dict(zip(dict_result['index_content'], dict_result['a_type']))
            reviews_with_dict['dict_pred'] = reviews_with_dict.index.map(
                lambda idx: dict_map.get(idx + 1, 'unknown')
            )
        
        # 合并预测结果（优先使用LSTM，如果LSTM预测失败则使用词典）
        reviews_with_dict['final_pred'] = reviews_with_dict['lstm_pred']
        # 如果LSTM预测为unknown或不存在，使用词典预测
        mask = (reviews_with_dict['final_pred'].isna()) | (reviews_with_dict['final_pred'] == 'unknown')
        reviews_with_dict.loc[mask, 'final_pred'] = reviews_with_dict.loc[mask, 'dict_pred']
        
        # 5. 计算准确率（如果有真实标签）
        accuracy = None
        confusion_matrix = None
        if 'content_type' in df.columns:
            from sklearn.metrics import accuracy_score, confusion_matrix as cm
            y_true = df['content_type'].map({'pos': 1, 'neg': 0})
            y_pred = reviews_with_dict['final_pred'].map({'pos': 1, 'neg': 0, 'unknown': -1})
            valid_mask = y_pred != -1
            if valid_mask.sum() > 0:
                accuracy = float(accuracy_score(y_true[valid_mask], y_pred[valid_mask]))
                confusion_matrix = cm(y_true[valid_mask], y_pred[valid_mask]).tolist()
        
        # 6. 统计信息
        total = len(reviews_with_dict)
        positive = (reviews_with_dict['final_pred'] == 'pos').sum()
        negative = (reviews_with_dict['final_pred'] == 'neg').sum()
        positive_rate = positive / total if total > 0 else 0
        
        return {
            'reviews': reviews_with_dict.to_dict('records'),
            'word_df': word_df,
            'statistics': {
                'total': int(total),
                'positive': int(positive),
                'negative': int(negative),
                'positive_rate': float(positive_rate),
                'accuracy': accuracy
            },
            'confusion_matrix': confusion_matrix
        }


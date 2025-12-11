"""
数据预处理服务（基于demo代码）
"""
import re
import pandas as pd
import numpy as np
import jieba.posseg as psg
from pathlib import Path
from typing import List, Tuple
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import STOPWORDS_FILE


class DataProcessor:
    """数据预处理类"""
    
    def __init__(self):
        """初始化数据处理器"""
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> set:
        """加载停用词表"""
        try:
            with open(STOPWORDS_FILE, 'r', encoding='UTF-8') as f:
                stopwords = set(line.strip() for line in f.readlines())
            return stopwords
        except FileNotFoundError:
            print(f"警告: 停用词文件 {STOPWORDS_FILE} 不存在，使用空停用词表")
            return set()
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据预处理主流程
        
        Args:
            df: 原始DataFrame，包含content和content_type列
            
        Returns:
            处理后的DataFrame，包含分词结果
        """
        # 1. 去重
        reviews = df[['content', 'content_type']].drop_duplicates().copy()
        content = reviews['content']
        
        # 2. 去除英文、数字、特定品牌词
        strinfo = re.compile('[0-9a-zA-Z]|京东|美的|电热水器|热水器|')
        content = content.apply(lambda x: strinfo.sub('', x))
        
        # 3. 分词
        worker = lambda s: [(x.word, x.flag) for x in psg.cut(s)]
        seg_word = content.apply(worker)
        
        # 4. 转换为DataFrame格式
        result = self._seg_to_dataframe(seg_word, reviews)
        
        # 5. 删除标点符号
        result = result[result['nature'] != 'x']
        
        # 6. 删除停用词
        result = result[~result['word'].isin(self.stopwords)]
        
        # 7. 添加词语位置索引
        result = self._add_word_index(result)
        
        # 8. 提取含有名词类的评论
        ind = result[['n' in x for x in result['nature']]]['index_content'].unique()
        result = result[[x in ind for x in result['index_content']]]
        
        return result
    
    def _seg_to_dataframe(self, seg_word: pd.Series, reviews: pd.DataFrame) -> pd.DataFrame:
        """
        将分词结果转换为DataFrame
        
        Args:
            seg_word: 分词结果Series
            reviews: 原始评论DataFrame
            
        Returns:
            包含分词信息的DataFrame
        """
        n_word = seg_word.apply(lambda x: len(x))
        
        # 评论ID
        n_content = [[x+1]*y for x, y in zip(list(seg_word.index), list(n_word))]
        index_content = sum(n_content, [])
        
        # 词语和词性
        seg_word_flat = sum(seg_word, [])
        word = [x[0] for x in seg_word_flat]
        nature = [x[1] for x in seg_word_flat]
        
        # 评论类型
        content_type = [[x]*y for x, y in zip(list(reviews['content_type']), list(n_word))]
        content_type = sum(content_type, [])
        
        result = pd.DataFrame({
            "index_content": index_content,
            "word": word,
            "nature": nature,
            "content_type": content_type
        })
        
        return result
    
    def _add_word_index(self, result: pd.DataFrame) -> pd.DataFrame:
        """
        添加词语在评论中的位置索引
        
        Args:
            result: 分词结果DataFrame
            
        Returns:
            添加了index_word列的DataFrame
        """
        n_word = list(result.groupby(by=['index_content'])['index_content'].count())
        index_word = [list(np.arange(0, y)) for y in n_word]
        index_word = sum(index_word, [])
        result['index_word'] = index_word
        return result
    
    def get_word_frequencies(self, result: pd.DataFrame, sentiment: str = None) -> pd.Series:
        """
        获取词频统计
        
        Args:
            result: 分词结果DataFrame
            sentiment: 情感类型 ('pos' 或 'neg')，如果为None则统计全部
            
        Returns:
            词频Series，按频率降序排列
        """
        if sentiment:
            result = result[result['content_type'] == sentiment]
        
        frequencies = result.groupby('word')['word'].count()
        frequencies = frequencies.sort_values(ascending=False)
        return frequencies


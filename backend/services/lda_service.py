"""
LDA主题模型服务（参考微博分析项目的LDA.py）
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import jieba
import jieba.posseg as psg
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import STOPWORDS_FILE

# 尝试导入gensim和pyLDAvis，如果不存在则提供降级方案
try:
    from gensim import corpora, models
    import pyLDAvis
    import pyLDAvis.gensim_models as gensimvis
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False
    print("警告: gensim 或 pyLDAvis 未安装，LDA功能将不可用")
    print("请运行: pip install gensim pyldavis")


class LDAService:
    """LDA主题模型分析服务"""
    
    def __init__(self):
        """初始化LDA服务"""
        self.stopwords = self._load_stopwords()
        jieba.initialize()
    
    def _load_stopwords(self) -> set:
        """加载停用词表"""
        try:
            with open(STOPWORDS_FILE, 'r', encoding='UTF-8') as f:
                stopwords = set(line.strip() for line in f.readlines())
            return stopwords
        except FileNotFoundError:
            print(f"警告: 停用词文件 {STOPWORDS_FILE} 不存在，使用空停用词表")
            return set()
    
    def preprocess_texts(self, texts: List[str]) -> List[List[str]]:
        """
        预处理文本，用于LDA分析
        
        Args:
            texts: 文本列表
            
        Returns:
            分词后的文本列表
        """
        processed_texts = []
        
        for text in texts:
            # 分词和词性标注
            words = psg.cut(str(text))
            # 过滤：只保留名词、动词、形容词，长度>1，不在停用词表中
            filtered_words = [
                word.word for word in words
                if len(word.word) > 1
                and word.word not in self.stopwords
                and ('n' in word.flag or 'v' in word.flag or 'a' in word.flag)
            ]
            if len(filtered_words) > 2:  # 至少3个词
                processed_texts.append(filtered_words)
        
        return processed_texts
    
    def train_lda_model(self, texts: List[str], num_topics: int = 5, passes: int = 10) -> Dict:
        """
        训练LDA模型并生成可视化数据
        
        Args:
            texts: 文本列表
            num_topics: 主题数量
            passes: 训练轮数
            
        Returns:
            包含LDA模型和可视化数据的字典
        """
        if not GENSIM_AVAILABLE:
            return {
                'topics': [],
                'vis_html': None,
                'error': 'gensim 或 pyLDAvis 未安装，请运行: pip install gensim pyldavis'
            }
        
        if len(texts) < num_topics:
            # 如果文本数量少于主题数，减少主题数
            num_topics = max(2, len(texts) // 2)
        
        # 预处理文本
        processed_texts = self.preprocess_texts(texts[:500])  # 限制数量，避免过慢
        
        if len(processed_texts) < num_topics:
            # 如果预处理后的文本太少，返回空结果
            return {
                'topics': [],
                'vis_html': None,
                'error': '文本数量不足，无法进行LDA分析'
            }
        
        try:
            # 创建词典
            dictionary = corpora.Dictionary(processed_texts)
            # 过滤极端值
            dictionary.filter_extremes(no_below=2, no_above=0.8)
            
            # 转换为语料库
            corpus = [dictionary.doc2bow(text) for text in processed_texts]
            
            # 训练LDA模型
            lda_model = models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=num_topics,
                passes=passes,
                alpha='auto',
                per_word_topics=True
            )
            
            # 生成主题列表
            topics = []
            for idx, topic in lda_model.print_topics(num_words=10):
                topics.append({
                    'id': idx,
                    'words': topic,
                    'top_words': [word.split('*')[1].strip('"') for word in topic.split('+')[:5]]
                })
            
            # 生成pyLDAvis可视化（转换为HTML字符串）
            try:
                vis = gensimvis.prepare(lda_model, corpus, dictionary, sort_topics=False)
                # 将可视化转换为HTML字符串
                vis_html = pyLDAvis.prepared_data_to_html(vis)
            except Exception as e:
                print(f"生成LDA可视化时出错: {e}")
                vis_html = None
            
            return {
                'topics': topics,
                'vis_html': vis_html,
                'num_topics': num_topics,
                'num_docs': len(processed_texts)
            }
            
        except Exception as e:
            print(f"LDA模型训练出错: {e}")
            return {
                'topics': [],
                'vis_html': None,
                'error': str(e)
            }
    
    def generate_lda_from_reviews(self, reviews: List[Dict], num_topics: int = 5) -> Dict:
        """
        从评论列表生成LDA分析结果
        
        Args:
            reviews: 评论列表
            num_topics: 主题数量
            
        Returns:
            LDA分析结果
        """
        # 提取评论内容
        texts = [review.get('content', '') for review in reviews if review.get('content')]
        
        if len(texts) < num_topics:
            return {
                'topics': [],
                'vis_html': None,
                'error': f'评论数量({len(texts)})少于主题数({num_topics})'
            }
        
        return self.train_lda_model(texts, num_topics=num_topics)


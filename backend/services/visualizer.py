"""
可视化数据生成服务
"""
import base64
import io
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import FONT_PATH


class Visualizer:
    """可视化数据生成器"""
    
    def __init__(self):
        """初始化可视化器"""
        self.font_path = FONT_PATH
        # 缓存默认图片
        self._default_positive_image = None
        self._default_negative_image = None
    
    def generate_wordcloud(self, word_frequencies: pd.Series, 
                          max_words: int = 100,
                          background_color: str = 'white') -> str:
        """
        生成词云图（base64编码）
        
        Args:
            word_frequencies: 词频Series
            max_words: 最大词数
            background_color: 背景颜色
            
        Returns:
            base64编码的图片字符串
        """
        if word_frequencies.empty:
            # 返回空白图片
            return self._create_blank_image()
        
        try:
            # 转换为字典格式
            word_dict = word_frequencies.to_dict()
            
            # 创建词云
            wordcloud = WordCloud(
                font_path=self.font_path,
                max_words=max_words,
                background_color=background_color,
                width=800,
                height=400,
                relative_scaling=0.5
            )
            
            # 生成词云
            wordcloud.fit_words(word_dict)
            
            # 转换为base64
            img_buffer = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"生成词云图时出错: {e}")
            return self._create_blank_image()
    
    def _create_blank_image(self) -> str:
        """创建空白图片"""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, '暂无数据', ha='center', va='center', fontsize=20)
        ax.axis('off')
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    
    def generate_pie_chart_data(self, statistics: Dict) -> List[Dict]:
        """
        生成饼图数据
        
        Args:
            statistics: 统计信息字典
            
        Returns:
            ECharts饼图数据格式
        """
        return [
            {"name": "正面", "value": statistics.get('positive', 0)},
            {"name": "负面", "value": statistics.get('negative', 0)}
        ]
    
    def generate_confusion_matrix_data(self, confusion_matrix: Optional[List]) -> List[List]:
        """
        生成混淆矩阵数据
        
        Args:
            confusion_matrix: 混淆矩阵（2x2列表）
            
        Returns:
            混淆矩阵数据（用于ECharts热力图）
        """
        if confusion_matrix is None:
            return [[0, 0], [0, 0]]
        
        # 确保是2x2矩阵
        if len(confusion_matrix) == 2 and len(confusion_matrix[0]) == 2:
            return confusion_matrix
        
        return [[0, 0], [0, 0]]
    
    def generate_time_series_data(self, reviews: List[Dict]) -> Dict:
        """
        生成时间序列数据（参考微博分析项目的line.py）
        
        Args:
            reviews: 评论列表，包含情感分析结果
            
        Returns:
            时间序列数据，用于折线图展示
        """
        # 如果没有时间信息，生成模拟的时间序列
        # 按评论顺序分组，每10条评论为一组
        time_data = {
            'dates': [],
            'positive': [],
            'negative': [],
            'total': []
        }
        
        if not reviews:
            return time_data
        
        # 将评论分组（每10条一组）
        group_size = max(1, len(reviews) // 10)
        for i in range(0, len(reviews), group_size):
            group = reviews[i:i + group_size]
            pos_count = sum(1 for r in group if r.get('sentiment') == 'pos' or r.get('final_pred') == 'pos')
            neg_count = sum(1 for r in group if r.get('sentiment') == 'neg' or r.get('final_pred') == 'neg')
            
            time_data['dates'].append(f'批次{i//group_size + 1}')
            time_data['positive'].append(pos_count)
            time_data['negative'].append(neg_count)
            time_data['total'].append(len(group))
        
        return time_data
    
    def generate_3d_bar_data(self, reviews: List[Dict]) -> Dict:
        """
        生成3D柱状图数据（参考微博分析项目的3Dbar.py）
        
        Args:
            reviews: 评论列表，包含情感分析结果
            
        Returns:
            3D柱状图数据
        """
        # 按置信度区间分组统计
        confidence_ranges = [
            (0.0, 0.2, '0-0.2'),
            (0.2, 0.4, '0.2-0.4'),
            (0.4, 0.6, '0.4-0.6'),
            (0.6, 0.8, '0.6-0.8'),
            (0.8, 1.0, '0.8-1.0')
        ]
        
        pos_data = [0] * len(confidence_ranges)
        neg_data = [0] * len(confidence_ranges)
        
        for review in reviews:
            confidence = review.get('confidence', review.get('lstm_confidence', 0.5))
            sentiment = review.get('sentiment', review.get('final_pred', 'pos'))
            
            for idx, (low, high, label) in enumerate(confidence_ranges):
                if low <= confidence < high:
                    if sentiment == 'pos':
                        pos_data[idx] += 1
                    else:
                        neg_data[idx] += 1
                    break
        
        return {
            'categories': [label for _, _, label in confidence_ranges],
            'positive': pos_data,
            'negative': neg_data
        }
    
    def generate_keywords_data(self, reviews: List[Dict], top_n: int = 20) -> List[Dict]:
        """
        生成关键词数据（参考微博分析项目）
        
        Args:
            reviews: 评论列表
            top_n: 返回前N个关键词
            
        Returns:
            关键词列表，包含词和频率
        """
        # 简单的关键词提取（基于词频）
        # 实际项目中可以使用TF-IDF或TextRank
        word_freq = {}
        
        for review in reviews:
            content = review.get('content', '')
            # 简单分词（实际应该使用jieba）
            words = content.split()
            for word in words:
                if len(word) > 1:  # 过滤单字
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序并取前N个
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return [
            {'word': word, 'freq': freq}
            for word, freq in sorted_words
        ]
    
    def generate_statistics(self, analysis_result: Dict) -> Dict:
        """
        生成统计信息
        
        Args:
            analysis_result: 分析结果字典
            
        Returns:
            统计信息字典
        """
        stats = analysis_result.get('statistics', {})
        
        return {
            'total': stats.get('total', 0),
            'positive': stats.get('positive', 0),
            'negative': stats.get('negative', 0),
            'positive_rate': stats.get('positive_rate', 0.0),
            'accuracy': stats.get('accuracy')
        }
    
    def _create_default_wordcloud_image(self, sentiment: str = 'positive') -> str:
        """
        创建默认的静态词云图片（用于快速展示）
        
        Args:
            sentiment: 情感类型 ('positive' 或 'negative')
            
        Returns:
            base64编码的图片字符串
        """
        # 检查缓存
        if sentiment == 'positive' and self._default_positive_image:
            return self._default_positive_image
        if sentiment == 'negative' and self._default_negative_image:
            return self._default_negative_image
        
        try:
            # 使用示例词汇创建词云
            if sentiment == 'positive':
                sample_words = {
                    '好': 50, '不错': 40, '满意': 35, '推荐': 30, '质量': 25,
                    '喜欢': 20, '值得': 18, '方便': 15, '实用': 12, '性价比': 10,
                    '好用': 8, '服务': 7, '包装': 6, '物流': 5, '正品': 4
                }
                bg_color = '#f0f9ff'
            else:
                sample_words = {
                    '差': 50, '不好': 40, '失望': 35, '问题': 30, '质量': 25,
                    '退货': 20, '破损': 18, '慢': 15, '贵': 12, '不推荐': 10,
                    '故障': 8, '服务': 7, '包装': 6, '物流': 5, '假货': 4
                }
                bg_color = '#fff0f0'
            
            # 创建词云
            # 检查字体是否支持中文，如果不支持则尝试其他字体
            font_to_use = self.font_path
            
            # 如果当前字体是DejaVu（不支持中文），尝试查找中文字体
            if 'dejavu' in self.font_path.lower() or 'DejaVu' in self.font_path:
                import os
                chinese_fonts = [
                    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                    "/usr/share/fonts/truetype/arphic/uming.ttc",
                    "/usr/share/fonts/truetype/arphic/ukai.ttc",
                    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
                ]
                for font in chinese_fonts:
                    if os.path.exists(font):
                        font_to_use = font
                        print(f"使用中文字体: {font}")
                        break
            
            # 创建词云
            try:
                wordcloud = WordCloud(
                    font_path=font_to_use,
                    max_words=50,
                    background_color=bg_color,
                    width=800,
                    height=400,
                    relative_scaling=0.5,
                    prefer_horizontal=0.7,
                    colormap='viridis' if sentiment == 'positive' else 'Reds'
                )
                wordcloud.fit_words(sample_words)
            except Exception as font_error:
                # 如果指定字体失败，尝试不指定字体（使用默认字体）
                print(f"使用指定字体失败: {font_error}，尝试使用默认字体")
                try:
                    wordcloud = WordCloud(
                        max_words=50,
                        background_color=bg_color,
                        width=800,
                        height=400,
                        relative_scaling=0.5,
                        prefer_horizontal=0.7,
                        colormap='viridis' if sentiment == 'positive' else 'Reds'
                    )
                    wordcloud.fit_words(sample_words)
                except Exception as e:
                    print(f"创建词云失败: {e}")
                    raise
            
            # 转换为base64
            img_buffer = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            result = f"data:image/png;base64,{img_base64}"
            
            # 缓存结果
            if sentiment == 'positive':
                self._default_positive_image = result
            else:
                self._default_negative_image = result
            
            return result
        except Exception as e:
            print(f"创建默认词云图时出错: {e}")
            return self._create_blank_image()
    
    def generate_wordclouds(self, word_df: pd.DataFrame, reviews: List[Dict] = None, use_default: bool = False) -> Dict[str, str]:
        """
        生成正面和负面词云图
        
        Args:
            word_df: 分词结果DataFrame
            reviews: 分析结果中的评论列表（包含final_pred），如果提供则使用预测结果，否则使用原始标签
            use_default: 如果为True，直接返回默认静态图片（用于快速展示）
            
        Returns:
            包含正面和负面词云图的字典
        """
        # 如果使用默认图片，直接返回
        if use_default:
            return {
                'positive': self._create_default_wordcloud_image('positive'),
                'negative': self._create_default_wordcloud_image('negative')
            }
        
        try:
            # 如果提供了reviews，根据final_pred来映射
            if reviews:
                # 创建index_content到final_pred的映射
                pred_map = {}
                for review in reviews:
                    # reviews中的索引对应word_df中的index_content - 1
                    idx = review.get('id', -1)
                    if idx >= 0:
                        pred_map[idx + 1] = review.get('final_pred', 'unknown')
                
                # 为word_df添加pred列
                word_df = word_df.copy()
                word_df['pred'] = word_df['index_content'].map(lambda x: pred_map.get(x, 'unknown'))
                
                # 正面词云（基于预测结果）
                pos_freq = word_df[word_df['pred'] == 'pos'].groupby('word')['word'].count()
                pos_freq = pos_freq.sort_values(ascending=False)
                pos_wordcloud = self.generate_wordcloud(pos_freq) if not pos_freq.empty else self._create_default_wordcloud_image('positive')
                
                # 负面词云（基于预测结果）
                neg_freq = word_df[word_df['pred'] == 'neg'].groupby('word')['word'].count()
                neg_freq = neg_freq.sort_values(ascending=False)
                neg_wordcloud = self.generate_wordcloud(neg_freq) if not neg_freq.empty else self._create_default_wordcloud_image('negative')
            else:
                # 使用原始标签
                pos_freq = word_df[word_df['content_type'] == 'pos'].groupby('word')['word'].count()
                pos_freq = pos_freq.sort_values(ascending=False)
                pos_wordcloud = self.generate_wordcloud(pos_freq) if not pos_freq.empty else self._create_default_wordcloud_image('positive')
                
                neg_freq = word_df[word_df['content_type'] == 'neg'].groupby('word')['word'].count()
                neg_freq = neg_freq.sort_values(ascending=False)
                neg_wordcloud = self.generate_wordcloud(neg_freq) if not neg_freq.empty else self._create_default_wordcloud_image('negative')
            
            return {
                'positive': pos_wordcloud,
                'negative': neg_wordcloud
            }
        except Exception as e:
            print(f"生成词云图时出错，使用默认图片: {e}")
            # 出错时返回默认图片
            return {
                'positive': self._create_default_wordcloud_image('positive'),
                'negative': self._create_default_wordcloud_image('negative')
            }


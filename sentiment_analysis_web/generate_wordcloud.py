"""
生成正负面评论的词云图片
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import jieba.posseg as psg
import os
import warnings
warnings.filterwarnings("ignore")

# 设置matplotlib后端
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

DATA_PATH = "data"
OUTPUT_PATH = "static/assets/img"

def generate_wordclouds():
    """生成正负面评论的词云"""
    # 读取数据
    csv_path = os.path.join(DATA_PATH, "reviews.csv")
    if not os.path.exists(csv_path):
        print(f"错误: 未找到数据文件 {csv_path}")
        return
    
    reviews = pd.read_csv(csv_path, encoding='utf-8')
    print(f"读取了 {len(reviews)} 条评论")
    
    # 删除重复记录
    reviews = reviews[['content', 'content_type']].drop_duplicates()
    content = reviews['content']
    
    # 去除英文、数字、京东、美的、电热水器等词语
    strinfo = re.compile('[0-9a-zA-Z]|京东|美的|电热水器|热水器|')
    content = content.apply(lambda x: strinfo.sub('', str(x)))
    
    # 分词
    worker = lambda s: [(x.word, x.flag) for x in psg.cut(str(s))]
    seg_word = content.apply(worker)
    
    # 将词语转为数据框形式
    n_word = seg_word.apply(lambda x: len(x))
    n_content = [[x+1]*y for x, y in zip(list(seg_word.index), list(n_word))]
    index_content = sum(n_content, [])
    seg_word = sum(seg_word, [])
    word = [x[0] for x in seg_word]
    nature = [x[1] for x in seg_word]
    
    content_type = [[x]*y for x, y in zip(list(reviews['content_type']), list(n_word))]
    content_type = sum(content_type, [])
    
    result = pd.DataFrame({
        "index_content": index_content,
        "word": word,
        "nature": nature,
        "content_type": content_type
    })
    
    # 删除标点符号
    result = result[result['nature'] != 'x']
    
    # 删除停用词
    stop_path = os.path.join(DATA_PATH, "stoplist.txt")
    if os.path.exists(stop_path):
        with open(stop_path, 'r', encoding='UTF-8') as f:
            stop = [line.replace('\n', '') for line in f.readlines()]
        word_set = set(word) - set(stop)
        result = result[result['word'].isin(word_set)]
    
    # 提取含有名词类的评论
    ind = result[['n' in str(x) for x in result['nature']]]['index_content'].unique()
    result = result[[x in ind for x in result['index_content']]]
    
    # 分离正负面评论
    pos_data = result[result['content_type'] == 'pos']
    neg_data = result[result['content_type'] == 'neg']
    
    # 设置字体路径（Windows）
    font_path = 'C:/Windows/Fonts/simsun.ttc'
    if not os.path.exists(font_path):
        font_path = 'C:/Windows/Fonts/msyh.ttc'  # 备用字体
    if not os.path.exists(font_path):
        font_path = None  # 如果都不存在，使用默认字体
    
    # 读取背景图片
    mask_path = os.path.join(DATA_PATH, "pl.jpg")
    if os.path.exists(mask_path):
        background_image = plt.imread(mask_path)
    else:
        background_image = None
    
    # 生成正面评论词云
    if len(pos_data) > 0:
        freq_pos = pos_data.groupby('word')['word'].count()
        freq_pos = freq_pos.sort_values(ascending=False)
        
        wordcloud = WordCloud(
            font_path=font_path,
            max_words=100,
            background_color='white',
            mask=background_image,
            width=800,
            height=600
        )
        pos_wordcloud = wordcloud.fit_words(freq_pos)
        
        # 保存图片
        output_file = os.path.join(OUTPUT_PATH, "正面词云.png")
        plt.figure(figsize=(10, 8))
        plt.imshow(pos_wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"正面词云已保存到: {output_file}")
    
    # 生成负面评论词云
    if len(neg_data) > 0:
        freq_neg = neg_data.groupby('word')['word'].count()
        freq_neg = freq_neg.sort_values(ascending=False)
        
        wordcloud = WordCloud(
            font_path=font_path,
            max_words=100,
            background_color='white',
            mask=background_image,
            width=800,
            height=600
        )
        neg_wordcloud = wordcloud.fit_words(freq_neg)
        
        # 保存图片
        output_file = os.path.join(OUTPUT_PATH, "负面词云.png")
        plt.figure(figsize=(10, 8))
        plt.imshow(neg_wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"负面词云已保存到: {output_file}")
    
    print("词云生成完成！")


if __name__ == '__main__':
    generate_wordclouds()


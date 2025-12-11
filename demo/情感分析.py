import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import jieba.posseg as psg

import matplotlib
matplotlib.use('TkAgg')  # 或者 'Qt5Agg', 'wxAgg', 'GTK3Agg' 等
import warnings
warnings.filterwarnings("ignore")

# %matplotlib inline

# path = '/home/kesci/input/emotion_analysi7147'
path = 'E:/pythonProject/情感分析/数据集/'
reviews = pd.read_csv(path+'/reviews.csv')
print(reviews.shape)
reviews.head()

# 删除数据记录中所有列值相同的记录
reviews = reviews[['content','content_type']].drop_duplicates()
content = reviews['content']

reviews.shape

# reviews

# 去除英文、数字、京东、美的、电热水器等词语
strinfo = re.compile('[0-9a-zA-Z]|京东|美的|电热水器|热水器|')
content = content.apply(lambda x: strinfo.sub('',x))

# 分词
worker = lambda s: [(x.word, x.flag) for x in psg.cut(s)] # 自定义简单分词函数
seg_word = content.apply(worker)

seg_word.head()
# 将词语转为数据框形式，一列是词，一列是词语所在的句子ID，最后一列是词语在该句子的位置
n_word = seg_word.apply(lambda x: len(x))  # 每一评论中词的个数

n_content = [[x+1]*y for x,y in zip(list(seg_word.index), list(n_word))]

# 将嵌套的列表展开，作为词所在评论的id
index_content = sum(n_content, [])

seg_word = sum(seg_word, [])
# 词
word = [x[0] for x in seg_word]
# 词性
nature = [x[1] for x in seg_word]

content_type = [[x]*y for x,y in zip(list(reviews['content_type']), list(n_word))]
# 评论类型
content_type = sum(content_type, [])

result = pd.DataFrame({"index_content":index_content,
                       "word":word,
                       "nature":nature,
                       "content_type":content_type})
result.head()

# 删除标点符号
result = result[result['nature'] != 'x']  # x表示标点符号

# 删除停用词
stop_path = open(path+"/stoplist.txt", 'r',encoding='UTF-8')
stop = stop_path.readlines()
stop = [x.replace('\n', '') for x in stop]
word = list(set(word) - set(stop))
result = result[result['word'].isin(word)]
result.head()

# 构造各词在对应评论的位置列
n_word = list(result.groupby(by = ['index_content'])['index_content'].count())
index_word = [list(np.arange(0, y)) for y in n_word]
# 词语在该评论的位置
index_word = sum(index_word, [])
# 合并评论id
result['index_word'] = index_word

result.head()
# 提取含有名词类的评论,即词性含有“n”的评论
ind = result[['n' in x for x in result['nature']]]['index_content'].unique()
result = result[[x in ind for x in result['index_content']]]
result.head()

import matplotlib.pyplot as plt
from wordcloud import WordCloud

frequencies = result.groupby('word')['word'].count()
frequencies = frequencies.sort_values(ascending = False)
backgroud_Image=plt.imread(path+'/pl.jpg')

# 自己上传中文字体到kesci
# font_path = '/home/kesci/work/data/fonts/MSYHL.TTC'
font_path='C:/Windows/Fonts/simsun.ttc'
wordcloud = WordCloud(font_path=font_path, # 设置字体，不设置就会出现乱码
                      max_words=100,
                      background_color='white',
                      mask=backgroud_Image)# 词云形状

my_wordcloud = wordcloud.fit_words(frequencies)
plt.imshow(my_wordcloud)
plt.axis('off')
plt.show()

# 将结果保存
result.to_csv("./word.csv", index = False, encoding = 'utf-8')

word = pd.read_csv("./word.csv")

# 读入正面、负面情感评价词
# pos_comment = pd.read_csv(path+"/正面评价词语（中文）.txt", header=None,sep="\n",
#                           encoding = 'utf-8', engine='python')
# 假设你的path变量已经正确设置
with open(path + "/正面评价词语（中文）.txt", 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
pos_comment_df = pd.DataFrame(lines, columns=['正面评价词语'])

with open(path + "/负面评价词语（中文）.txt", 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
neg_comment_df = pd.DataFrame(lines, columns=['正面评价词语'])

with open(path + "/正面评价词语（中文）.txt", 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
pos_emotion_df = pd.DataFrame(lines, columns=['正面评价词语'])

with open(path + "/负面评价词语（中文）.txt", 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
neg_emotion_df = pd.DataFrame(lines, columns=['负面评价词语'])

# 合并情感词与评价词
positive = set(pos_comment_df.iloc[:,0])|set(pos_emotion_df.iloc[:,0])
negative = set(neg_comment_df.iloc[:,0])|set(neg_emotion_df.iloc[:,0])

# 正负面情感词表中相同的词语
intersection = positive&negative

positive = list(positive - intersection)
negative = list(negative - intersection)

positive = pd.DataFrame({"word":positive,
                         "weight":[1]*len(positive)})
negative = pd.DataFrame({"word":negative,
                         "weight":[-1]*len(negative)})

posneg = positive.append(negative)


# 将分词结果与正负面情感词表合并，定位情感词
data_posneg = posneg.merge(word, left_on = 'word', right_on = 'word',
                           how = 'right')
data_posneg = data_posneg.sort_values(by = ['index_content','index_word'])

data_posneg.head()

# 载入否定词表
notdict = pd.read_csv(path + "/not.csv")

# 构造新列，作为经过否定词修正后的情感值
data_posneg['amend_weight'] = data_posneg['weight']
data_posneg['id'] = np.arange(0, len(data_posneg))

# 只保留有情感值的词语
only_inclination = data_posneg.dropna().reset_index(drop=True)

index = only_inclination['id']

for i in np.arange(0, len(only_inclination)):
    # 提取第i个情感词所在的评论
    review = data_posneg[data_posneg['index_content'] == only_inclination['index_content'][i]]
    review.index = np.arange(0, len(review))
    # 第i个情感值在该文档的位置
    affective = only_inclination['index_word'][i]
    if affective == 1:
        ne = sum([i in notdict['term'] for i in review['word'][affective - 1]]) % 2
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]
    elif affective > 1:
        ne = sum([i in notdict['term'] for i in review['word'][[affective - 1,
                                                                affective - 2]]]) % 2
        if ne == 1:
            data_posneg['amend_weight'][index[i]] = -data_posneg['weight'][index[i]]

# 更新只保留情感值的数据
only_inclination = only_inclination.dropna()

# 计算每条评论的情感值
emotional_value = only_inclination.groupby(['index_content'],
                                           as_index=False)['amend_weight'].sum()

# 去除情感值为0的评论
emotional_value = emotional_value[emotional_value['amend_weight'] != 0]

# 给情感值大于0的赋予评论类型（content_type）为pos,小于0的为neg
emotional_value['a_type'] = ''
emotional_value['a_type'][emotional_value['amend_weight'] > 0] = 'pos'
emotional_value['a_type'][emotional_value['amend_weight'] < 0] = 'neg'

emotional_value.head()

# 查看情感分析结果
result = emotional_value.merge(word,
                               left_on = 'index_content',
                               right_on = 'index_content',
                               how = 'left')
result.head()
result = result[['index_content','content_type', 'a_type']].drop_duplicates()
result.head()

# 交叉表:统计分组频率的特殊透视表
confusion_matrix = pd.crosstab(result['content_type'], result['a_type'],
                               margins=True)
confusion_matrix.head()

(confusion_matrix.iat[0,0] + confusion_matrix.iat[1,1])/confusion_matrix.iat[2,2]

# 提取正负面评论信息
ind_pos = list(emotional_value[emotional_value['a_type'] == 'pos']['index_content'])
ind_neg = list(emotional_value[emotional_value['a_type'] == 'neg']['index_content'])
posdata = word[[i in ind_pos for i in word['index_content']]]
negdata = word[[i in ind_neg for i in word['index_content']]]

# 绘制词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# 正面情感词词云
freq_pos = posdata.groupby('word')['word'].count()
freq_pos = freq_pos.sort_values(ascending = False)
backgroud_Image=plt.imread(path+'/pl.jpg')
wordcloud = WordCloud(font_path=font_path,
                      max_words=100,
                      background_color='white',
                      mask=backgroud_Image)
pos_wordcloud = wordcloud.fit_words(freq_pos)
plt.imshow(pos_wordcloud)
plt.axis('off')
plt.show()


# 负面情感词词云
freq_neg = negdata.groupby(by = ['word'])['word'].count()
freq_neg = freq_neg.sort_values(ascending = False)
neg_wordcloud = wordcloud.fit_words(freq_neg)
plt.imshow(neg_wordcloud)
plt.axis('off')
plt.show()

# 将结果写出,每条评论作为一行
posdata.to_csv("./posdata.csv", index = False, encoding = 'utf-8')
negdata.to_csv("./negdata.csv", index = False, encoding = 'utf-8')

reviews.head()

reviews['content_type'] = reviews['content_type'].map(lambda x:1.0 if x == 'pos' else 0.0)
reviews.head()

from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF  # 原始文本转化为tf-idf的特征矩阵
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

# 将有标签的数据集划分成训练集和测试集
train_X,valid_X,train_y,valid_y = train_test_split(reviews['content'],reviews['content_type'],test_size=0.2,random_state=42)

train_X.shape,train_y.shape,valid_X.shape,valid_y.shape

# 模型构建
model_tfidf = TFIDF(min_df=5, max_features=5000, ngram_range=(1,3), use_idf=1, smooth_idf=1)
# 学习idf vector
model_tfidf.fit(train_X)
# 把文档转换成 X矩阵（该文档中该特征词出现的频次），行是文档个数，列是特征词的个数
train_vec = model_tfidf.transform(train_X)
train_vec.toarray()
# 模型训练
model_SVC = LinearSVC()
clf = CalibratedClassifierCV(model_SVC)
clf.fit(train_vec,train_y)

# 把文档转换成矩阵
valid_vec = model_tfidf.transform(valid_X)
# 验证
pre_valid = clf.predict_proba(valid_vec)
pre_valid[:5]

pre_valid = clf.predict(valid_vec)
print('正例:',sum(pre_valid == 1))
print('负例:',sum(pre_valid == 0))
import matplotlib.pyplot as plt
import seaborn as sns

# 假设 pre_valid 是 clf.predict(valid_vec) 的结果，即预测的标签
# pre_valid_proba 是 clf.predict_proba(valid_vec) 的结果，即预测的概率

# 计算正例和负例的数量
positive_count = sum(pre_valid == 1)
negative_count = sum(pre_valid == 0)


# 或者使用饼图展示正例和负例的比例
plt.figure(figsize=(6, 6))
labels = ['Negative', 'Positive']
sizes = [negative_count, positive_count]
explode = (0.1, 0)  # 为了让其中一个部分稍微分离出来
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Percentage of Positive and Negative ')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix



# 计算混淆矩阵
cm = confusion_matrix(valid_y, pre_valid)

# 绘制热力混淆矩阵图
plt.figure(figsize=(6, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Negative', 'Positive'],
            yticklabels=['Negative', 'Positive'],
            cbar=False)  # 可以选择是否显示颜色条
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.title('Confusion Matrix')
plt.show()

from sklearn.metrics import accuracy_score

score = accuracy_score(pre_valid,valid_y)
print("准确率:",score)




import pandas as pd
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# 加载数据
pos_data = pd.read_csv('./posdata.csv')
neg_data = pd.read_csv('./negdata.csv')


pos_data['label'] = 1  # 积极情感标记为1
neg_data['label'] = 0  # 消极情感标记为0

combined_data = pd.concat([pos_data[['word', 'label']], neg_data[['word', 'label']]], ignore_index=True)

# 文本预处理：将文本转换为序列
max_features = 10000  # 词汇表大小
max_len = 100  # 文本最大长度

tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(combined_data['word'])

sequences = tokenizer.texts_to_sequences(combined_data['word'])
padded_sequences = pad_sequences(sequences, maxlen=max_len)

labels = to_categorical(combined_data['label'])

# 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)

# 构建LSTM模型
embedding_dim = 128
lstm_out = 128

model = Sequential()
model.add(Embedding(max_features, embedding_dim, input_length=max_len))
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2, activation='softmax'))

# 编译模型
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 训练模型
epochs = 10
batch_size = 32

model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), verbose=1)

# 评估模型
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Test loss: {loss}, Test accuracy: {accuracy}')


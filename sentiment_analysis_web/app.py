from flask import Flask, render_template
import sqlite3
import json
import os

app = Flask(__name__)

# 数据库路径
DB_PATH = "reviews.db"
DATA_PATH = "data"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/reviews')
def reviews():
    """显示评论列表"""
    datalist = []
    error_msg = None
    if os.path.exists(DB_PATH):
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            # 检查表是否存在
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'")
            if cur.fetchone():
                sql = "SELECT id, content, content_type, creationTime, nickname, referenceName FROM reviews ORDER BY id LIMIT 500"
                data = cur.execute(sql)
                for item in data:
                    datalist.append(item)
            else:
                error_msg = "数据库表不存在，请先运行 init_db.py 初始化数据库"
            cur.close()
            con.close()
        except Exception as e:
            error_msg = f"数据库查询错误: {str(e)}"
    else:
        error_msg = "数据库文件不存在，请先运行 init_db.py 初始化数据库"
    
    return render_template("reviews.html", reviews=datalist, error_msg=error_msg)


@app.route('/sentiment')
def sentiment():
    """情感分析统计"""
    pos_count = 0
    neg_count = 0
    total_count = 0
    sentiment_dist = {}
    error_msg = None
    
    if os.path.exists(DB_PATH):
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            
            # 检查表是否存在
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'")
            if cur.fetchone():
                # 统计正负面评论数量
                sql = "SELECT content_type, COUNT(*) FROM reviews GROUP BY content_type"
                data = cur.execute(sql)
                for item in data:
                    if item[0] == 'pos':
                        pos_count = item[1]
                    elif item[0] == 'neg':
                        neg_count = item[1]
                    sentiment_dist[item[0]] = item[1]
                    total_count += item[1]
            else:
                error_msg = "数据库表不存在，请先运行 init_db.py 初始化数据库"
            
            cur.close()
            con.close()
        except Exception as e:
            error_msg = f"数据库查询错误: {str(e)}"
    else:
        error_msg = "数据库文件不存在，请先运行 init_db.py 初始化数据库"
    
    # 准备图表数据
    labels = ['正面', '负面']
    values = [pos_count, neg_count]
    
    return render_template("sentiment.html", 
                         pos_count=pos_count, 
                         neg_count=neg_count,
                         total_count=total_count,
                         labels=labels,
                         values=values,
                         sentiment_dist=sentiment_dist,
                         error_msg=error_msg)


@app.route('/wordcloud')
def wordcloud():
    """词云展示"""
    import os
    pos_exists = os.path.exists("static/assets/img/正面词云.png")
    neg_exists = os.path.exists("static/assets/img/负面词云.png")
    return render_template("cloud.html", 
                         pos_wordcloud_exists=pos_exists,
                         neg_wordcloud_exists=neg_exists)


@app.route('/about')
def about():
    """关于页面"""
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)

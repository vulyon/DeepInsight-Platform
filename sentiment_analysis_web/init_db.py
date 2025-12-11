"""
初始化数据库，将CSV数据导入SQLite
"""
import sqlite3
import pandas as pd
import os

DB_PATH = "reviews.db"
CSV_PATH = "data/reviews.csv"


def init_db():
    """初始化数据库"""
    # 创建数据库连接
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建表
    sql = '''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            creationTime TEXT,
            nickname TEXT,
            referenceName TEXT,
            content_type TEXT
        )
    '''
    cursor.execute(sql)
    conn.commit()
    
    # 如果CSV文件存在，导入数据
    if os.path.exists(CSV_PATH):
        print(f"正在从 {CSV_PATH} 导入数据...")
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        
        # 清空表
        cursor.execute("DELETE FROM reviews")
        conn.commit()
        
        # 插入数据
        df.to_sql('reviews', conn, if_exists='append', index=False)
        print(f"成功导入 {len(df)} 条评论数据")
    else:
        print(f"警告: 未找到数据文件 {CSV_PATH}")
        print("请确保数据文件存在于 data/reviews.csv")
    
    cursor.close()
    conn.close()
    print("数据库初始化完成！")


if __name__ == '__main__':
    init_db()


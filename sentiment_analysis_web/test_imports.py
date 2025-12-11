# -*- coding: utf-8 -*-
"""
测试导入是否正常
"""
import sys
import io

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from flask import Flask, render_template
    print("[OK] Flask import successful")
except ImportError as e:
    print(f"[ERROR] Flask import failed: {e}")
    exit(1)

try:
    import sqlite3
    print("[OK] sqlite3 import successful")
except ImportError as e:
    print(f"[ERROR] sqlite3 import failed: {e}")

try:
    import pandas as pd
    print("[OK] pandas import successful")
except ImportError as e:
    print(f"[ERROR] pandas import failed: {e}")

try:
    import jieba
    print("[OK] jieba import successful")
except ImportError as e:
    print(f"[ERROR] jieba import failed: {e}")

try:
    from wordcloud import WordCloud
    print("[OK] wordcloud import successful")
except ImportError as e:
    print(f"[ERROR] wordcloud import failed: {e}")

print("\nAll necessary modules import test completed!")


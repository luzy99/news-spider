# %%
import matplotlib.pyplot as plt
import wordcloud
import sys
import pandas as pd
import numpy as np
from collections import Counter
import time
import jieba.analyse
import re
import pymysql
import os
os.chdir(os.path.dirname(__file__))
sys.path.append("..")
import settings


# %%
conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                       passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
cur = conn.cursor()
name = "orientaldaily"
'''
peoplenews
nytimes
orientaldaily
singtaousa
'''
ch_name = "东方日报"
'''
人民日报
纽约时报
东方日报
星岛日报
'''


def load_data(name):
    conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                           passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
    cur = conn.cursor()
    sql = "SELECT title,content,date,url FROM {}".format(name)
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    frame = pd.DataFrame(data, columns=['title', 'content', 'date', 'url'])
    frame['month'] = frame['date'].apply(lambda x: x.strftime('%Y-%m'))
    return frame


# %%
name = 'peoplenews'
frame = load_data(name)
total_lines = frame.loc[(frame["month"] <= "2020-02") & (frame["month"] >= "2019-02")]
opinion_lines = total_lines.loc[
    (total_lines["title"].str.contains("网评") |
     total_lines["title"].str.contains("评论") |
     total_lines["url"].str.contains("opinion"))]
opinion_lines.to_csv("%s_社评.csv" % name, index=False, sep=',')
print("%s: %d/%d" % (name, len(opinion_lines), len(total_lines)))

# %%
name = 'nytimes'
frame = load_data(name)
total_lines = frame.loc[(frame["month"] <= "2020-02") & (frame["month"] >= "2019-02")]
opinion_lines = total_lines.loc[
    (total_lines["title"].str.contains("网评") |
     total_lines["title"].str.contains("评论") |
     total_lines["url"].str.contains("opinion"))]
opinion_lines.to_csv("%s_社评.csv" % name, index=False, sep=',')
print("%s: %d/%d" % (name, len(opinion_lines), len(total_lines)))

# %%
name = 'orientaldaily'
frame = load_data(name)
total_lines = frame.loc[(frame["month"] <= "2020-02") & (frame["month"] >= "2019-02")]
opinion_lines = total_lines.loc[
    (total_lines["url"].str.contains("00186") |
        total_lines["url"].str.contains("00190") |
        total_lines["url"].str.contains("00182") |
        total_lines["url"].str.contains("00184") |
        total_lines["url"].str.contains("00192") |
        total_lines["url"].str.contains("00273"))]
opinion_lines.to_csv("%s_社评.csv" % name, index=False, sep=',')
print("%s: %d/%d" % (name, len(opinion_lines), len(total_lines)))

# %%
name = 'singtaousa'
frame = load_data(name)
total_lines = frame.loc[(frame["month"] <= "2020-02") & (frame["month"] >= "2019-02")]
opinion_lines = total_lines.loc[
    (total_lines["url"].str.contains("00186") |
        total_lines["url"].str.contains("00190") |
        total_lines["url"].str.contains("00182") |
        total_lines["url"].str.contains("00184") |
        total_lines["url"].str.contains("00192") |
        total_lines["url"].str.contains("00273"))]
# opinion_lines.to_csv("%s_社评.csv" % name, index=False, sep=',', encoding="gbk")
print("%s: %d/%d" % (name, len(opinion_lines), len(total_lines)))

# %%
name = 'std.stheadline.com'
conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                        passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
cur = conn.cursor()
sql = "SELECT keyword,url FROM google WHERE site = '{}'".format(name)
cur.execute(sql)
data = cur.fetchall()
cur.close()
conn.close()
frame = pd.DataFrame(data, columns=['keyword', 'url'])
total_lines = frame.loc[frame["url"].str.contains("article")]
opinion_lines = total_lines.loc[
    (total_lines["url"].str.contains("%E7%A4%BE%E8%AB%96"))]
opinion_lines.to_csv("%s_社评.csv" % name, index=False, sep=',')
print("%s: %d/%d" % (name, len(opinion_lines)+37, len(total_lines)))

# %%
import os
os.chdir(os.path.dirname(__file__))
import pymysql
import re
import jieba.analyse
import time
from collections import Counter
import numpy as np
import pandas as pd
import sys
import wordcloud
import re
import matplotlib.pyplot as plt
sys.path.append("..")
import settings


# %%
conn = pymysql.connect(host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                       passwd=settings.MYSQL_PASSWD, db=settings.MYSQL_DBNAME, charset='utf8')
cur = conn.cursor()
name = "peoplenews"
'''
peoplenews
nytimes
orientaldaily
singtaousa
'''
ch_name = "人民日报"
'''
人民日报
纽约时报
东方日报
星岛日报
'''
sql = "SELECT title,content,date FROM {}".format(name)
cur.execute(sql)
data = cur.fetchall()
cur.close()
conn.close()

# %%
frame = pd.DataFrame(data, columns=['title', 'content', 'date'])
# %%
all_content = ''
all_title = ''
for line in data:
    all_content += line[1] + " "
    all_title += line[0] + " "

# %% 结巴分词
sentence = all_title + all_content
# 只保留中文
pat = re.compile("[\u4e00-\u9fa5]+")
sentence = " ".join(pat.findall(sentence))
jieba.load_userdict('./userdict.txt')
jieba.analyse.set_stop_words('./stopwords_cn.txt')

hot_words = []

weight = []
# tf-idf 词频分析
for x, w in jieba.analyse.extract_tags(sentence, topK=100, withWeight=True):
    print('%s %s' % (x, w))
    hot_words.append(x)
    weight.append(w)
# %%    词频统计
seg_list = jieba.cut(sentence)
c = Counter()
for x in seg_list:
    if len(x) > 1 and x != '\r\n':
        c[x] += 1

word_freq = []
hot_word2 = []
for (k, v) in c.most_common(100):
    hot_word2.append(k)
    word_freq.append(v)
    pass
    # print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*'*int(v/3), v))

# %% 词云
word_str = ' '.join(hot_words)
w = wordcloud.WordCloud(width=1000, height=700,
                        background_color='white', font_path="msyh.ttc")
w.generate(word_str)
w.to_file('output/%s_wordcloud.png' % name)
# %%    权重
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.bar(hot_words[:10], weight[:10], label='权重')
plt.legend()
plt.xticks(size=9, rotation=30)
plt.grid(axis="y")
plt.title("%s新闻报道词频统计图" % ch_name)
plt.savefig('output/%s_wordweight.png'%name, dpi=300)
# %%    词频
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.bar(hot_word2[:10], word_freq[:10], label='词频')
plt.legend()
plt.xticks(size=9, rotation=30)
plt.title("%s新闻报道词频统计图" % ch_name)
plt.grid(axis="y")
plt.savefig('output/%s_wordfreq.png'% name, dpi=300)

# %% 月份统计
frame['month'] = frame['date'].apply(lambda x: x.strftime('%Y-%m'))
month_distr = frame["month"].loc[frame["month"] <= "2020-02"].value_counts().sort_index()
# month_distr = frame["month"].value_counts().sort_index()
# %%
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.plot(month_distr.index, month_distr, label='报道数量')
plt.legend()
plt.title("%s新闻报道数量月份统计图" % ch_name)
plt.xticks(size=9, rotation=30)
plt.grid(axis="y")
plt.savefig('output/%s_month.png' % name, dpi=300)
# %%主体对象出现频率
subjects = []
with open('./subject.txt',encoding='utf8') as f:
    for line in f.readlines():
        subjects.append(line.strip().split(','))
print(subjects)
# %%
sub_count = []
for subject in subjects:
    pat = re.compile("|".join(subject))
    match = pat.findall(sentence)
    sub_count.append(len(match))
plt_list =zip(sub_count,[x[0] for x in subjects])
plt_list=sorted(plt_list,key=lambda x:x[0],reverse=True)

# %% 绘制饼图
import brewer2mpl
bmap = brewer2mpl.get_map('Set3', 'qualitative', 10)
colors = bmap.mpl_colors
plt.figure()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.pie(sub_count, labels=[x[0] for x in subjects], colors=colors,autopct='%1.1f%%',startangle=30,pctdistance=0.8,rotatelabels=False,radius=1.2)

# plt.pie([x[0] for x in plt_list], labels=[x[1] for x in plt_list], colors=colors,autopct='%1.1f%%',startangle=0)
# plt.legend()
plt.title("%s新闻主体频率分布图" % ch_name)

plt.savefig('output/%s_subjects.png' % name, dpi=300)
print(plt_list)
with open('output/%s_subjects_list.txt' % name, 'w', encoding='utf8') as f:
    for i in plt_list:
        f.write('%d, %s\n' % i)
# %%

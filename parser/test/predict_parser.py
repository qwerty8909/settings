import os
import time

import pandas as pd

from predict_parser import championat, ironbets, liveresult, stavkionline
from predict_parser import stavkiprognozy, vseprosport, odds, metaratings
from predict_parser import sportsru, soccer365, bookmakerratings

path = r"/home/project/data/" #r'C:\Users\vitalii\IdeaProjects\settings\parser\test\data\\'
now = time.time()

for f in os.listdir(path):
    f = os.path.join(path, f)
    if os.stat(f).st_mtime < now - 2 * 86400:
        if os.path.isfile(f):
            os.remove(os.path.join(path, f))

df1 = pd.DataFrame(championat.news_parser())
df2 = pd.DataFrame(ironbets.news_parser())
df3 = pd.DataFrame(liveresult.news_parser())
df4 = pd.DataFrame(stavkionline.news_parser())
df5 = pd.DataFrame(stavkiprognozy.news_parser())
df6 = pd.DataFrame(vseprosport.news_parser())
df7 = pd.DataFrame(odds.news_parser())
df8 = pd.DataFrame(metaratings.news_parser())
df9 = pd.DataFrame(sportsru.news_parser())
df10 = pd.DataFrame(soccer365.news_parser())
df11 = pd.DataFrame(bookmakerratings.news_parser())
df_base = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11], ignore_index=True)
# print('championat       - ', df1.shape[0])
# print('ironbets         - ', df2.shape[0])
# print('liveresult       - ', df3.shape[0])
# print('stavkionline     - ', df4.shape[0])
# print('stavkiprognozy   - ', df5.shape[0])
# print('vseprosport      - ', df6.shape[0])
# print('odds             - ', df7.shape[0])
# print('metaratings      - ', df8.shape[0])
# print('sportsru         - ', df9.shape[0])
# print('soccer365        - ', df10.shape[0])
# print('bookmakerratings - ', df11.shape[0])
# print('all              - ', df_base.shape[0])
df_base.to_csv(path + str(int(now)) + '.csv', index=False, sep=';', encoding='utf-8-sig')

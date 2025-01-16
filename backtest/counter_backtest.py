
import pandas as pd
import numpy as np

#테스트 파일 로딩
df_org = pd.read_csv('./data/XRPUSDT_index.csv')
# print(df_org.shape)
# print(df_org.columns)

#변수 선언
open_long_cnt = 0 
open_long_price = 0
open_long_amt = 0
open_short_cnt = 0
open_short_price = 0
open_short_amt = 0
momentum = ''
revenue = 0
revenue_t = 0

df = df_org.iloc[df_org.shape[0]-144000:,] #테스트 데이터 선택 100, 1440, 14400, 144000, 전체
for i in range(0, df.shape[0]-1):
    
    close2 = round(df.iloc[i+1:i+2,]['close'].values[0],4) #다음 분 종가: 매매 기준 가격
    w7 = round(df.iloc[i:i+1,]['wma7'].values[0],4)
    w25 = round(df.iloc[i:i+1,]['wma25'].values[0],4)
    w99 = round(df.iloc[i:i+1,]['wma99'].values[0],4)
    
    #close long position
    if momentum == 'long' and open_long_cnt > 0 and w7 < w25:
        revenue_t = close2*open_long_amt - open_long_price
        revenue = revenue + revenue_t
        open_long_cnt = 0
        open_long_amt = 0
        open_long_price = 0
        momentum = ''
        continue
    
    #close short position
    if momentum == 'short' and open_short_cnt > 0 and w7 > w25:
        revenue_t = open_short_price - close2*open_short_amt
        revenue = revenue + revenue_t
        open_short_cnt = 0
        open_short_amt = 0
        open_short_price = 0
        momentum = ''
        continue
    
    #open long position
    if momentum != 'short' and open_long_cnt < 4 and w7 > w25 and w25 > w99: 
        open_long_amt = round(open_long_amt + (1-open_long_cnt*0.25),4)
        open_long_price = round(open_long_price + close2*(1-open_long_cnt*0.25),4)
        open_long_cnt = open_long_cnt + 1        
        momentum = 'long'
        
    #open short position
    if momentum != 'long' and open_short_cnt < 4 and w7 < w25 and w25 < w99: 
        open_short_amt = round(open_short_amt + (1-open_short_cnt*0.25),4)
        open_short_price = round(open_short_price + close2*(1-open_short_cnt*0.25),4)
        open_short_cnt = open_short_cnt + 1        
        momentum = 'short'

    #monitoring log
#     print("c:{} w7:{} w25:{} w99:{} olc:{} ola:{} olp:{} osc:{} osa:{} osp:{} revenue:{:0.4f}"
#           .format(close2, w7, w25, w99, open_long_cnt, open_long_amt, open_long_price, 
#                   open_short_cnt, open_short_amt, open_short_price, revenue))

#print total revenue
print(revenue)

 
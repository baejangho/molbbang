import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator # RSI 계산 클래스
from ta.momentum import StochRSIIndicator # StochRSI 계산 클래스
from ta.volatility import BollingerBands # 볼린저밴드 계산 클래스

df = pd.read_csv('./data/XRPUSDT.csv') # 저장한 데이터 불러오기

## RSI 계산
df['rsi6'] = RSIIndicator(df['close'], window=6).rsi()
df['rsi12'] = RSIIndicator(df['close'], window=12).rsi()
df['rsi24'] = RSIIndicator(df['close'], window=24).rsi()
# print(df.head(10))

## StochRSI 계산
stochRSI = StochRSIIndicator(df['close'], window=14, smooth1=3, smooth2=3)
df['srsi'] = stochRSI.stochrsi()
df['srsik'] = stochRSI.stochrsi_k()
df['srsid'] = stochRSI.stochrsi_d()
# print(df.tail(10))

## 볼린저밴드 계산
bb = BollingerBands(df['close'], window=20, window_dev=2)
df['bh'] = bb.bollinger_hband() #high band
df['bhi'] = bb.bollinger_hband_indicator() #현재 가격이 high band 보다 가격이 높으면 1, 아니면 0
df['bl'] = bb.bollinger_lband() #low band
df['bli'] = bb.bollinger_lband_indicator() #현재 가격이 low band 보다 가격이 낮으면 1, 아니면 0
df['bm'] = bb.bollinger_mavg() #middle band
df['bw'] = bb.bollinger_wband() #band width
df.tail(10)

## 데이터 저장(null 값 제거)
df = df.dropna()
print(df.columns) # 컬럼명 확인
df.to_csv('./data/XRPUSDT_index.csv', index=False)
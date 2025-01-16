import pandas as pd
import numpy as np
from ta.trend import SMAIndicator
from ta.trend import WMAIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.momentum import StochRSIIndicator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice

df = pd.read_csv('./data/XRPUSDT.csv')
# print(df)

##### 단순 이동평균 계산
df['sma7'] = SMAIndicator(df['close'], window=7).sma_indicator()
df['sma25'] = SMAIndicator(df['close'], window=25).sma_indicator()
df['sma99'] = SMAIndicator(df['close'], window=99).sma_indicator()

##### 가중 이동평균 계산
df['wma7'] = WMAIndicator(df['close'], window=7).wma()
df['wma25'] = WMAIndicator(df['close'], window=25).wma()
df['wma99'] = WMAIndicator(df['close'], window=99).wma()

##### 지수 이동평균 계산
df['ema7'] = EMAIndicator(df['close'], window=7).ema_indicator()
df['ema25'] = EMAIndicator(df['close'], window=25).ema_indicator()
df['ema99'] = EMAIndicator(df['close'], window=99).ema_indicator()

##### MACD 계산
macd = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
df['macd'] = macd.macd()
df['macd_s'] = macd.macd_signal()
df['macd_d'] = macd.macd_diff()

##### RSI 계산
df['rsi6'] = RSIIndicator(df['close'], window=6).rsi()
df['rsi12'] = RSIIndicator(df['close'], window=12).rsi()
df['rsi24'] = RSIIndicator(df['close'], window=24).rsi()

##### StochRSI 계산
stochRSI = StochRSIIndicator(df['close'], window=14, smooth1=3, smooth2=3)
df['srsi'] = stochRSI.stochrsi()
df['srsik'] = stochRSI.stochrsi_k()
df['srsid'] = stochRSI.stochrsi_d()

##### Bollinger Bands 계산
bb = BollingerBands(df['close'], window=20, window_dev=2)
df['bh'] = bb.bollinger_hband() #high band
df['bhi'] = bb.bollinger_hband_indicator() #high band 보다 가격이 높으면 1, 아니면 0
df['bl'] = bb.bollinger_lband() #low band
df['bli'] = bb.bollinger_lband_indicator() #low band 보다 가격이 낮으면 1, 아니면 0
df['bm'] = bb.bollinger_mavg() #middle band
df['bw'] = bb.bollinger_wband() #band width

##### VWAP 계산
vwap = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=14)
df['vwap7'] = vwap.volume_weighted_average_price()

df = df.dropna()
df.to_csv('./data/XRPUSDT_index.csv', index=False)
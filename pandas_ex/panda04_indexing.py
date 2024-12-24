## 데이터 프레임에 든 데이터를 인덱싱하는 방법
## 레이블 인덱싱(loc()), 위치 인덱싱(iloc())
## 훈련 데이터와 테스트 데이터로 나누기
import pandas as pd
import numpy as np

## 레이블 인덱싱
df = pd.DataFrame(np.random.randn(5, 4), index=pd.date_range('20210101',periods=5), columns=["a", "b", "c","d"])
# pd.date_range() 함수는 날짜를 생성하는 함수
# print("df:\n",df,"\n")
df1 = df.loc['20210102':'20210104',:"c"]
# print("df1:\n",df1,"\n")
df2 = df.loc[:'20210102',["a","c"]]
# print("df2:\n",df2,"\n")

## 조건으로 인덱싱
df3 = df.loc['2021-01-03']>0.1
# print("df3:\n",df3,"\n")
df4 = df.loc[:,df3]
# print("df4:\n",df4,"\n")

## 위치 인덱싱
df = pd.DataFrame(np.random.randn(5, 4), index=pd.date_range('20210101',periods=5), columns=["a", "b", "c","d"])
print("df:\n",df,"\n")
df1 = df.iloc[1:3,1:3]
print("df1:\n",df1,"\n")
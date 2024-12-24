## 프레임 자체 가공 기술
## axis=0은 행을 기준으로, axis=1은 열을 기준으로 한다.
import pandas as pd
import numpy as np

## 데이터 프레임의 결합
data1 = [[1,3,5,7,9,11],[2,4,6,8,10,12]]
df1 = pd.DataFrame(data1, index=[0,1], columns=[1,2,3,4,5,6])
data2 = [[1,3,5,7,9,11],[2,4,6,8,10,12]]
## 행렬 결합에서 데이터 프레임의 인덱스를 사용함
df2 = pd.DataFrame(data2, index=[2,3], columns=[1,2,3,4,5,6])
data3 = [[1,3,5,7],[2,4,6,8]]
df3 = pd.DataFrame(data3, index=[0,1], columns=[1,2,3,4])
df4 = pd.concat([df1, df2], axis=1)
# print(df4)
df5 = pd.concat([df2, df3], axis=1)
# print(df5)
df6 = pd.concat([df1, df3], axis=0)
# print(df6)
df7 = pd.concat([df1, df3], axis=1)
# print(df7)
## 데이터 프레임의 병합
## 키를 중심으로 데이터 프레임을 결합
data1 = [["K0","a0","b0"],
         ["K1","a1","b1"],
         ["K2","a2","b2"],
         ["K3","a3","b3"]]   
df1 = pd.DataFrame(data1, columns=["Key","a","b"])
data2 = [["K0","c0","d0"],
         ["K1","c1","d1"],
         ["K2","c2","d2"]]   
df2 = pd.DataFrame(data2, columns=["Key","c","d"])
result1 = pd.merge(df1, df2, how="outer", on="Key")
print(result1)


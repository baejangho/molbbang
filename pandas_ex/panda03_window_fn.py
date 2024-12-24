## 윈도함수 : 이동평균 개념
## 움직이는 부분 데이터에 대한 평균, 최댓값, 최솟값 등을 구할 때 사용
## rolling() 함수를 사용 : 지속적으로 윈도우를 이동시키면서 통계량을 계산
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
print(df)
df["a_sum"] = df["a"].rolling(window=3, min_periods=1).sum()
df["a_mean"] = df["a"].rolling(window=3).mean()
print(df)



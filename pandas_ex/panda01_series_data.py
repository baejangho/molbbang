import pandas as pd
import numpy as np

# Series 객체 생성
s1 = pd.Series([1, 3, 5, np.nan, "a", "b"])
print(s1)
# Series 객체 생성 (index 지정)
s2 = pd.Series([1, 3, 5, np.nan, "a", "b"], index=["A", "B", "C", "D", "E", "F"])
print(s2)
# data frame 객체 생성
data = [[1,3,5,7,9,11], 
        [2,4,5,1,2,3]]
idx = np.array(range(2))
print(idx)
s3 = pd.DataFrame(data,index=idx,columns=["C1","C2","C3","C4","C5","C6"])
print(s3)
s3.info()
print(s3.shape)
print(s3.describe())
print(s3.head(1))
print(s3.tail(1))
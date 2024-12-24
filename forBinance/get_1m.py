##### 총 x일치 1분봉 데이터 받아오는 코드 #####

import time
import datetime
import pandas as pd
import requests
import json
import os

## 밀리세컨드 시간을 일반 시간으로 변환하는 함수 : 확인용
def get_date(mili_time):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time / 1000.0, tz=KST)
    timeline = str(dt.strftime('%D %H:%M:%S'))  #(1) 출력형식 지정
    return timeline  

# (0) 가져올 데이터 총 일수(x) 선택 및 x일 전 타임스탬프 설정
x = 10
gettimestamp = int(time.time() - 60*60*24 * x)*1000 

# 120일치 1분 데이터 1000개씩 요청하는 URL
base_url = "https://www.binance.com/fapi/v1/klines?symbol=XRPUSDT"+\
    "&interval=1m&limit=1000&startTime={}"

#(1) 데이터 건수 설정 1일=24시간=1440초 1000개씩 받기=1.4배 
# ex)120일*1.4=168회 for문 돌리기
df_candle = pd.DataFrame() # 데이터프레임 초기화
for i in range(int(x*1.4)+1): 
    
    #(2)url의 데이터 요청 설정
    url = base_url.format(gettimestamp)
    webpage = requests.get(url)
    
    #(3)JSON 형식 데이터 읽어서 임시 데이터프레임에 저장
    str_data = webpage.content.decode('utf-8')
    json_data = json.loads(str_data)
    df_candle_temp = pd.DataFrame(json_data)

    #(4) 새로받은 데이터를 기존 데이터프레임과 병합
    df_candle = pd.concat([df_candle,df_candle_temp],axis=0) 
    
    #(5)마지막 타임스탬프 추출
    gettimestamp = df_candle_temp[0][-1:].values[0] 
    print(get_date(gettimestamp)) # (6)출력형식 지정

#(6)컬럼명 수정 및 한국시간으로 변경
rename_columns = {0: 'time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}
df_candle = df_candle[[0, 1, 2, 3, 4, 5]].rename(columns=rename_columns)
KST = datetime.timezone(datetime.timedelta(hours=9))
df_candle['time'] = pd.to_datetime(df_candle['time'], unit='ms', utc=True).dt.tz_convert(KST)

#(7)널 데이터 삭제
df_candle = df_candle.dropna(axis=0)

#(8)파일로 저장
output_dir = "./data"
# data 폴더가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
df_candle.to_csv("./data/BTCUSDT.csv", index=False)

# 최종 타임스탬프 확인   
gettimestamp = df_candle['time'][-1:].values[0] 
print(get_date(1734549300000))
import pandas as pd
import datetime
import time
import requests
import os

#타임스템프에서 초 추출
def get_time_ss(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%S'))
    return timeline

#타임스템프에서 분 추출
def get_time_mm(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%M'))
    return timeline

#타임스템프에서 시간 추출
def get_time_hhmmss(mili_time):
    mili_time = float(mili_time)
    KST = datetime.timezone(datetime.timedelta(hours=9))
    dt = datetime.datetime.fromtimestamp(mili_time, tz=KST)
    timeline = str(dt.strftime('%D %H:%M:%S'))
    return timeline

#로그 기록
def log_info(message):
    print("{}".format(message))

#1분 데이터 가져오기
def get_web_1m_data(days, granularity, symbol="BTCUSDT_UMCBL"):
    '''
    bitget에서 캔들 데이터 가져오는 함수
    args:
        days(int): 가져올 데이터 일수
        granularity(int): 캔들 단위 예: 60(1분봉), 300(5분봉), 900(15분봉), 1800(30분봉), 3600(1시간봉), 14400(4시간봉), 86400(1일봉)
        symbol(str): 코인 심볼(기본값 : BTCUSDT_UMCBL)
    '''
    # 현재 시간 기준으로 days 일 전 타임스탬프 계산
    since = int((datetime.datetime.now() - datetime.timedelta(days=days)).timestamp() * 1000)
    
    # 데이터프레임 초기화
    df_all = pd.DataFrame()
    
    # 요청 파라미터
    url = "https://api.bitget.com/api/mix/v1/market/candles"
    params = {
        "symbol": "BTCUSDT_UMCBL",  # 심볼: 비트코인/USDT
        "granularity": 60,          # 1분봉 (60초 단위)
        "startTime": 1672444800000, # 시작 시간 (밀리초)
        "endTime": 1672448400000    # 종료 시간 (밀리초)
    }
    
    while True:
        df = fetch_ohlcv(symbol, timeframe=timeframe, since=since)
        if df.empty:
            break
        df_all = pd.concat([df_all, df], axis=0)
        since = int(df['timestamp'].iloc[-1].timestamp() * 1000) + 1  # 마지막 타임스탬프 이후부터 가져오기

        # Bitget API rate limit을 피하기 위해 잠시 대기
        bitget.sleep(10)

    # 중복된 행 제거
    df_all.drop_duplicates(subset='timestamp', keep='first', inplace=True)
    
    # CSV 파일로 저장
    output_dir = "./data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, f"{symbol.replace('/', '_')}_1m_{days}d.csv")
    df_all.to_csv(output_file, index=False)
    print(f"CSV 파일로 저장 완료: {output_file}")
    
    

    # API 요청 (Public API라 인증 불필요)
    response = requests.get(url, params=params)

    # 결과 출력
    print(response.json())
    return '작성할 것'

#오픈건수 계산
def check_open_cnt(check_data, amt_list):
    idx = 1
    for data in amt_list:
        if round(check_data,0) == round(data,0):
            return idx
        idx = idx + 1
    return idx

#단계별 구매 수량
def get_open_amt_list(open_amt_unit, open_cnt_limit, increace_rate):
    open_amt = 0
    open_amt_list = [0.0]
    for idx in range(0, open_cnt_limit):
        temp_amt = open_amt_unit + open_amt * increace_rate
        open_amt = round(open_amt + temp_amt, 4)
        open_amt_list.append(open_amt)
    return open_amt_list

#손실 최소화 실현 금액
def get_max_loss(close, open_amt_unit, open_cnt_limit, increace_rate, max_loss_rate):
    open_amt = 0
    open_price = 0
    for idx in range(0, open_cnt_limit):
        temp_amt = open_amt_unit + open_amt * increace_rate
        open_price = round(open_price + close * temp_amt, 4)
        open_amt = round(open_amt + temp_amt, 4)
    return round(open_price/open_amt * max_loss_rate, 4)


if __name__ == "__main__":
    get_web_1m_data(10)
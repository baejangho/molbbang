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

#캔들 데이터 가져오기
def get_web_1m_data(days, granularity, symbol="BTCUSDT_UMCBL"):
    '''
    bitget에서 캔들 데이터 가져오는 함수
    args:
        days(int): 가져올 데이터 일수
        granularity(int): 캔들 단위 예: 60(1분봉), 300(5분봉), 900(15분봉), 1800(30분봉), 3600(1시간봉), 14400(4시간봉), 86400(1일봉)
        symbol(str): 코인 심볼(기본값 : BTCUSDT_UMCBL)
    '''
    # 요청 url
    url = "https://api.bitget.com/api/mix/v1/market/candles"
    # 현재 시간(밀리초)
    current_time = int(time.time() * 1000)
    # 요청 시작 시간(days일 전)
    start_time = current_time - (days * 24 * 60 * 60 * 1000)
    # 1,000개의 캔들 데이터 범위(최대 1,000개의 데이터 요청, 밀리초 단위)
    max_interval = 1000 * granularity * 1000 # 개 * 초 * 밀리초
    # 현재 시간 기준으로 days 일 전 타임스탬프 계산
    since = int((datetime.datetime.now() - datetime.timedelta(days=days)).timestamp() * 1000)
    
    # 데이터프레임 초기화
    # df = pd.DataFrame()
    df_all = pd.DataFrame()
    
    # 데이터 반복 요청(1000개씩)
    while start_time < current_time:
        # 요청 파라미터
        print(pd.to_datetime(start_time, unit='ms').tz_localize('UTC').tz_convert('Asia/Seoul'))
        end_time = min(start_time + max_interval, current_time)
        params = {
            "symbol": symbol,           # 심볼: 비트코인/USDT
            "granularity": granularity, # 캔들 단위
            "startTime": start_time,    # 시작 시간 (밀리초)
            "endTime": end_time,    # 종료 시간 (밀리초)
            "limit": "1000"        # 최대 1000개 데이터 요청
        }
        # API 요청 (Public API라 인증 불필요)
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(data)
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume','turnover'])
            df['timestamp'] = df['timestamp'].astype(int)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df[['open', 'high', 'low', 'close', 'volume','turnover']] = df[['open', 'high', 'low', 'close', 'volume','turnover']].astype(float)
            df_all = pd.concat([df_all, df], axis=0)
            # 다음 데이터 요청을 위한 시작 시간 설정
            start_time = end_time + 1
            # Bitget API rate limit을 피하기 위해 잠시 대기
            time.sleep(1)
        else:
            print(f"API 요청 에러: {response.status_code}")
    
    # 중복된 행 제거
    df_all.drop_duplicates(subset='timestamp', keep='first', inplace=True)
    
    # CSV 파일로 저장
    output_dir = "./data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, f"{symbol.replace('/', '_')}_1m_{days}d.csv")
    df_all.to_csv(output_file, index=False)
    print(f"CSV 파일로 저장 완료: {output_file}")
    
    return df_all


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
    get_web_1m_data(32,60)
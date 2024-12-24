import ccxt
import pandas as pd
import datetime
import os

# Bitget API 키와 시크릿 키 설정
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET_KEY'
symbol = 'BTC/USDT:USDT'  # Bitget 무기한 선물 계약 심볼

# config 가져올 데이터 일수 설정
days = 10

# ccxt Bitget 객체 생성
bitget = ccxt.bitget({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
})

# 1분봉 데이터 가져오기
def fetch_ohlcv(symbol, timeframe='1m', since=None, limit=1000):
    ohlcv = bitget.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# 10일치 1분봉 데이터 가져오기 및 CSV 파일로 저장
def fetch_and_save_ohlcv(symbol, days=10, timeframe='1m'):
    # 현재 시간 기준으로 10일 전 타임스탬프 계산
    since = int((datetime.datetime.now() - datetime.timedelta(days=days)).timestamp() * 1000)
    
    # 데이터프레임 초기화
    df_all = pd.DataFrame()

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

# 예제 실행
if __name__ == "__main__":
    fetch_and_save_ohlcv(symbol, days=10, timeframe='1m')
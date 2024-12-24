import ccxt.pro as ccxt
from asyncio import run

print('CCXT Version:', ccxt.__version__)

async def main():
    # Bitget 거래소 객체 생성
    exchange = ccxt.pro.bitget({
        'options': {
            'defaultType': 'swap',  # spot, swap, future
        },
    })

    symbol = 'BTC/USDT'
    while True:
        try:
            # Bitget의 orderbook을 구독
            orderbook = await exchange.watch_order_book(symbol)
            print(
                exchange.iso8601(exchange.milliseconds()),
                exchange.id,
                symbol,
                'ask:', orderbook['asks'][0],
                'bid:', orderbook['bids'][0]
            )
        except Exception as e:
            print(type(e).__name__, str(e))
            break
    await exchange.close()


run(main())
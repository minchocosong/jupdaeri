"""
암호화폐 자동매매프로그램
"""
import json
from common import telegram_bot, CHAT_ID
from exchange_apis import get_balance, buy_market_order, buy_limit_order, sell_market_order
from quotation_apis import get_markets
from strategy.sungjin import Sungjin


def get_available_krw(account_list):
    """
    매수가능 한화 금액
    """
    bal = [curr['balance'] for curr in account_list if curr['currency'] == 'KRW']
    return bal[0] if len(bal) > 0 else 0


# 자산 조회
balance = get_balance()
print(balance)

# 매수 가능 한화
krw_balance = get_available_krw(balance)
print(krw_balance)

# 마켓 종목 조회
market_list = get_markets(fiat="KRW")
print(len(market_list))

# [조건1] 7일 전 장대양봉 출현여부 확인
sungjin = Sungjin()
result_list = sungjin.get_codes_have_big_plus_candle(market_list)

print(result_list)

#buy_market_order("KRW-PCI", 5000)
#buy_limit_order("KRW-PCI", 500, 10)
sell_market_order("", 0)
telegram_bot.send_message(CHAT_ID, json.dumps(result_list, ensure_ascii=False))

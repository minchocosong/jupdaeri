import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import telegram
import logging

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

telegram_access_token = os.environ['TELEGRAM_BOT_ACCESS_TOKEN']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}
chat_id = '948219871'


def upbit_request(sub_url, querystring):
    if querystring == {}:
        return requests.get(server_url + sub_url, headers=headers)
    return requests.get(server_url + sub_url, params=querystring, headers=headers)


def get_all_market_codes():
    market_list = []
    res = upbit_request("/v1/market/all", {})
    if res.status_code == 200:
        for market in res.json():
            market_list.append({'code': market['market']})
    else:
        logger.log(level=4, msg='마켓 정보 조회 실패')

    return market_list


def get_codes_have_big_plus_candle(market_list):
    result_list = []
    total_count = 0
    for market in market_list:
        if not market['code'].startswith("KRW"):
            continue
        querystring = {"count": 9, "market": market['code'], "convertingPriceUnit": "KRW"}
        res = upbit_request("/v1/candles/days", querystring)
        if res.status_code == 200:

            result = res.json()

            # 8일 전 캔들
            candle_before_8_day = result[-2]
            candle_before_8_day_size = abs(candle_before_8_day['opening_price'] - candle_before_8_day['trade_price']) # 상하폭(몸통)
            candle_before_8_day_volumn = candle_before_8_day['candle_acc_trade_volume']

            # 7일 전 캔들
            candle_before_7_day = result[-3]
            candle_before_7_day_size = abs(candle_before_7_day['opening_price'] - candle_before_7_day['trade_price'])  # 상하폭(몸통)
            candle_before_7_day_volumn = candle_before_7_day['candle_acc_trade_volume']

            # 양봉 여부
            is_plus = candle_before_7_day['trade_price'] > candle_before_7_day['opening_price']
            # 8일전 대비 상하폭 2배 이상 여부
            is_double_size = candle_before_7_day_size >= candle_before_8_day_size * 2
            # 8일 전 대비 거래량 2배 이상 여부
            is_double_volumn = candle_before_7_day_volumn >= candle_before_8_day_volumn * 2

            if is_plus and is_double_size and is_double_volumn:
                result_list.append(market['code'])
            else:
                total_count += 1

    logger.log(level=1, msg="get {0} / {1}".format(len(result_list), total_count))
    return result_list

# 마켓 종목 조회
market_list = get_all_market_codes()

# [조건1] 7일 전 장대양봉 출현여부 확인
result_list = get_codes_have_big_plus_candle(market_list)

print(result_list)

bot = telegram.Bot(telegram_access_token)
bot.send_message(chat_id, result_list)
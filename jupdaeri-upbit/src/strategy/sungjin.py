import time
from common import logger, urlencode, quote_plus
from quotation_apis import get_candles, get_orderbook


class Sungjin():

    def __init__(self):
        print("This is Sungjin's Strategy")

    def get_list(self, market_list):
        #TODO 구현 필요
        return self.get_codes_have_big_plus_candle(market_list)

    def get_codes_have_big_plus_candle(self, market_list):
        result_list = []
        total_count = 0
        count = 0
        for market in market_list:
            count += 1
            # 초당 10회 제한
            if count % 10 == 0:
                time.sleep(1)
            result, result_msg = get_candles(market['market'], "days", 9)
            if result is not None:

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
                    result_list.append({"code": market['market'], "name": market['korean_name']})
                else:
                    total_count += 1

        logger.log(level=1, msg="get {0} / {1}".format(len(result_list), total_count))
        return result_list

    def check_sell_condition(self, market, buy_price):
        """
        현재가 조회
        """
        result, result_msg = get_orderbook(market)

        if result is None:
            return "hold", 0

        units = result[0]["orderbook_units"]
        cur_price = units[0]

        if (cur_price - buy_price) / buy_price * 100 >= 3 or \
                (cur_price - buy_price) / buy_price * 100 < -2:
            return "sell", cur_price
        else:
            return "hold", 0

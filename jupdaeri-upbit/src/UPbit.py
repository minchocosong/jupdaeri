"""
암호화폐 자동매매프로그램
"""
import time
from datetime import datetime
from threading import Thread
from common import logger, telegram_bot, CHAT_ID
from exchange_apis import get_balance, buy_limit_order, sell_limit_order, get_order_state
from quotation_apis import get_markets, get_orderbook
from strategy.sungjin import Sungjin
from simulator import simul_buy_limit_order, simul_sell_limit_order


profit_and_loss_report = {}  # 손익 리스트
order_report = {}  # 주문 리포트

SIMULATION = True
INIT_DEPOSIT = 1000000  # 초기 예수금 (시뮬레이션 모드시 사용)
BUY_AMOUNT = 100000  # 마켓 당 매수 금액
strategy = Sungjin()


# 기능 테스트
# buy_market_order("KRW-PCI", 5000)
# buy_limit_order("KRW-PCI", 500, 10)
# sell_market_order("", 0)
# telegram_bot.send_message(CHAT_ID, json.dumps(result_list, ensure_ascii=False))


def get_available_krw(account_list):
    """
    매수가능 한화 금액
    """
    bal = [curr['balance'] for curr in account_list if curr['currency'] == 'KRW']
    return float(bal[0]) if len(bal) > 0 else 0


def buyer():
    # 조건식 지정
    logger.log(level=1, msg='Buyer starts work')

    # 자산 조회
    balance = get_balance()
    logger.log(level=1, msg=f'자산 조회 {balance}')

    # 마켓 전체 종목 조회
    all_market_list, all_market_list_msg = get_markets(fiat="KRW")

    while True:

        # 매수 가능 한화
        if SIMULATION:
            krw_balance = INIT_DEPOSIT
        else:
            krw_balance = get_available_krw(balance)

        logger.log(level=1, msg=f'매수 가능 한화 {krw_balance}')

        if krw_balance > BUY_AMOUNT:  # 매수 가능 한화가 있을 경우

            today_pl_report = profit_and_loss_report.get(datetime.now().strftime("%Y%m%d"))

            market_list = strategy.get_list(all_market_list)
            markets = ",".join([market['code'] for market in market_list])
            orderbook_list, orderbook_msg = get_orderbook(markets)

            if orderbook_list is None:
                telegram_bot.send_message(CHAT_ID, orderbook_msg)
                break

            # 현재 호가를 조회
            for orderbook in orderbook_list:

                if krw_balance > BUY_AMOUNT:

                    market = orderbook['market']
                    # 3호가 채택
                    units = orderbook['orderbook_units']
                    pick_unit = units[2]

                    # 주문량
                    volume = int(BUY_AMOUNT / pick_unit['bid_price'])

                    if SIMULATION:
                        buy_result, buy_result_msg = simul_buy_limit_order(market, pick_unit['bid_price'],
                                                                           volume)  # TEST코드
                    else:
                        buy_result, buy_result_msg = buy_limit_order(orderbook['market'], pick_unit['bid_price'], volume)

                    if buy_result is None:
                        telegram_bot.send_message(CHAT_ID, buy_result_msg)
                        break

                    # 주문 리스트 (진행중) 업데이트, 상태는 buy
                    order_result = {"market": market, "state": "buy", "buy_uuid": buy_result['uuid'],
                                    "buy_price": pick_unit['bid_price'], "volume": volume}

                    if order_report.get('active') is None:
                        order_report['active'] = [order_result]
                    else:
                        order_report['active'].append(order_result)

                    # 손익 리스트 업데이트 (market, buy_price, volume, create_at)
                    profit_and_loss = {
                                        "market": market,
                                        "buy_price": pick_unit['bid_price'],
                                        "volume": volume,
                                        "create_at": buy_result['created_at']
                                      }

                    if today_pl_report is None:
                        today_pl_report = {}

                    today_pl_report[buy_result['uuid']] = profit_and_loss
                    profit_and_loss_report[datetime.now().strftime("%Y%m%d")] = today_pl_report

        # 주문 리포트 (진행중) buy 있는 경우
        for active in order_report['active']:
            if active['state'] == 'buy':
                order_result, order_result_msg = get_order_state(active['buy_uuid'])

                if order_result is None:
                    telegram_bot.send_message(CHAT_ID, order_result_msg)
                    break

                if order_result['state'] == 'done':
                    telegram_bot.send_message(CHAT_ID, order_result_msg)

                    active['state'] = 'buy-done'
                    today_pl_report[active['buy_uuid']]['buy_at'] = order_result['trades.created_at']

        time.sleep(60)


def seller():
    logger.log(level=1, msg='Seller starts work')
    print("seller")
    while True:
        print("hi seller")
        today_pl_report = profit_and_loss_report.get(datetime.now().strftime("%Y%m%d"))

        if order_report.get('active') is None:
            time.sleep(60)
            continue

        # 주문 리포트 (진행중) sell 있는 경우
        for active in order_report['active']:
            if active['state'] == 'buy-done':

                # 매도 조건 체크
                market = active['market']
                result_sell_condition, sell_price = strategy.check_sell_condition(market, active['buy_price'])

                if result_sell_condition == 'sell':

                    # 매도
                    if SIMULATION:
                        sell_result, sell_result_msg = simul_sell_limit_order(market, sell_price, active['volume'])
                    else:
                        sell_result, sell_result_msg = sell_limit_order(market, sell_price, active['volume'])

                    if sell_result is None:
                        telegram_bot.send_message(CHAT_ID, sell_result_msg)
                        break

                    active['sell_uuid'] = sell_result['buy_uuid']
                    active['state'] = 'sell'

            if active['state'] == 'sell':
                order_result, order_result_msg = get_order_state(active['uuid'])  # 주문 완료 여부 조회

                if order_result is None:
                    telegram_bot.send_message(CHAT_ID, order_result_msg)
                    break

                if order_result['state'] == 'done':
                    telegram_bot.send_message(CHAT_ID, order_result_msg)

                    active['state'] = 'sell-done'
                    order_report.pop(active)

                    if order_report.get('done') is None:
                        order_report['done'] = [active]
                    else:
                        order_report['done'].append(active)

                    target_pl_report = today_pl_report[active['buy_uuid']]

                    target_pl_report['sell_price'] = order_result['trades.price']
                    target_pl_report['fee'] = order_result['paid_fee']
                    target_pl_report['earning'] = (target_pl_report['buy_price'] - target_pl_report['sell_price']) \
                                                  * target_pl_report['volume'] - target_pl_report['fee']
                    target_pl_report['yield'] = target_pl_report['earning'] / (target_pl_report['buy_price']
                                                                               * target_pl_report['volume']) * 100
                    target_pl_report['sell_at'] = order_result['trades.created_at']

        time.sleep(60)


buyer_thread = Thread(target=buyer)
seller_thread = Thread(target=seller)

buyer_thread.start()
seller_thread.start()
buyer_thread.join()
seller_thread.join()


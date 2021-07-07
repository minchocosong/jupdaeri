"""
잔고조회, 지정가/시장가 매수, 지정가/시장가 매도
"""
from common import logger, upbit_request


def get_balance():
    """
    잔고 조회
    """
    balance = None
    res = upbit_request("get", "/v1/accounts", {})
    if res.status_code == 200:
        balance = res.json()
        msg = f'[자산 조회 성공]'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[자산 조회 실패]'
        logger.error(msg=msg)

    return balance, msg


def buy_limit_order(market, price, volume):
    """
    지정가 매수
    """
    query = {
        'market': market,
        'side': 'bid',
        'price': price,  # 주문가격 ( 호가 기준으로 입력 )
        'volume': volume,  # 주문수량 (살 가격  / 호가)
        'ord_type': 'limit',
    }

    result = None
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
        msg = f'[지정가 매수 주문 성공] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[지정가 매수 주문 실패] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.error(msg=msg)

    return result, msg


def buy_market_order(market, price):
    """
    시장가 매수
    """

    query = {
        'market': market,
        'side': 'bid',
        'price': price,  # 주문가격 ( 살 가격으로 입력 )
        'ord_type': 'price',
    }

    result = None
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
        msg = f'[시장가 매수 주문 성공] 마켓코드: {market}, price: {price}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[시장가 매수 주문 실패] 마켓코드: {market}, price: {price}'
        logger.error(msg=msg)

    return result, msg


def sell_limit_order(market, price, volume):
    """
    지정가 매도
    """
    query = {
        'market': market,
        'side': 'ask',
        'price': price,  # 주문가격 ( 호가 기준으로 입력 )
        'volume': volume,   # 주문수량 (팔 가격  / 호가)
        'ord_type': 'limit',
    }

    result = None
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
        msg = f'[지정가 매도 주문 성공] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[지정가 매도 주문 실패] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.error(msg=msg)

    return result, msg


def sell_market_order(market, volume):
    """
    시장가 매도
    """
    query = {
        'market': market,
        'side': 'ask',
        'volume': volume,  # 주문가격 ( 팔 가격으로 입력 )
        'ord_type': 'market',
    }

    result = None
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
        msg = f'[시장가 매도 주문 성공] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[시장가 매도 주문 실패] 마켓코드: {market}, price: {price}, volume: {volume}'
        logger.error(msg=msg)

    return result, msg


def get_order_state(uuid):
    """
    개별 주문 조회
    """
    query = {
        'uuid': uuid,
    }

    result = None
    res = upbit_request("get", "/v1/order", query)
    if res.status_code == 200:
        result = res.json()
        msg = f'[개별 주문 조회 성공] uuid: {uuid}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[개별 주문 조회 실패] uuid: {uuid}'
        logger.error(msg=msg)

    return result, msg

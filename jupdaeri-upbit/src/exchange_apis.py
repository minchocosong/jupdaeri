"""
잔고조회, 지정가/시장가 매수, 지정가/시장가 매도
"""
from common import logger, upbit_request


def get_balance():
    """
    잔고 조회
    """
    balance = []
    res = upbit_request("get", "/v1/accounts", {})
    if res.status_code == 200:
        balance = res.json()
    else:
        logger.log(level=4, msg='자산 조회 실패')

    return balance


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

    result = {}
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
    else:
        logger.log(level=4, msg='지정가 매수 실패')

    return result


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

    result = {}
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
    else:
        logger.log(level=4, msg='시장가 매수 실패')

    return result


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

    result = {}
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
    else:
        logger.log(level=4, msg='지정가 매도 실패')

    return result



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

    result = {}
    res = upbit_request("post", "/v1/orders", query)
    if res.status_code == 201:
        result = res.json()
    else:
        logger.log(level=4, msg='시장가 매도 실패')

    return result

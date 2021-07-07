"""
마켓코드 조회, 캔들 조회
"""
from common import logger, upbit_request


def get_markets(fiat=None):
    """
    마켓코드 조회
    """

    markets = None
    res = upbit_request("get", "/v1/market/all", {})
    if res.status_code == 200:
        if fiat == "KRW":
            markets = [market for market in res.json() if market['market'].startswith("KRW")]
        else:
            markets = [market for market in res.json()]
        msg = f'[마켓 코드 조회 성공]'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[마켓 코드 조회 실패]'
        logger.error(msg=msg)

    return markets, msg


def get_candles(market, interval, count, unit=1):
    """
    캔들조회
    """
    query = {"market": market, "count": count}

    result = None
    if interval == "minutes":
        res = upbit_request("get", "/v1/candles/minutes/" + unit, query)
    elif interval == "days":
        res = upbit_request("get", "/v1/candles/days", query)
    elif interval == "weeks":
        res = upbit_request("get", "/v1/candles/weeks", query)
    else:
        res = upbit_request("get", "/v1/candles/months", query)

    if res.status_code == 200:
        result = res.json()
        msg = f'[캔들 조회 성공] 마켓코드: {market}, 캔들 종류: {interval}, 캔들 개수: {count}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[캔들 조회 실패] 마켓코드: {market}, 캔들 종류: {interval}, 캔들 개수: {count}'
        logger.error(msg=msg)

    return result, msg


def get_orderbook(markets):
    """
    호가 조회
    """
    query = {"markets": markets}

    result = None
    res = upbit_request("get", "/v1/orderbook", query)
    if res.status_code == 200:
        result = res.json()
        msg = f'[호가 조회 성공] 마켓코드: {markets}'
        logger.log(level=4, msg=msg)
    else:
        msg = f'[호가 조회 실패] 마켓코드: {markets}'
        logger.error(msg=msg)

    return result, msg

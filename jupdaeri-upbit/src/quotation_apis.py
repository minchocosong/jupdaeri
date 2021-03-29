"""
마켓코드 조회, 캔들 조회
"""
from common import logger, upbit_request


def get_markets(fiat=None):
    """
    마켓코드 조회
    """
    markets = []
    res = upbit_request("get", "/v1/market/all", {})
    if res.status_code == 200:
        if fiat == "KRW":
            markets = [market for market in res.json() if market['market'].startswith("KRW")]
        else:
            markets = [market for market in res.json()]
    else:
        logger.log(level=4, msg='마켓 정보 조회 실패')

    return markets


def get_candles(market, interval, count, unit=1):
    """
    캔들조회
    """

    query = {"market": market, "count": count}

    if interval == "minutes":
        res = upbit_request("get", "/v1/candles/minutes/" + unit, query)
    elif interval == "days":
        res = upbit_request("get", "/v1/candles/days", query)
    elif interval == "weeks":
        res = upbit_request("get", "/v1/candles/weeks", query)
    else:
        res = upbit_request("get", "/v1/candles/months", query)

    if res.status_code == 200:
        return res.json()

    return None

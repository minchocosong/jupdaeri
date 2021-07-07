"""
시뮬레이션 코드
"""

def simul_buy_limit_order(market, price, volume): 

    msg = f'[지정가 매수 주문 성공] 마켓코드: {market}, price: {price}, volume: {volume}'
    response = {
          "uuid": "cdd92199-2897-4e14-9448-f923320408ad",
          "side": "bid",
          "ord_type": "limit",
          "price": price,
          "avg_price": "0.0",
          "state": "wait",
          "market": market,
          "created_at": "2018-04-10T15: 42: 23+09: 00",
          "volume": volume,
          "remaining_volume": "0.01",
          "reserved_fee": "0.0015",
          "remaining_fee": "0.0015",
          "paid_fee": "0.0",
          "locked": "1.0015",
          "executed_volume": "0.0",
          "trades_count": 0
        }

    return response, msg


def simul_sell_limit_order(market, price, volume):

    msg = f'[지정가 매도 주문 성공] 마켓코드: {market}, price: {price}, volume: {volume}'
    response = {
        "uuid": "cdd92199-2897-4e14-9448-f923320408ad",
        "side": "bid",
        "ord_type": "limit",
        "price": price,
        "avg_price": "0.0",
        "state": "wait",
        "market": market,
        "created_at": "2018-04-10T15: 42: 23+09: 00",
        "volume": volume,
        "remaining_volume": "0.01",
        "reserved_fee": "0.0015",
        "remaining_fee": "0.0015",
        "paid_fee": "0.0",
        "locked": "1.0015",
        "executed_volume": "0.0",
        "trades_count": 0
    }

    return response, msg

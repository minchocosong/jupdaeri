"""
각종 유틸 함수들
"""


def get_order_unit(hoga):
    """
    원화 마켓 주문 가격 단위
    """
    if 0 <= hoga < 10:
        return 0.01
    elif 10 <= hoga < 100:
        return 0.1
    elif 100 <= hoga < 1000:
        return 1
    elif 1000 <= hoga < 10000:
        return 5
    elif 10000 <= hoga < 100000:
        return 10
    elif 100000 <= hoga < 500000:
        return 50
    elif 500000 <= hoga < 1000000:
        return 100
    elif 1000000 <= hoga < 2000000:
        return 500
    elif 2000000:
        return 1000

    return 0

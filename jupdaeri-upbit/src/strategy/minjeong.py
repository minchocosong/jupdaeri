from common import logger
from quotation_apis import get_candles


class Minjeong:

    def get_rsi(self):
        """
            RSI
            ＊과매수구간(RSI 70이상) - 매수세가 고점에 다달았기에 매도하기 적합,매수타이밍으로 좋지 못함.
            ＊과매도구간(RSI 30이하) - 지금 극 매도구간으로 조만간 반등이 타이밍.RSI 30 이하에서 다시 올라올 때 매수.
        """
        return None


    # Up trend (상승 추세선) 최소 두 개 이상의 저점 꼬리로 그린다
    # down trend (하락 추세선) 최소 두 개 이상의 고점



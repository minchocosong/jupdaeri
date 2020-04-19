from .common import *


# Cp6033 : 주식 잔고 조회
class Cp6033:
    def __init__(self):
        if init_plus_check():
            self.acc = g_objCpTrade.AccountNumber[0]  # 계좌번호
            self.accFlag = g_objCpTrade.GoodsList(self.acc, 1)  # 주식상품 구분
            self.balance = []
            print(self.acc, self.accFlag[0])

            self.objRq = win32com.client.Dispatch("CpTrade.CpTd6033")
            self.objRq.SetInputValue(0, self.acc)  # 계좌번호
            self.objRq.SetInputValue(1, self.accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
            self.objRq.SetInputValue(2, 50)  # 요청 건수(최대 50)
            self.dicFlag1 = {ord(' '): '현금',
                             ord('Y'): '융자',
                             ord('D'): '대주',
                             ord('B'): '담보',
                             ord('M'): '매입담보',
                             ord('P'): '플러스론',
                             ord('I'): '자기융자',
                             }

    # 실제적인 6033 통신 처리
    def request_jango(self):
        while True:
            self.objRq.BlockRequest()
            # 통신 및 통신 에러 처리
            rq_status = self.objRq.GetDibStatus()
            rq_ret = self.objRq.GetDibMsg1()
            print("통신상태", rq_status, rq_ret)
            if rq_status != 0:
                return False

            cnt = self.objRq.GetHeaderValue(7)
            print(cnt)

            for i in range(cnt):
                item = {}
                code = self.objRq.GetDataValue(12, i)  # 종목코드
                item['code'] = code  # 종목코드
                item['name'] = self.objRq.GetDataValue(0, i)  # 종목명
                item['cash_credit'] = self.dicFlag1[self.objRq.GetDataValue(1, i)]  # 신용구분
                item['loan_date'] = self.objRq.GetDataValue(2, i)  # 대출일
                item['available_selling_amount'] = self.objRq.GetDataValue(15, i)  # 매도가능수량
                item['conclusion_amount'] = self.objRq.GetDataValue(7, i)  # 체결잔고수량
                item['conclusion_unit_price'] = self.objRq.GetDataValue(17, i)  # 체결장부단가
                item['evaluation_price'] = self.objRq.GetDataValue(9, i)  # 평가금액(천원미만은 절사 됨)
                item['evaluation_plus_minus'] = self.objRq.GetDataValue(11, i)  # 평가손익(천원미만은 절사 됨)
                item['conclusion_price'] = item['conclusion_unit_price'] * item['conclusion_amount']
                item['current_price'] = 0  # TODO 현재가 연동하기

                self.balance.append(item)

            if len(self.balance) >= 200:
                break

            if not self.objRq.Continue:
                break

        return True

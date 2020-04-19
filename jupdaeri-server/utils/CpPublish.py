import win32com.client

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')


################################################
# plus 실시간 수신 base 클래스
class CpPublish:
    def __init__(self, name, serviceID):
        self.name = name
        self.obj = win32com.client.Dispatch(serviceID)
        self.bIsSB = False

    def Subscribe(self, var, caller):
        if self.bIsSB:
            self.Unsubscribe()

        if (len(var) > 0):
            self.obj.SetInputValue(0, var)

        handler = win32com.client.WithEvents(self.obj, CpEvent)
        handler.set_params(self.obj, self.name, caller)
        self.obj.Subscribe()
        self.bIsSB = True

    def Unsubscribe(self):
        if self.bIsSB:
            self.obj.Unsubscribe()
        self.bIsSB = False


################################################
# CpEvent: 실시간 이벤트 수신 클래스
class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관

        # 구분값 : 텍스트로 변경하기 위해 딕셔너리 이용
        self.dicflag12 = {'1': '매도', '2': '매수'}
        self.dicflag14 = {'1': '체결', '2': '확인', '3': '거부', '4': '접수'}
        self.dicflag15 = {'00': '현금', '01': '유통융자', '02': '자기융자', '03': '유통대주',
                          '04': '자기대주', '05': '주식담보대출', '07': '채권담보대출',
                          '06': '매입담보대출', '08': '플러스론',
                          '13': '자기대용융자', '15': '유통대용융자'}
        self.dicflag16 = {'1': '정상주문', '2': '정정주문', '3': '취소주문'}
        self.dicflag17 = {'1': '현금', '2': '신용', '3': '선물대용', '4': '공매도'}
        self.dicflag18 = {'01': '보통', '02': '임의', '03': '시장가', '05': '조건부지정가'}
        self.dicflag19 = {'0': '없음', '1': 'IOC', '2': 'FOK'}

    def OnReceived(self):
        # 실시간 처리 - 현재가 주문 체결
        if self.name == 'stockcur':
            code = self.client.GetHeaderValue(0)  # 초
            name = self.client.GetHeaderValue(1)  # 초
            timess = self.client.GetHeaderValue(18)  # 초
            exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
            cprice = self.client.GetHeaderValue(13)  # 현재가
            diff = self.client.GetHeaderValue(2)  # 대비
            cVol = self.client.GetHeaderValue(17)  # 순간체결수량
            vol = self.client.GetHeaderValue(9)  # 거래량

            item = {}
            item['code'] = code
            # rpName = self.objRq.GetDataValue(1, i)  # 종목명
            # rpDiffFlag = self.objRq.GetDataValue(3, i)  # 대비부호
            item['diff'] = diff
            item['cur'] = cprice
            item['vol'] = vol

            # 현재가 업데이트
            self.caller.updateJangoCurPBData(item)

        # 실시간 처리 - 주문체결
        elif self.name == 'conclution':
            # 주문 체결 실시간 업데이트
            conc = {}

            # 체결 플래그
            conc['체결플래그'] = self.dicflag14[self.client.GetHeaderValue(14)]

            conc['주문번호'] = self.client.GetHeaderValue(5)  # 주문번호
            conc['주문수량'] = self.client.GetHeaderValue(3)  # 주문/체결 수량
            conc['주문가격'] = self.client.GetHeaderValue(4)  # 주문/체결 가격
            conc['원주문'] = self.client.GetHeaderValue(6)
            conc['종목코드'] = self.client.GetHeaderValue(9)  # 종목코드
            conc['종목명'] = g_objCodeMgr.CodeToName(conc['종목코드'])

            conc['매수매도'] = self.dicflag12[self.client.GetHeaderValue(12)]

            flag15 = self.client.GetHeaderValue(15)  # 신용대출구분코드
            if (flag15 in self.dicflag15):
                conc['신용대출'] = self.dicflag15[flag15]
            else:
                conc['신용대출'] = '기타'

            conc['정정취소'] = self.dicflag16[self.client.GetHeaderValue(16)]
            conc['현금신용'] = self.dicflag17[self.client.GetHeaderValue(17)]
            conc['주문조건'] = self.dicflag19[self.client.GetHeaderValue(19)]

            conc['체결기준잔고수량'] = self.client.GetHeaderValue(23)
            loandate = self.client.GetHeaderValue(20)
            if (loandate == 0):
                conc['대출일'] = ''
            else:
                conc['대출일'] = str(loandate)
            flag18 = self.client.GetHeaderValue(18)
            if (flag18 in self.dicflag18):
                conc['주문호가구분'] = self.dicflag18[flag18]
            else:
                conc['주문호가구분'] = '기타'

            conc['장부가'] = self.client.GetHeaderValue(21)
            conc['매도가능수량'] = self.client.GetHeaderValue(22)

            print(conc)
            self.caller.updateJangoCont(conc)

            return

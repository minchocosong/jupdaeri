import os
import sys
from PyQt5.QAxContainer import *  # QAxContainer 에는 마이크로소프트사에서 제공하는 프로세스를 가지고 화면을 구성하는데 필요한 기능이 담겨있음
from PyQt5.QtCore import *
from PyQt5.QtTest import QTest

from config.errorCode import *
from config.kiwoomType import *
from config.log_class import *

from config.slack import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()  # QAxWidget은 디자인 구성을 컨트롤하고 재사용하는 기능들을 포함함

        self.realType = RealType()
        self.logging = Logging()
        self.slack = Slack()

        self.logging.logger.debug("Kiwoom() class start.")

        # event loop를 실행하기 위한 변수 모음
        self.login_event_loop = QEventLoop()  # 로그인 요청용 이벤트 루프
        self.detail_account_info_event_loop = QEventLoop()  # 예수금 요청용 이벤트 루프
        self.calculator_event_loop = QEventLoop()  # 종목 계산 이벤트 루프
        ###################################

        # 계좌 관련된 변수
        self.account_stock_dict = {}
        self.not_account_stock_dict = {}
        self.account_num = None  # 계좌번호 담아줄 변수
        self.deposit = 0  # 예수금
        self.use_money = 0  # 실제 투자에 사용할 금액
        self.use_money_percent = 0.5  # 예수금에서 실제 사용할 비율
        self.output_deposit = 0  # 출력가능 금액
        self.total_profit_loss_money = 0  # 총평가손익금액
        self.total_profit_loss_rate = 0.0  # 총 수익률(%)
        ###################################

        # 종목 정보 가져오기
        self.portfolio_stock_dict = {}
        self.jango_dict = {}
        ###################################

        # 종목 분석 용
        self.calcul_data = []
        ###################################

        # 요청 스크린 번호
        self.screen_my_info = "2000"  # 계좌 관련한 스크린 번호
        self.screen_calculation_stock = "4000"  # 계산용 스크린 번호
        self.screen_real_stock = "5000"  # 종목별 할당할 스크린 번호
        self.screen_meme_stock = "6000"  # 종목별 할당할 주문용 스크린 번호
        self.screen_start_stop_real = "1000" # 장 시작/종료 실시간 스크린 번호
        ###################################

        # 초기 셋팅 함수들 바로 실행
        self.get_ocx_instance()  # OCX 방식을 파이선에서 사용할 수 있게 반환해주는 함수 실행
        self.event_slots()  # 키움과 연결하기 위한 시그널 / 슬롯 모음
        self.real_event_slot()  # 실시간 이벤트 시그널 / 슬롯 연결
        self.signal_login_comm_connect()  # 로그인 요청 함수 포함
        self.get_account_info()  # 계좌번호 가져오기
        self.detail_account_info()  # 예수금 요청 시그널 포함
        self.detail_account_mystock()  # 계좌평가잔고내역 가져오기
        QTimer.singleShot(5000, self.not_concluded_account)  # 5초 뒤에 미체결 종목들 가져오기 실행
        # QTimer.singleShot(5000, self.calculator_fnc)  # 5초 뒤에 미체결 종목들 가져오기 실행
        ###################################

        QTest.qWait(10000)
        self.read_code()
        self.screen_number_setting()

        QTest.qWait(5000)

        # 실시간 수신 관련 함수
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", self.screen_start_stop_real, '',
                         self.realType.REALTYPE['장시작시간']['장운영구분'], "0")

        for code in self.portfolio_stock_dict.keys():
            screen_num = self.portfolio_stock_dict[code]['스크린번호']
            fids = self.realType.REALTYPE['주식체결']['체결시간']
            self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_num, code, fids, "1")

        self.slack.notification(
            pretext="줍대리 동작",
            title="줍대리가 일을 시작했습니다.",
            fallback="줍대리 출근",
            text="오늘도 열심히 하겠습니다."
        )

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 API 모듈 불러오기

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)  # 로그인 관련 이벤트
        self.OnReceiveTrData.connect(self.trdata_slot)  # 트랜잭션 요청 관련 이벤트
        self.OnReceiveMsg.connect(self.msg_slot)

    def real_event_slot(self):
        self.OnReceiveRealData.connect(self.realdata_slot)  # 실시간 이벤트 연결
        self.OnReceiveChejanData.connect(self.chejan_slot)  # 종목 주문체결 관련한 이벤트

    def signal_login_comm_connect(self):
        self.dynamicCall('CommConnect()')  # 로그인 요청 시그널
        self.login_event_loop.exec_()  # 이벤트 루프 실행

    def login_slot(self, err_code):
        print(errors(err_code)[1])

        # 로그인 처리가 완료됐으면 이벤트 루프를 종료한다.
        self.login_event_loop.exit()

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(QString)", "ACCNO")  # 계좌번호 반환
        account_num = account_list.split(';')[0]

        self.account_num = account_num

        print("계좌번호 : %s" % account_num)

    def detail_account_info(self, s_prev_next="0"):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "예수금상세현황요청", "opw00001", s_prev_next, self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def detail_account_mystock(self, s_prev_next="0"):
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "계좌평가잔고내역요청", "opw00018", s_prev_next, self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def not_concluded_account(self, s_prev_next="0"):
        print("미체결 종목 요청")
        self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(QString, QString)", "체결구분", "1")
        self.dynamicCall("SetInputValue(QString, QString)", "매매구분", "0")
        self.dynamicCall("CommRqData(QString, QString, int, QString)",
                         "실시간미체결요청", "opt10075", s_prev_next, self.screen_my_info)

        self.detail_account_info_event_loop.exec_()

    def trdata_slot(self, s_scr_no, s_rq_name, s_tr_code, s_record_name, s_prev_next):
        if s_rq_name == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)", s_tr_code, s_rq_name, 0, "예수금")
            self.deposit = int(deposit)

            use_money = float(self.deposit) * self.use_money_percent
            self.use_money = int(use_money)
            self.use_money = self.use_money / 4

            output_deposit = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                              s_tr_code, s_rq_name, 0, "출금가능금액")
            self.output_deposit = int(output_deposit)

            print("예수금 : %s" % self.deposit)
            print("출금가능금액 : %s" % self.output_deposit)

            self.stop_screen_cancel(self.screen_my_info)
            self.detail_account_info_event_loop.exit()

        elif s_rq_name == "계좌평가잔고내역요청":
            total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               s_tr_code, s_rq_name, 0, "총매입금액")
            self.total_buy_money = int(total_buy_money)
            total_profit_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                       s_tr_code, s_rq_name, 0, "총평가손익금액")
            self.total_profit_loss_money = int(total_profit_loss_money)
            total_profit_loss_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                      s_tr_code, s_rq_name, 0, "총수익률(%)")
            self.total_profit_loss_rate = float(total_profit_loss_rate)

            print("계좌평가잔고내역요청 싱글데이터 : %s - %s - %s" %
                  (total_buy_money, total_profit_loss_money, total_profit_loss_rate))

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", s_tr_code, s_rq_name)
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                        s_tr_code, s_rq_name, i, "종목번호")
                code = code.strip()[1:]

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                           s_tr_code, s_rq_name, i, "종목명")
                stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                  s_tr_code, s_rq_name, i,
                                                  "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                             s_tr_code, s_rq_name, i, "매입가")
                learn_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                              s_tr_code, s_rq_name, i, "수익률(%)")
                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                 s_tr_code, s_rq_name, i, "현재가")
                total_chegual_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                       s_tr_code, s_rq_name, i, "매입금액")
                possible_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                     s_tr_code, s_rq_name, i, "매매가능수량")

                print("종목번호: %s - 종목명: %s - 보유수량: %s - 매입가: %s - 수익률: %s - 현재가: %s"
                      % (code, code_nm, stock_quantity, buy_price, learn_rate, current_price))

                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict[code] = {}

                code_nm = code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = int(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                self.account_stock_dict[code].update({"종목명": code_nm,
                                                      "보유수량": stock_quantity,
                                                      "매입가": buy_price,
                                                      "수익률(%)": learn_rate,
                                                      "현재가": current_price,
                                                      "매입금액": total_chegual_price,
                                                      "매매가능수량": possible_quantity})

                print("sPreNext: %s" % s_prev_next)
                print("계좌에 가지고 있는 종목은 %s" % rows)

                if s_prev_next == "2":
                    self.detail_account_mystock(s_prev_next="2")
                else:
                    self.detail_account_info_event_loop.exit()

        elif s_rq_name == "실시간미체결요청":
            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", s_tr_code, s_rq_name)

            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", s_tr_code, s_rq_name, i, "종목코드")

                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                           s_tr_code, s_rq_name, i, "종목명")
                order_no = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                            s_tr_code, s_rq_name, i, "주문번호")
                order_status = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                s_tr_code, s_rq_name, i, "주문상태")  # 접수,확인,체결
                order_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                  s_tr_code, s_rq_name, i, "주문수량")
                order_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               s_tr_code, s_rq_name, i, "주문가격")
                order_gubun = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               s_tr_code, s_rq_name, i, "주문구분")  # -매도, +매수, -매도정정, +매수정정
                not_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                s_tr_code, s_rq_name, i, "미체결수량")
                ok_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               s_tr_code, s_rq_name, i, "체결량")

                code = code.strip()
                code_nm = code_nm.strip()
                order_no = int(order_no.strip())
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = int(order_price.strip())
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')
                not_quantity = int(not_quantity.strip())
                ok_quantity = int(ok_quantity.strip())

                if order_no in self.not_account_stock_dict:
                    pass
                else:
                    self.not_account_stock_dict[order_no] = {}

                self.not_account_stock_dict[order_no].update({'종목코드': code,
                                                              '종목명': code_nm,
                                                              '주문번호': order_no,
                                                              '주문상태': order_status,
                                                              '주문수량': order_quantity,
                                                              '주문가격': order_price,
                                                              '주문구분': order_gubun,
                                                              '미체결수량': not_quantity,
                                                              '체결량': ok_quantity})

                print("미체결 종목 : %s " % self.not_account_stock_dict[order_no])

            self.detail_account_info_event_loop.exit()

        elif s_rq_name == "주식일봉차트조회":
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", s_tr_code, s_rq_name, 0, "종목코드")
            code = code.strip()
            # data = self.dynamicCall("GetCommDataEx(QString, QString)", s_tr_code, s_rq_name)
            cnt = self.dynamicCall("GetRepeatCnt(QString, QString)", s_tr_code, s_rq_name)
            print("남은 일자 수 %s" % cnt)

            for i in range(cnt):
                data = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                 s_tr_code, s_rq_name, i, "현재가")
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                         s_tr_code, s_rq_name, i, "거래량")
                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                                 s_tr_code, s_rq_name, i, "거래대금")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                        s_tr_code, s_rq_name, i, "일자")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                               s_tr_code, s_rq_name, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                              s_tr_code, s_rq_name, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)",
                                             s_tr_code, s_rq_name, i, "저가")

                data.append("")
                data.append(float(current_price.strip()))
                data.append(value.strip())
                data.append(trading_value.strip())
                data.append(date.strip())
                data.append(start_price.strip())
                data.append(float(high_price.strip()))
                data.append(float(low_price.strip()))
                data.append("")

                self.calcul_data.append(data.copy())

            if s_prev_next == "2":
                self.day_kiwoom_db(code=code, s_prev_next=s_prev_next)
            else:
                print("총 일수 %s" % len(self.calcul_data))

                pass_success = False

                # 120일 이평선을 그릴만큼의 데이터가 있는지 체크
                if self.calcul_data is None or len(self.calcul_data) < 120:
                    pass_success = False
                else:
                    # 120일 이평선의 최근 가격 구함
                    total_price = 0
                    for value in self.calcul_data[:120]:
                        total_price += int(value[1])
                    moving_average_price = total_price / 120

                    # [조건1] 오늘자 주가가 120일 이평선에 걸쳐있는지 확인
                    bottom_stock_price = False
                    check_price = None

                    # 최근 저가 : self.calcul_data[0][7], 최근 고가 self.calcul_data[0][6]
                    if int(self.calcul_data[0][7] <= moving_average_price <= int(self.calcul_data[0][6])):
                        print("오늘의 주가가 120 이평선에 걸쳐있는지 확인")
                        bottom_stock_price = True
                        check_price = int(self.calcul_data[0][6])  # 최근 고가

                    # [조건2] 과거 일봉 데이터를 조회하면서 120일 이평선보다 주가가 계속 밑에 존재하는지 확인
                    prev_price = None
                    if bottom_stock_price:
                        moving_average_price_prev = 0
                        price_top_moving = False
                        idx = 1

                        while True:
                            if len(self.calcul_data[idx:]) < 120:  # 120일 치가 있는지 계속 확인
                                print("120일 치가 없음")
                                break

                            total_price = 0
                            for value in self.calcul_data[idx:120+idx]:
                                total_price += int(value[1])
                            moving_average_price_prev = total_price / 120

                            # 20일 동안 고가가 이평선보다 높으면 안됨
                            if moving_average_price_prev <= int(self.calcul_data[idx][6]) and idx <= 20:
                                print("20일 동안 주가가 120 이평선과 같거나 위에 있으면 조건 통과 못 함")
                                price_top_moving = False
                                break

                            # 20일 이전의 저가가 이평선보다 높은 구간 (넘는 구간) 찾기
                            elif int(self.calcul_data[idx][7]) > moving_average_price_prev and idx > 20:
                                print("120일치 이평선 위에 있는 구간 확인됨")
                                price_top_moving = True
                                prev_price = int(self.calcul_data[idx][7])  # 20일 이전 이평선보다 높은 구간의 저가
                                break

                            idx += 1

                        # [조건3] 과거에 주가가 120이평선보다 위에 있는 구간의 고가가 최근의 저가보다 낮은지 확인
                        if price_top_moving:
                            if moving_average_price > moving_average_price_prev and check_price > prev_price:
                                print("포착된 이평선의 가격이 오늘자 이평선 가격보다 낮은 것 확인")
                                print("포착된 부분의 일봉 저가가 오늘자 일봉의 고가보다 낮은지 확인")
                                pass_success = True

                    if pass_success:
                        print("조건부 통과됨")

                        code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

                        f = open("files/condition_stock.txt", "a", encoding="utf8")
                        f.write("%s\t%s\t%s\n" % (code, code_nm, str(self.calcul_data[0][1])))
                        f.close()
                    elif not pass_success:
                        print("조건부 통과 못 함")

                self.calcul_data.clear()
                self.calculator_event_loop.exit()

    def stop_screen_cancel(self, s_scr_no=None):
        self.dynamicCall("DisconnectRealData(QString)", s_scr_no)  # 스크린 번호 연결 끊기

    def get_code_list_by_market(self, market_code):
        # market_code : 0(장내), 10(코스닥), 3(ELW), 8(ETF), 50(KONEX),
        #               4(뮤추얼펀드), 5(신주인수권), 6(리츠), 9(하이얼펀드), 30(K=OTC)
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(';')[:-1]
        return code_list

    def calculator_fnc(self):
        code_list = self.get_code_list_by_market("10")

        print("코스닥 갯수 %s" % len(code_list))

        for idx, code in enumerate(code_list):
            if idx < 373:
                continue

            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)
            # 스크린 연결 끊기

            print("%s / %s : KOSDAQ Stock Code : %s is updating..." % (idx + 1, len(code_list), code))
            self.day_kiwoom_db(code=code)

    def day_kiwoom_db(self, code=None, date=None, s_prev_next="0"):
        QTest.qWait(3600)  # 3.6초마다 딜레이를 준다. 동시성 없음

        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("setInputValue(QString, QString)", "수정주가구분", "1")

        if date is not None:
            self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회",
                         "opt10081", s_prev_next, self.screen_calculation_stock)

        self.calculator_event_loop.exec_()

    def read_code(self):
        if os.path.exists("files/condition_stock.txt"):
            f = open("files/condition_stock.txt", "r", encoding="utf8")

            lines = f.readlines()
            for line in lines:
                if line != "":
                    ls = line.split("\\t")

                    stock_code = ls[0]
                    stock_name = ls[1]
                    stock_price = int(ls[2].split("\\n")[0])
                    stock_price = abs(stock_price)

                    self.portfolio_stock_dict.update({stock_code: {"종목명":stock_name, "현재가": stock_price}})
            f.close()
            
    def screen_number_setting(self):
        screen_overwrite = []
        
        # 계좌평가잔고내역에 있는 종목들
        for code in self.account_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)
                
        # 미체결에 있는 종목들
        for order_number in self.not_account_stock_dict.keys():
            code = self.not_account_stock_dict[order_number]['종목코드']
            
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 포트폴리오에 있는 종목들
        for code in self.portfolio_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 스크린 번호 할당
        cnt = 0
        for code in screen_overwrite:
            temp_screen = int(self.screen_real_stock)
            meme_screen = int(self.screen_meme_stock)

            if (cnt % 50) == 0:
                temp_screen += 1
                self.screen_real_stock = str(temp_screen)

            if (cnt % 50) == 0:
                meme_screen += 1
                self.screen_meme_stock = str(meme_screen)

            if code in self.portfolio_stock_dict.keys():
                self.portfolio_stock_dict[code].update({"스크린번호": str(self.screen_real_stock),
                                                        "주문용스크린번호": str(self.screen_meme_stock)})

            elif code not in self.portfolio_stock_dict.keys():
                self.portfolio_stock_dict.update({code: {"스크린번호": str(self.screen_real_stock),
                                                         "주문용스크린번호": str(self.screen_meme_stock)}})
            cnt += 1

        print(self.portfolio_stock_dict)

    def realdata_slot(self, s_code, s_real_type, s_real_data):
        if s_real_type == "장시작시간":
            fid = self.realType.REALTYPE[s_real_type]['장운영구분']  # (0:장시작전, 2:장종료전(20분), 3:장시작, 4,8:장종료(30분), 9:장마감)
            value = self.dynamicCall("GetCommRealData(QString, int)", s_code, fid)

            if value == '0':
                print("장 시작 전")

            elif value == '3':
                print("장 시작")

            elif value == "2":
                print("장 종료, 동시호가로 넘어감")

            elif value == "4":
                print("3시30분 장 종료")

                for code in self.portfolio_stock_dict.keys():
                    self.dynamicCall("SetRealRemove(QString, QString)", self.portfolio_stock_dict[code]['스크린번호'], code)
                    
                # TODO 종목분석/발굴 코드

                sys.exit()

        elif s_real_type == "주식체결":
            a = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['체결시간'])  # 출력 HHMMSS
            b = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['현재가'])  # 출력 : +(-)2520
            b = abs(int(b))

            c = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['전일대비'])  # 출력 : +(-)2520
            c = abs(int(c))

            d = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['등락율'])  # 출력 : +(-)12.98
            d = float(d)

            e = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['(최우선)매도호가'])  # 출력 : +(-)2520
            e = abs(int(e))

            f = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['(최우선)매수호가'])  # 출력 : +(-)2515
            f = abs(int(f))

            g = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['거래량'])  # 출력 : +240124 매수일때, -2034 매도일 때
            g = abs(int(g))

            h = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['누적거래량'])  # 출력 : 240124
            h = abs(int(h))

            i = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['고가'])  # 출력 : +(-)2530
            i = abs(int(i))

            j = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['시가'])  # 출력 : +(-)2530
            j = abs(int(j))

            k = self.dynamicCall("GetCommRealData(QString, int)", s_code,
                                 self.realType.REALTYPE[s_real_type]['저가'])  # 출력 : +(-)2530
            k = abs(int(k))

            if s_code not in self.portfolio_stock_dict:
                self.portfolio_stock_dict.update({s_code: {}})

            self.portfolio_stock_dict[s_code].update({"체결시간": a, "현재가": b, "전일대비": c, "등락율": d,
                                                      "(최우선)매도호가": e, "(최우선)매수호가": f, "거래량": g,
                                                      "누적거래량": h, "고가": i, "시가": j, "저가": k})

            if s_code in self.account_stock_dict.keys() and s_code not in self.jango_dict.keys():
                asd = self.account_stock_dict[s_code]
                meme_rate = (b - asd['매입가']) / asd['매입가'] * 100
                
                if asd['매매가능수량'] > 0 and (meme_rate > 5 or meme_rate < -5):
                    order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, "
                                                 "QString, QString)",
                                                 ["신규매도", self.portfolio_stock_dict[s_code]["주문용스크린번호"],
                                                  self.account_num, 2, s_code,
                                                  asd['매매가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                    if order_success == 0:
                        print("매도주문 전달 성공")
                        del self.account_stock_dict[s_code]
                    else:
                        print("매도주문 전달 실패")

            elif s_code in self.jango_dict.keys():
                jd = self.jango_dict[s_code]
                meme_rate = (b - jd['매입단가']) / jd['매입단가'] * 100

                if jd['주문가능수량'] > 0 and (meme_rate > 5 or meme_rate < -5):
                    order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, "
                                                 "QString, QString)",
                                                 ["신규매도", self.portfolio_stock_dict[s_code]["주문용스크린번호"],
                                                  self.account_num, 2, s_code,
                                                  jd['주문가능수량'], 0, self.realType.SENDTYPE['거래구분']['시장가'], ""])

                    if order_success == 0:
                        print("매도주문 전달 성공")
                    else:
                        print("매도주문 전달 실패")

            elif d > 2.0 and s_code not in self.jango_dict:
                print("매수조건 통과 %s " % s_code)

                result = (self.use_money * 0.1) / e
                quantity = int(result)

                order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, "
                                                 "QString, QString)",
                                                 ["신규매수", self.portfolio_stock_dict[s_code]["주문용스크린번호"],
                                                  self.account_num, 1, s_code,
                                                  quantity, e, self.realType.SENDTYPE['거래구분']['지정가'], ""])

                if order_success == 0:
                    print("매수주문 전달 성공")
                else:
                    print("매수주문 전달 실패")

                not_meme_list = list(self.not_account_stock_dict)
                for order_num in not_meme_list:
                    code = self.not_account_stock_dict[order_num]["종목코드"]
                    meme_price = self.not_account_stock_dict[order_num]["주문가격"]
                    not_quantity = self.not_account_stock_dict[order_num]["미체결수량"]
                    order_gubun = self.not_account_stock_dict[order_num]["주문구분"]
                    
                    if order_gubun == "매수" and not_quantity > 0 and e > meme_price:
                        order_success = self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, "
                                                         "QString, QString)",
                                                 ["매수취소", self.portfolio_stock_dict[code]["주문용스크린번호"],
                                                  self.account_num, 3, code,
                                                  0, 0, self.realType.SENDTYPE['거래구분']['지정가'], order_num])
                        if order_success == 0:
                            print("매수취소 전달 성공")
                        else:
                            print("매수취소 전달 실패")
                    elif not_quantity == 0:
                        del self.not_account_stock_dict[order_num]
        
    def chejan_slot(self, s_gubun, n_item_cnt, s_fid_list):
        if int(s_gubun) == 0:  # 주문체결 (주문 넣은게 체결 될 때마다 불러와짐)
            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['계좌번호'])
            s_code = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목코드'])[1:]
            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['종목명'])
            stock_name = stock_name.strip()

            origin_order_number = self.dynamicCall("GetChejanData(int)",
                                                   self.realType.REALTYPE['주문체결']['원주문번호'])  # 출력 : defaluse : "000000"
            order_number = self.dynamicCall("GetChejanData(int)",
                                            self.realType.REALTYPE['주문체결']['주문번호'])  # 출럭: 0115061 마지막 주문번호

            order_status = self.dynamicCall("GetChejanData(int)",
                                            self.realType.REALTYPE['주문체결']['주문상태'])  # 출력: 접수, 확인, 체결
            order_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문수량'])  # 출력 : 3
            order_quan = int(order_quan)

            order_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문가격'])  # 출력: 21000
            order_price = int(order_price)

            not_chegual_quan = self.dynamicCall("GetChejanData(int)",
                                                self.realType.REALTYPE['주문체결']['미체결수량'])  # 출력: 15, default: 0
            not_chegual_quan = int(not_chegual_quan)

            order_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['주문구분'])  # 출력: -매도, +매수
            order_gubun = order_gubun.strip().lstrip('+').lstrip('-')

            chegual_time_str = self.dynamicCall("GetChejanData(int)",
                                                self.realType.REALTYPE['주문체결']['주문/체결시간'])  # 출력: '151028'

            chegual_price = self.dynamicCall("GetChejanData(int)",
                                             self.realType.REALTYPE['주문체결']['체결가'])  # 출력: 2110 default : ''
            if chegual_price == '':
                chegual_price = 0
            else:
                chegual_price = int(chegual_price)

            chegual_quantity = self.dynamicCall("GetChejanData(int)",
                                                self.realType.REALTYPE['주문체결']['체결량'])  # 출력: 5 default : ''
            if chegual_quantity == '':
                chegual_quantity = 0
            else:
                chegual_quantity = int(chegual_quantity)

            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['주문체결']['현재가'])  # 출력: -6000
            current_price = abs(int(current_price))

            first_sell_price = self.dynamicCall("GetChejanData(int)",
                                                self.realType.REALTYPE['주문체결']['(최우선)매도호가'])  # 출력: -6010
            first_sell_price = abs(int(first_sell_price))

            first_buy_price = self.dynamicCall("GetChejanData(int)",
                                               self.realType.REALTYPE['주문체결']['(최우선)매수호가'])  # 출력: -6000
            first_buy_price = abs(int(first_buy_price))

            # 새로 들어온 주문이면 주문번호 할당
            if order_number not in self.not_account_stock_dict.keys():
                self.not_account_stock_dict.update({order_number: {}})

            self.not_account_stock_dict[order_number].update({"종목코드": s_code, "주문번호": order_number,
                                                              "종목명": stock_name, "주문상태": order_status,
                                                              "주문수량": order_quan, "주문가격": order_price,
                                                              "미체결수량": not_chegual_quan, "원주문번호": origin_order_number,
                                                              "주문구분": order_gubun, "주문/체결시간": chegual_time_str,
                                                              "체결가": chegual_price, "체결량": chegual_quantity,
                                                              "현재가": current_price, "(최우선)매도호가": first_sell_price,
                                                              "(최우선)매수호가": first_buy_price})
        
        elif int(s_gubun) == 1:  # 잔고 (주문체결이 불러와지고 이어서 잔고가 불러와짐)
            account_num = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['계좌번호'])
            s_code = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목코드'])[1:]

            stock_name = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['종목명'])
            stock_name = stock_name.strip()

            current_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['현재가'])
            current_price = abs(int(current_price))

            stock_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['보유수량'])
            stock_quan = int(stock_quan)

            like_quan = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['주문가능수량'])
            like_quan = int(like_quan)

            buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매입단가'])
            buy_price = abs(int(buy_price))

            total_buy_price = self.dynamicCall("GetChejanData(int)",
                                               self.realType.REALTYPE['잔고']['총매입가'])  # 계좌에 있는 종목의 총매입가
            total_buy_price = int(total_buy_price)

            meme_gubun = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['매도매수구분'])
            meme_gubun = self.realType.REALTYPE['매도수구분'][meme_gubun]

            first_sell_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매도호가'])
            first_sell_price = abs(int(first_sell_price))

            first_buy_price = self.dynamicCall("GetChejanData(int)", self.realType.REALTYPE['잔고']['(최우선)매수호가'])
            first_buy_price = abs(int(first_buy_price))

            if s_code not in self.jango_dict.keys():
                self.jango_dict.update({s_code: {}})

            self.jango_dict[s_code].update({"현재가": current_price, "종목코드": s_code, "종목명": stock_name,
                                            "보유수량": stock_quan, "주문가능수량": like_quan, "매입단가": buy_price,
                                            "총매입가": total_buy_price, "매도매수구분": meme_gubun,
                                            "(최우선)매도호가": first_sell_price, "(최우선)매수호가": first_buy_price})

            if stock_quan == 0:
                del self.jango_dict[s_code]

    def msg_slot(self, s_scr_no, s_rq_name, s_tr_code, msg):
        print("스크린: %s, 요청이름: %s, tr코드: %s --- %s" % (s_scr_no, s_rq_name, s_tr_code, msg))




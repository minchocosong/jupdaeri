import win32com.client
import ctypes
import pythoncom

################################################
# PLUS 공통 OBJECT
g_objCpTrade = win32com.client.Dispatch('CpTrade.CpTdUtil')
g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')


def init_plus_check():
    pythoncom.CoInitialize()

    # 프로세스가 관리자 권한으로 실행 여부
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('정상: 관리자권한으로 실행된 프로세스입니다.')
    else:
        print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
        return False

    # 연결 여부 체크
    if g_objCpStatus.IsConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False

    # 주문 관련 초기화
    if g_objCpTrade.TradeInit(0) != 0:
        print("주문 초기화 실패")
        return False

    return True


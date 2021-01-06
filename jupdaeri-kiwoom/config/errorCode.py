def errors(err_code):

    err_dic = {0: ('OP_ERR_NONE', '정상처리'),
                -10: ('OP_ERR_FAIL', '실패'),
                -100: ('OP_ERR_LOGIN', '사용자정보교환실패'),
                -101: ('OP_ERR_CONNECT', '서버접속실패'),

                -310: ('OP_ERR_MIS_500CNT_EXC', '주문수량500계약초과'),
                -340: ('OP_ERR_ORD_WRONG_ACCTINFO', '계좌정보없음'),
                -500: ('OP_ERR_ORD_SYMCODE_EMPTY', '종목코드없음'),
                }
    result = err_dic[err_code]

    return result

# jupdaeri

## 조건식

1. 성진's
    - [장대양봉 기준]
        - 전일 캔들 상하폭(몸통)의 2배 이상
        - 전일 대비 거래량 2배 이상 
    - [횡보]
        - 상하폭
    - [조건식]
        - 7일 전 장대양봉 출현 and 직전 5일 간 횡보(상하폭 범위 유사)

1. 민정's
    - [조건식]
        - ddddfd

## 변수
- profit_and_loss_report 손익  리포트 
    - YYYYMMDD 날짜 (key)
        - UUID (key) 매수 주문 UUID
            - market 마켓
            - buy_price 매수단가
            - sell_price 매도단가
            - volume 수량 
            - fee 수수료 
            - earning 실현손익 (매수단가*수량 - 매도단가*수량 - 수수료)
            - yield 수익률 
            - create_at 주문시간(YYMMDD HHMMSS) 
            - buy_at 매수 주문 체결 시간
            - sell_at 매도 주문 체결 시간 
    - ex) profit_and_loss_list = { "20210329" : 
                                        { "9ca023a5-851b-4fec-9f0a-48cd83c2eaae": {"market:"KRW-BTC", ...} ,
                                          "9ca023a5-851b-4fec-9f0a-48cd83c2eaae": {"market:"KRW-BTC", ...} 
                                        },
                                   "20210328" :
                                        { "9ca023a5-851b-4fec-9f0a-48cd83c2eaae": {"market:"KRW-BTC", ...} ,
                                          "9ca023a5-851b-4fec-9f0a-48cd83c2eaae": {"market:"KRW-BTC", ...} 
                                        }
                                  }
        
- order_report 주문 리포트 (list < dict >)
    - active 진행중 (key)
        - market 마켓 
        - state 상태 (buy, buy-done, sell, sell-done)
        - buy_uuid 매수 주문 UUID
        - sell_uuid 매도 주문 UUID
        - buy_price 매수 가격 (계산편의를 위해 저장)
        - volume 매수 수량 (계산편의를 위해 저장)
    - done 완료 (key)
        - market 마켓 
        - buy_uuid 매수주문 UUID
        - sell_uuid 매도주문 UUID
        
    - ex) order_report = {"active": 
                            [ {"market":"KRW-BTC", "state":"buy", "buy_uuid":"9ca023a5-851b-4fec-9f0a-48cd83c2eaae"} ], 
                          "done" : []
                         }
        
## 기본 flow

초기 투자금은 100만원. <br/>
마켓 당 매수 금액은 10만원. <br/>
최초 10 마켓을 보유하고 수익금에 따라 보유 마켓량이 달라진다. <br/>
일괄 매도만 있고 부분 매도는 없다.

buyer 무한 루프 시작 (1분 sleep)

- 매수 가능 한화가 있을 경우
    - 조건식에 맞는 마켓 리스트 업데이트
    - 조건식에 부합하는 리스트 중 각 마켓의 현재 호가를 조회
    - 10만원선에서 현재 호가에 주문 가능한 수량 만큼 매수 주문
    - 주문 리포트 (진행중) 업데이트, 상태는 buy
    - 손익 리스트 업데이트 (market, buy_price, volume, create_at)
    - 매수 가능 한화가 더 있는 경우 조건식 마켓리스트 갯수만큼 반복

- 주문 리포트 (진행중) buy 있는 경우 
    - 주문 완료 여부 조회
    - 주문 리포트 (진행중) 업데이트, 상태는 buy-done
    - 손익 리스트 업데이트 (buy_at)

seller 무한 루프 시작 (1분 sleep)

- 주문 리포트 (진행중) buy-done이 있는 경우 
    - 매도 조건 체크 ( 현재가 기준 +3% 면 익절 , -2%면 손절 매도 주문 )
    - 주문 리포트 (진행중) 업데이트, 상태는 sell
 
- 주문 리포트 (진행중) sell이 있는 경우 
    - 주문 완료 여부 조회
    - 주문 리포트 (진행중) 제거, 주문 리포트(완료) 업데이트
    - 손익 리스트 업데이트 (sell_price, fee, earning, yield, sell_at)

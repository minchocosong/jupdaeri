from django.db import models


class Balance(models.Model):
    code = models.TextField()  # 종목코드
    name = models.TextField()  # 종목명
    cash_credit = models.TextField(null=True)  # 현금/신용
    loan_date = models.DateField(null=True)  # 대출일(신용매수일경우)
    balance_amount = models.IntegerField(null=True)  # 잔고수량
    available_selling_amount = models.IntegerField(null=True)  # 매도가능수량
    conclusion_price = models.FloatField(null=True)  # 체결단가
    evaluation_price = models.FloatField(null=True)  # 평가금액
    evaluation_plus_minus = models.FloatField(null=True)  # 평가손익
    current_price = models.FloatField(null=True)  # 현재가

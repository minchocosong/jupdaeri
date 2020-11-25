from PyQt5.QAxContainer import *
# QAxContainer 에는 마이크로소프트사에서 제공하는 프로세스를 가지고 화면을 구성하는데 필요한 기능이 담겨있음

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()  # QAxWidget은 디자인 구성을 컨트롤하고 재사용하는 기능들을 포함함
        print("Kiwoom() class start.")

        self.get_ocx_instance()  #OCX 방식을 파이선에서 사용할 수 있게 반환해주는 함수 실행
        
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") # 레지스트리에 저장된 API 모듈 불러오기
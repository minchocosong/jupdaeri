from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer
from .daeshin_module.cp6033 import *
from .daeshin_module.common import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class BalanceAPIView(APIView):
    """
    API endpoint that allows balance to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 6033 잔고 object
        obj6033 = Cp6033()
        obj6033.request_jango()
        print(obj6033.acc)
        print(obj6033.balance)
        return Response(obj6033.balance)

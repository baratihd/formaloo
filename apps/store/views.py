from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from core.pagination import PageNumberPagination
from apps.store.models import App
from apps.store.serializers import AppSerializer


__all__ = (
    'AppListView',
    'AppCreateView',
    'PurchaseAppView',
)


class AppListView(ListAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


class AppCreateView(CreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseAppView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        return Response({'message': 'Purchase app endpoint is mocked.'})

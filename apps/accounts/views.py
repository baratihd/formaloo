from rest_framework.views import APIView
from rest_framework.response import Response


__all__ = ('SignupView',)


class SignupView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        return Response({'message': 'Signup endpoint is mocked.'})

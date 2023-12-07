from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password

from app import models
from . import serializers


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'},
                            status=status.HTTP_400_BAD_REQUEST)


class CustomLogin(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            # print(make_password("123"))
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token,
                             'refresh_token': str(refresh),
                             'role': user.role},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'},
                            status=status.HTTP_400_BAD_REQUEST)

class RequestCode(APIView):

    def post(self, request, *args, **kwargs):
        subject = 'Your 2FA Code'
        message = f'Your 2FA code is: test'
        from_email = 'gremoryrias070@gmail.com'
        recipient_list = ['ianautentico598@gmail.com']

        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False)
        return Response({'message': '2FA code sent'})

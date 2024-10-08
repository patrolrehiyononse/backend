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
from django.utils.crypto import get_random_string

from app import models
from api.person import serializers

from .serializers import CustomUserSerializer


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

            if user.role == "admin":
                return Response({'access_token': access_token,
                                 'refresh_token': str(refresh),
                                 'role': user.role,
                                 'sub_unit': user.sub_unit
                                 },
                                status=status.HTTP_200_OK)
            person = models.Person.objects.get(email=user.email)
            return Response({'access_token': access_token,
                             'refresh_token': str(refresh),
                             'role': user.role,
                             'unit': person.person_sub_unit.sub_unit_description,
                             'id': person.id
                             },
                            status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid email or password'},
                            status=status.HTTP_401_UNAUTHORIZED)

class RequestCode(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        subject = 'Your 2FA Code'
        code = get_random_string(length=6)

        user.twofactor_code = code
        user.save()

        message = f'Your 2FA code is: {code}'
        from_email = 'patroleleven@gmail.com'

        # recipient_list = request.data.get("email_list")

        user = request.user
        recipient_list = [user.email]


        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False)
        return Response({'message': '2FA code sent'})

class VerifyCode(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get('code', '')

        if user.twofactor_code == code:
            # Code is valid, perform the desired action
            user.twofactor_code = ''  # Clear the code
            user.save()
            return Response({'message': '2FA code verified'})
        else:
            return Response({'message': 'Invalid 2FA code'}, status=400)

class RegisterUser(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        print(request.data['username'])

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


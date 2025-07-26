from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            send_mail(
                 subject='New User Registration Pending Approval',
                 message=f"A new user has registered:\n\nUsername: {user.username}\nEmail: {user.email}\nApprove them in the admin panel.",
                 from_email=settings.DEFAULT_FROM_EMAIL,
                 recipient_list=[settings.EMAIL_HOST_USER],  # make sure ADMIN_EMAIL is defined in settings.py
                 fail_silently=False
            )
            return Response({'message': 'Registration submitted. Await admin approval.'}, status=201)
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_approved:
                return Response({'error': 'Account not approved yet.'}, status=403)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)
           
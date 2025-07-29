from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import notify_user

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            approve_url = f"http://localhost:8000/api/users/approve/{user.approval_token}/"
            reject_url = f"http://localhost:8000/api/users/reject/{user.approval_token}/"

            message = (
                 f"New user registered: {user.username}\n\n"
                 f"To approve, click: {approve_url}\n"
                 f"To reject, click: {reject_url}"
            )
             
            send_mail(
                 subject='New User Registration Pending Approval',
                 message=message,
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
        return Response({'error': 'You have either not been accepted by the admin or entered invalid credentials.'}, status=400)
           
User = get_user_model()

class ApproveUserView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(approval_token=token)
            user.is_approved = True
            user.approval_token = None
            user.save()

            notify_user(user, approved=True)
            return Response({"message": "User approved successfully."})
        except User.DoesNotExist:
            return Response({"error": "Invalid approval token."}, status=status.HTTP_404_NOT_FOUND)
        

class RejectUserView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(approval_token=token)
            notify_user(user, approved=False)
            user.delete()
            return Response({"message": "User rejected and deleted."})
        except User.DoesNotExist:
            return Response({"error": "Invalid rejection token."}, status=status.HTTP_404_NOT_FOUND)
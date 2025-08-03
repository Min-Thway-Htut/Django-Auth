from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import notify_user, password_reset_token

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
        
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No account with that email exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        token = password_reset_token.make_token(user)
        reset_link = f"http://localhost:3000/reset-password/{user.pk}/{token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
    
class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password_reset_token.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({"success": "Password has been reset."}, status=status.HTTP_200_OK)


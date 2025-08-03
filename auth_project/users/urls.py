from django.urls import path
from .views import RegisterView, LoginView, ApproveUserView, RejectUserView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('approve/<uuid:token>/', ApproveUserView.as_view(), name='approve-user'),
    path('reject/<uuid:token>/', RejectUserView.as_view(), name='reject-user'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password-confirm/<int:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm')
]
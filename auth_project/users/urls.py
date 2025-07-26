from django.urls import path
from .views import RegisterView, LoginView, ApproveUserView, RejectUserView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('approve/<uuid:token>/', ApproveUserView.as_view(), name='approve-user'),
    path('reject/<uuid:token>/', RejectUserView.as_view(), name='reject-user'),

]
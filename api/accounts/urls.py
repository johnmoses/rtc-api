from django.urls import path
from .views import (
    EmailSignupView, MobileSignupView, SignupVerifyView, 
    EmailSignupVerifyResendView, MobileSignupVerifyResendView,
    SigninView, SignoutView, PasswordChangeView, 
    EmailPasswordResetView, MobilePasswordResetView,
    PasswordResetVerifyView, EmailUserView, MobileUserView,
)

urlpatterns = [
    path('signup-email/', EmailSignupView.as_view(), name='signup-email'),
    path('signup-mobile/', MobileSignupView.as_view(), name='signup-mobile'),
    path('signup-verify/<code>/', SignupVerifyView.as_view(), name='signup-verify'),
    path('signup-verify-resend-email/', EmailSignupVerifyResendView.as_view(), name='signup-verify-resend-email'),
    path('signup-verify-resend-mobile/', MobileSignupVerifyResendView.as_view(), name='signup-verify-resend-mobile'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset-email/', EmailPasswordResetView.as_view(), name='password-reset-mobile'),
    path('password-reset-mobile/', MobilePasswordResetView.as_view(), name='password-reset-mobile'),
    path('password-reset-verify/', PasswordResetVerifyView.as_view(),
         name='password-reset-verify'),
    path('me-email/', EmailUserView.as_view(), name='me-email'),
    path('me-mobile/', MobileUserView.as_view(), name='me-mobile'),
]
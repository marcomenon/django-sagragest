from .views import (
    ProfileView, ProfileEditView, CustomLoginView, CustomLogoutView,
    RegisterView, CustomPasswordChangeView,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)
from django.urls import path

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('logout/', CustomLogoutView.as_view(), name='account_logout'),
    path('register/', RegisterView.as_view(), name='account_register'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='account_password_reset'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='account_password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='account_password_reset_confirm'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='account_password_reset_complete'),
]

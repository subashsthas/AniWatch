from django.urls import path, reverse_lazy, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"

urlpatterns = [
                  path('register', views.register, name="register"),
                  path('login', views.login, name="login"),
                  path('logout', views.logout_view, name="logout"),
                  path('profile', views.profile, name="profile"),
                  path('change_password', views.change_password, name="change_password"),
                  path('delete_account/<int:pk>', views.deleteUser, name="delete_user"),

                  path('reset_password/',
                       auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",
                                                            success_url=reverse_lazy('accounts:password_reset_done'),
                                                            email_template_name="accounts/password_reset_email.html"),
                       name="reset_password"),

                  path('reset_password_sent/',
                       auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
                       name="password_reset_done"),
                  path('reset/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html",
                                                                   success_url=reverse_lazy(
                                                                       'accounts:password_reset_complete')),
                       name="password_reset_confirm"),
                  path('reset_password_complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
                       name="password_reset_complete"),

                  path('resendOTP', views.resend_otp),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

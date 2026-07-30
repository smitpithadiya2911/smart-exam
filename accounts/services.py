import random
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPToken, LoginHistory

class AuthService:
    @staticmethod
    def generate_and_send_otp(user):
        otp_code = f"{random.randint(100000, 999999)}"
        OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)
        otp_obj = OTPToken.objects.create(user=user, otp_code=otp_code)
        
        subject = "Password Reset OTP - Smart Online Examination System"
        message = f"Hello {user.get_full_name()},\n\nYour OTP for password reset is: {otp_code}\nThis OTP is valid for 10 minutes."
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@exam.com', [user.email])
        except Exception as e:
            print(f"[Console Email Service] Sent OTP {otp_code} to {user.email}")
        return otp_obj

    @staticmethod
    def log_login_attempt(email, user, ip_address, user_agent, success):
        LoginHistory.objects.create(
            user=user if success else None,
            email_attempted=email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )

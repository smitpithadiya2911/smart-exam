from .models import LoginHistory


class AuthService:
    @staticmethod


    @staticmethod
    def log_login_attempt(email, user, ip_address, user_agent, success):
        LoginHistory.objects.create(
            user=user if success else None,
            email_attempted=email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )



import random
import json
import urllib.request
import urllib.parse
from django.core.mail import send_mail
from django.conf import settings
from .models import OTPToken, LoginHistory, RegistrationOTP


class AuthService:
    @staticmethod
    def generate_and_send_otp(user):
        otp_code = f"{random.randint(100000, 999999)}"
        OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)
        otp_obj = OTPToken.objects.create(user=user, otp_code=otp_code)
        
        subject = "Password Reset OTP - Smart Online Examination System"
        message = f"Hello {user.get_full_name()},\n\nYour OTP for password reset is: {otp_code}\nThis OTP is valid for 10 minutes."
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            print(f"[Email] Password reset OTP sent to {user.email}")
        except Exception as e:
            print(f"[Email ERROR] Failed to send OTP to {user.email}: {e}")
            print(f"[Console Fallback] OTP for {user.email}: {otp_code}")
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

    @staticmethod
    def generate_registration_otps(session_key, email, phone_number, pending_data):
        """Generate dual OTP codes for registration and store pending data."""
        # Invalidate any previous pending OTPs for this session
        RegistrationOTP.objects.filter(session_key=session_key, is_used=False).update(is_used=True)

        email_otp = f"{random.randint(100000, 999999)}"
        phone_otp = f"{random.randint(100000, 999999)}"

        reg_otp = RegistrationOTP.objects.create(
            session_key=session_key,
            email=email,
            phone_number=phone_number,
            email_otp=email_otp,
            phone_otp=phone_otp,
            pending_data=pending_data,
        )

        # Send Email OTP (via Gmail SMTP)
        AuthService._send_registration_email_otp(email, email_otp)
        # Send SMS OTP (via Fast2SMS)
        AuthService._send_registration_sms_otp(phone_number, phone_otp)

        return reg_otp

    @staticmethod
    def _send_registration_email_otp(email, otp_code):
        """Send registration OTP via Gmail SMTP."""
        subject = "Registration OTP - Smart Online Examination"
        message = (
            f"Hello,\n\n"
            f"Your email verification OTP for registration is: {otp_code}\n\n"
            f"This OTP is valid for 10 minutes.\n\n"
            f"If you did not request this, please ignore this email.\n\n"
            f"— Smart Online Examination System"
        )
        try:
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, [email], fail_silently=False)
            print(f"\n{'='*60}")
            print(f"  [OK] EMAIL OTP sent successfully to {email}")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"  [ERROR] EMAIL SEND FAILED: {e}")
            print(f"  [EMAIL] Fallback — EMAIL OTP for {email}: {otp_code}")
            print(f"{'='*60}\n")

    @staticmethod
    def _send_registration_sms_otp(phone_number, otp_code):
        """
        Send registration OTP via Fast2SMS API.
        Sign up at https://www.fast2sms.com/ to get your free API key.
        """
        api_key = getattr(settings, 'FAST2SMS_API_KEY', '')

        # Clean phone number — remove +91, spaces, dashes
        clean_number = phone_number.strip().replace(' ', '').replace('-', '')
        if clean_number.startswith('+91'):
            clean_number = clean_number[3:]
        elif clean_number.startswith('91') and len(clean_number) > 10:
            clean_number = clean_number[2:]

        if not api_key:
            print(f"\n{'='*60}")
            print(f"  [WARN] FAST2SMS_API_KEY not set in .env file!")
            print(f"  [SMS] Fallback — SMS OTP for {phone_number}: {otp_code}")
            print(f"  Sign up at https://www.fast2sms.com/ for free API key")
            print(f"{'='*60}\n")
            return False

        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = json.dumps({
                "route": "otp",
                "variables_values": otp_code,
                "numbers": clean_number,
            })
            headers = {
                'authorization': api_key,
                'Content-Type': 'application/json',
            }

            req = urllib.request.Request(url, data=payload.encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode('utf-8'))

            if result.get('return'):
                print(f"\n{'='*60}")
                print(f"  [OK] SMS OTP sent successfully to {phone_number}")
                print(f"{'='*60}\n")
                return True
            else:
                print(f"\n{'='*60}")
                print(f"  [ERROR] Fast2SMS error: {result.get('message', 'Unknown error')}")
                print(f"  [SMS] Fallback — SMS OTP for {phone_number}: {otp_code}")
                print(f"{'='*60}\n")
                return False

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"  [ERROR] SMS SEND FAILED: {e}")
            print(f"  [SMS] Fallback — SMS OTP for {phone_number}: {otp_code}")
            print(f"{'='*60}\n")
            return False

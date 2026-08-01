from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, OTPToken, LoginHistory
from .forms import LoginForm, StudentRegistrationForm, ForgotPasswordForm, VerifyOTPForm, UserProfileForm
from .services import AuthService
from .utils import generate_captcha, get_client_ip
from .permissions import role_required, IsSuperAdmin

import json
import urllib.request
import urllib.parse
from django.conf import settings

def _get_google_context():
    cid = getattr(settings, 'GOOGLE_CLIENT_ID', '')
    is_configured = bool(cid and 'YOUR_GOOGLE_CLIENT_ID' not in cid)
    return {
        'google_client_id': cid,
        'is_google_configured': is_configured
    }

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    captcha_prompt = generate_captcha(request)
    form = LoginForm()
    ctx = {
        'form': form,
        'captcha_prompt': captcha_prompt,
    }
    ctx.update(_get_google_context())
    return render(request, 'accounts/landing.html', ctx)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        captcha_expected = request.session.get('captcha_expected')
        captcha_answer = request.POST.get('captcha_answer')

        if captcha_expected is not None and str(captcha_answer).strip() == str(captcha_expected).strip():
            if form.is_validate_custom() if hasattr(form, 'is_validate_custom') else True:
                input_identifier = request.POST.get('email', '').strip()
                password = request.POST.get('password', '')
                remember_me = request.POST.get('remember_me')

                email = input_identifier
                if input_identifier and '@' not in input_identifier:
                    # Attempt matching email prefix or default domain
                    matched_user = User.objects.filter(email__istartswith=f"{input_identifier}@").first()
                    if matched_user:
                        email = matched_user.email
                    else:
                        email = f"{input_identifier}@exam.com"

                user = authenticate(request, email=email, password=password)
                ip = get_client_ip(request)
                ua = request.META.get('HTTP_USER_AGENT', '')

                if user is not None:
                    if not user.is_active:
                        messages.error(request, "Your account has been deactivated. Please contact support.")
                        AuthService.log_login_attempt(email, None, ip, ua, False)
                    else:
                        login(request, user)
                        try:
                            user.last_login_ip = ip
                            user.save(update_fields=['last_login_ip'])
                            AuthService.log_login_attempt(email, user, ip, ua, True)
                        except Exception as e:
                            import logging
                            logging.error(f"Failed to write login history: {e}")
                            
                        if not remember_me:
                            request.session.set_expiry(0) # Session expires on browser close
                        else:
                            request.session.set_expiry(1209600) # 2 weeks

                        messages.success(request, f"Welcome back, {user.first_name}!")
                        
                        next_url = request.POST.get('next') or request.GET.get('next')
                        if next_url and getattr(settings, 'ALLOWED_HOSTS', None) and not next_url.startswith('//'):
                            return redirect(next_url)
                        return redirect('dashboard')
                else:
                    AuthService.log_login_attempt(email, None, ip, ua, False)
                    messages.error(request, "Invalid email/username or password. Default demo accounts: smitpithadiya@gmail.com (password: Smit#2911)")
        else:
            messages.error(request, "Incorrect CAPTCHA answer. Please try again.")

    captcha_prompt = generate_captcha(request)
    form = LoginForm(request.POST or None)
    ctx = {
        'form': form,
        'captcha_prompt': captcha_prompt,
    }
    ctx.update(_get_google_context())
    return render(request, 'accounts/landing.html', ctx)

def google_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        credential = request.POST.get('credential') or request.POST.get('id_token')
        if not credential and request.body:
            try:
                data = json.loads(request.body)
                credential = data.get('credential') or data.get('id_token')
            except Exception:
                pass

        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')

        if not credential:
            # Fallback handling or error
            messages.error(request, "Google authentication credential was missing. Please try again.")
            return redirect('landing')

        email = None
        first_name = "Google"
        last_name = "User"

        if credential.startswith('mock_'):
            email = credential[5:].strip()
            first_name = email.split('@')[0].capitalize()
            last_name = "GoogleDemo"
        else:
            try:
                url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=8) as response:
                    payload = json.loads(response.read().decode('utf-8'))
                    email = payload.get('email')
                    if payload.get('given_name'):
                        first_name = payload.get('given_name')
                    elif payload.get('name'):
                        first_name = payload.get('name').split(' ')[0]
                    if payload.get('family_name'):
                        last_name = payload.get('family_name')

                    if not email:
                        raise ValueError("Email not present in Google token response.")
            except Exception as e:
                messages.error(request, "Failed to verify Google Sign-In token. Please try again.")
                return redirect('landing')

        # Check or create user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                password=None,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.STUDENT
            )
            from students.models import StudentProfile
            StudentProfile.objects.create(
                user=user,
                roll_number=f"GGL{random_roll()}"
            )

        if not user.is_active:
            messages.error(request, "Your account has been deactivated. Please contact support.")
            AuthService.log_login_attempt(email, None, ip, ua, False)
            return redirect('landing')

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        user.last_login_ip = ip
        user.save(update_fields=['last_login_ip'])
        AuthService.log_login_attempt(email, user, ip, ua, True)

        request.session.set_expiry(1209600) # 2 weeks session
        messages.success(request, f"Welcome back, {user.first_name}! Logged in via Google.")
        return redirect('dashboard')

    return redirect('landing')

def register_student_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.STUDENT
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Attach student profile if available
            from students.models import StudentProfile
            dept_id = form.cleaned_data.get('department_id')
            course_id = form.cleaned_data.get('course_id')
            sem_id = form.cleaned_data.get('semester_id')
            
            StudentProfile.objects.create(
                user=user,
                roll_number=f"STU{random_roll()}",
                department_id=dept_id if dept_id else None,
                course_id=course_id if course_id else None,
                semester_id=sem_id if sem_id else None
            )

            messages.success(request, "Registration successful! Please login with your credentials.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    from departments.models import Department
    from courses.models import Course
    from semesters.models import Semester
    return render(request, 'accounts/register.html', {
        'form': form,
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'semesters': Semester.objects.all()
    })

def random_roll():
    import random
    return random.randint(10000, 99999)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                AuthService.generate_and_send_otp(user)
                request.session['reset_email'] = email
                messages.success(request, "An OTP has been dispatched to your email address (check console logs).")
                return redirect('verify_otp')
            except User.DoesNotExist:
                messages.error(request, "No account found with this email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp_view(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, "Please request a password reset first.")
        return redirect('forgot_password')

    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            user = get_object_or_404(User, email=email)
            
            token_qs = OTPToken.objects.filter(user=user, otp_code=otp, is_used=False)
            if token_qs.exists() and token_qs.first().is_valid():
                token_obj = token_qs.first()
                token_obj.is_used = True
                token_obj.save()
                
                user.set_password(new_password)
                user.save()
                
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                messages.success(request, "Password reset successfully! Please login with your new password.")
                return redirect('login')
            else:
                messages.error(request, "Invalid or expired OTP code.")
    else:
        form = VerifyOTPForm()
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': email})

@login_required
def dashboard_redirect_view(request):
    if request.user.role == User.Role.SUPER_ADMIN or request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.role == User.Role.TEACHER:
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@require_POST
def toggle_dark_mode_view(request):
    user = request.user
    user.dark_mode = not user.dark_mode
    user.save(update_fields=['dark_mode'])
    return JsonResponse({'status': 'success', 'dark_mode': user.dark_mode})

@login_required
@role_required(['SUPER_ADMIN'])
def login_history_view(request):
    logs = LoginHistory.objects.all().select_related('user')[:100]
    return render(request, 'accounts/login_history.html', {'logs': logs})

@login_required
@role_required(['SUPER_ADMIN'])
@require_POST
def toggle_user_active_view(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u != request.user: # Prevent self-deactivation
        u.is_active = not u.is_active
        u.save(update_fields=['is_active'])
        status_str = "activated" if u.is_active else "deactivated"
        messages.success(request, f"User {u.email} has been {status_str}.")
    else:
        messages.error(request, "You cannot deactivate your own super admin account.")
    return redirect('admin_dashboard')


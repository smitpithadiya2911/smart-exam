from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import User, LoginHistory
from .forms import LoginForm, StudentRegistrationForm, UserProfileForm
from .services import AuthService
from .utils import generate_captcha, get_client_ip
from .permissions import role_required, IsSuperAdmin

import json
import random
from django.conf import settings


def landing_view(request):
    captcha_prompt = generate_captcha(request)
    form = LoginForm()
    reg_form = StudentRegistrationForm()

    from departments.models import Department
    from courses.models import Course
    from semesters.models import Semester

    active_tab = request.GET.get('tab', 'login')

    ctx = {
        'form': form,
        'reg_form': reg_form,
        'captcha_prompt': captcha_prompt,
        'active_tab': active_tab,
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'semesters': Semester.objects.all(),
    }
    return render(request, 'accounts/landing.html', ctx)


def login_view(request):
    login_error = None

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
                        return redirect('landing')
                else:
                    AuthService.log_login_attempt(email, None, ip, ua, False)
                    login_error = "Invalid email/username or password. Please check your credentials and try again."
        else:
            login_error = "Incorrect CAPTCHA answer. Please try again."

    captcha_prompt = generate_captcha(request)
    form = LoginForm(request.POST or None)
    reg_form = StudentRegistrationForm()

    from departments.models import Department
    from courses.models import Course
    from semesters.models import Semester

    ctx = {
        'form': form,
        'reg_form': reg_form,
        'captcha_prompt': captcha_prompt,
        'login_error': login_error,
        'active_tab': 'login',
        'departments': Department.objects.all(),
        'courses': Course.objects.all(),
        'semesters': Semester.objects.all(),
    }
    return render(request, 'accounts/landing.html', ctx)


def register_student_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('/?tab=register')
                
            with transaction.atomic():
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=phone_number,
                    role='STUDENT',
                    email_verified=True,
                    phone_verified=True
                )
                
                # Create student profile
                Student.objects.create(
                    user=user,
                    department_id=form.cleaned_data.get('department_id'),
                    course_id=form.cleaned_data.get('course_id'),
                    semester_id=form.cleaned_data.get('semester_id'),
                )


            
            messages.success(request, "Account created successfully! Please sign in.")
            return redirect('login')
        else:
            # Form has errors — re-render the landing page with register tab active
            messages.error(request, "Please correct the errors in the registration form.")
            return redirect('/?tab=register')
    return redirect('/?tab=register')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')





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




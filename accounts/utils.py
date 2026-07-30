import random

def generate_captcha(request):
    """Generates a simple 2-number math CAPTCHA stored in session."""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha_expected'] = num1 + num2
    return f"{num1} + {num2} = ?"

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

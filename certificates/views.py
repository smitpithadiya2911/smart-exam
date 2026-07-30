from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Certificate

@login_required
def certificate_list_view(request):
    if request.user.role == 'STUDENT':
        certificates = Certificate.objects.filter(student=request.user).select_related('exam', 'exam__subject')
    else:
        certificates = Certificate.objects.select_related('student', 'exam', 'exam__subject').all()
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

@login_required
def certificate_detail_view(request, uuid_str):
    cert = get_object_or_404(Certificate.objects.select_related('student', 'exam', 'exam__subject'), certificate_uuid=uuid_str)
    if request.user.role == 'STUDENT' and cert.student != request.user:
        messages.error(request, "Access denied.")
        return redirect('certificate_list')

    verification_url = request.build_absolute_uri(f"/certificates/verify/{cert.certificate_uuid}/")
    return render(request, 'certificates/certificate_detail.html', {
        'certificate': cert,
        'verification_url': verification_url
    })

def public_verify_certificate_view(request, uuid_str):
    """Public verification portal — No Login Required!"""
    try:
        cert = Certificate.objects.select_related('student', 'exam', 'exam__subject').get(certificate_uuid=uuid_str)
        is_valid = True
    except (Certificate.DoesNotExist, ValueError):
        cert = None
        is_valid = False

    return render(request, 'certificates/verify_public.html', {
        'certificate': cert,
        'is_valid': is_valid,
        'queried_uuid': uuid_str
    })

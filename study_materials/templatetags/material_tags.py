from django import template
from study_materials.models import StudyMaterial

register = template.Library()

@register.simple_tag
def get_material_count():
    return StudyMaterial.objects.count()

@register.simple_tag
def get_student_material_count(student_profile):
    from django.db.models import Q
    return StudyMaterial.objects.filter(
        Q(visibility='ALL') |
        Q(visibility='COURSE', course=student_profile.course) |
        Q(visibility='SEMESTER', semester=student_profile.semester) |
        Q(visibility='SUBJECT', subject__in=student_profile.course.subjects.all() if student_profile.course else [])
    ).distinct().count()

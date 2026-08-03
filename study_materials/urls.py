from django.urls import path
from . import views

urlpatterns = [
    # Admin/Teacher URLs
    path('manage/', views.material_manage_list, name='material_manage_list'),
    path('manage/create/', views.material_create, name='material_create'),
    path('manage/<int:pk>/update/', views.material_update, name='material_update'),
    path('manage/<int:pk>/delete/', views.material_delete, name='material_delete'),
    
    # Student URLs
    path('', views.student_material_list, name='student_material_list'),
    path('<int:pk>/', views.material_detail, name='material_detail'),
    path('<int:pk>/download/', views.material_download, name='material_download'),
]

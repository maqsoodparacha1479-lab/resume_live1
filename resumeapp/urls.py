from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect  # ✅ You forgot to import this!

urlpatterns = [
    path('', lambda request: redirect('login_page')),  # Redirect to login
    path('login/', views.login_page, name='login_page'),
    path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),  # ✅ Built-in logout
    path('dashboard/', views.dashboard, name='dashboard'),
    path('build/', views.resume_builder_view, name='resume_form'),
    path('generate/', views.generate_resume_api, name='generate_resume_api'),
    path('api/resume/generate/', views.generate_resume_api, name='generate_resume'),
    path('preview/', views.preview_resume, name='preview_resume'),
    path('download/', views.download_pdf, name='download_pdf'),
]

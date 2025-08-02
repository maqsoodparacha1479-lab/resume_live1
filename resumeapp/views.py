import json
import base64
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Education, Experience, Skill

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # ✅ This sets the session
            return redirect('dashboard')
        else:
            return render(request, 'login_page.html', {'error': 'Invalid credentials'})
    return render(request, 'login_page.html')

# ----- DASHBOARD -----

def dashboard(request):
    return render(request, 'resumeapp/dashboard.html')


# ----- RESUME FORM PAGE -----

def resume_builder_view(request):
    return render(request, 'resumeapp/resume_form.html')


# ----- PREVIEW PAGE -----

def preview_resume(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        education_entries = []
        experience_entries = []
        skill_entries = []

        education_count = int(data.get('education_count', 0))
        for i in range(1, education_count + 1):
            education_entries.append({
                'degree': data.get(f'education-{i}-degree', ''),
                'university': data.get(f'education-{i}-university', ''),
                'start_date': data.get(f'education-{i}-startDate', ''),
                'end_date': data.get(f'education-{i}-endDate', ''),
                'description': data.get(f'education-{i}-description', ''),
            })

        experience_count = int(data.get('experience_count', 0))
        for i in range(1, experience_count + 1):
            experience_entries.append({
                'job_title': data.get(f'experience-{i}-title', ''),
                'company': data.get(f'experience-{i}-company', ''),
                'start_date': data.get(f'experience-{i}-startDate', ''),
                'end_date': data.get(f'experience-{i}-endDate', ''),
                'responsibilities': data.get(f'experience-{i}-responsibilities', ''),
            })

        skill_count = int(data.get('skill_count', 0))
        for i in range(1, skill_count + 1):
            skill_entries.append({
                'name': data.get(f'skill-{i}-name', ''),
            })

        profile_picture_base64 = None
        profile_picture_file = files.get('profilePicture')
        if profile_picture_file:
            try:
                encoded_image = base64.b64encode(profile_picture_file.read()).decode('utf-8')
                profile_picture_base64 = f"data:{profile_picture_file.content_type};base64,{encoded_image}"
            except Exception as e:
                print(f"Error encoding profile picture: {e}")
                profile_picture_base64 = None

        context = {
            'fullName': data.get('fullName', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'linkedin': data.get('linkedin', ''),
            'address': data.get('address', ''),
            'summary': data.get('summary', ''),
            'education_entries': education_entries,
            'experience_entries': experience_entries,
            'skill_entries': skill_entries,
            'profile_picture_base64': profile_picture_base64,
            'original_form_data': data.dict(),
            'profile_picture_base64_for_download': profile_picture_base64,
        }

        return render(request, 'resumeapp/resume_preview.html', context)

    return HttpResponse("Invalid method for preview_resume. Please submit via POST.", status=405)


# ----- PDF DOWNLOAD -----

def download_pdf(request):
    if request.method == 'POST':
        data = request.POST

        template_name = data.get('template_name', 'resume_template_modern.html')

        education_entries = []
        experience_entries = []
        skill_entries = []

        education_count = int(data.get('education_count', 0))
        for i in range(1, education_count + 1):
            education_entries.append({
                'degree': data.get(f'education-{i}-degree', ''),
                'university': data.get(f'education-{i}-university', ''),
                'start_date': data.get(f'education-{i}-startDate', ''),
                'end_date': data.get(f'education-{i}-endDate', ''),
                'description': data.get(f'education-{i}-description', ''),
            })

        experience_count = int(data.get('experience_count', 0))
        for i in range(1, experience_count + 1):
            experience_entries.append({
                'job_title': data.get(f'experience-{i}-title', ''),
                'company': data.get(f'experience-{i}-company', ''),
                'start_date': data.get(f'experience-{i}-startDate', ''),
                'end_date': data.get(f'experience-{i}-endDate', ''),
                'responsibilities': data.get(f'experience-{i}-responsibilities', ''),
            })

        skill_count = int(data.get('skill_count', 0))
        for i in range(1, skill_count + 1):
            skill_entries.append({
                'name': data.get(f'skill-{i}-name', ''),
            })

        profile_picture_base64 = data.get('profile_picture_base64_for_download', None)

        context = {
            'fullName': data.get('fullName', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'linkedin': data.get('linkedin', ''),
            'address': data.get('address', ''),
            'summary': data.get('summary', ''),
            'education_entries': education_entries,
            'experience_entries': experience_entries,
            'skill_entries': skill_entries,
            'profile_picture_base64': profile_picture_base64,
        }

        template_path = f'resumeapp/{template_name}'
        html = render_to_string(template_path, context)

        response = HttpResponse(content_type='application/pdf')
        filename_prefix = template_name.replace('resume_template_', '').replace('.html', '')
        response['Content-Disposition'] = f'attachment; filename=resume_{filename_prefix}.pdf'

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse(f"Error generating PDF: {pisa_status.err}", status=500)

        return response

    return HttpResponse("Invalid request method for download_pdf. Please submit via POST.", status=405)


# ----- SAVE RESUME TO DB -----
@csrf_exempt
def generate_resume_api(request):
    # unchanged (same as your version)
    ...

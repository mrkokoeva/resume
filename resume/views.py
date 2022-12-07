from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template

from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
import pdfkit

def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form' : form}
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('resume_template')
    return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def resumetemplatePage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        skills = request.POST.get('skills')
        edu = request.POST.get('education')
        about_me = request.POST.get('about_me')
        experience = request.POST.get('experience')
        context = {
            'name' : name,
            'skills' : skills,
            'edu' : edu,
            'about_me' : about_me,
            'experience' : experience
        }
        path_wkhtmltopdf = r'ENTER_PATH_HERE'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        template = get_template('resume.html')
        rendered = template.render(context)
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        return response
    return render(request, 'resume_template.html')


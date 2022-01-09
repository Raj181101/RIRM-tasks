from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

import requests
from bs4 import BeautifulSoup


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="inv/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="inv/login.html", context={"login_form":form})

def reset_password(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(Q(email=username)|Q(username=username))
        if user:
            user = user.last()
            user.set_password(password)
            user.save()
            messages.info(request, f"You are successfully updated your password.")
            return redirect("login")
        else:
            messages.error(request,"username or mail does not exists.")
    form = PasswordResetForm()
    return render(request=request, template_name="inv/password_reset.html", context={"reset_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")


def index(request):
    items = StudentInfo.objects.all()
    if request.POST.get('search'):
        items = items.filter(name__icontains=request.POST.get('search'))
        
    context = {
        'items': items,
        'header': 'StudentInfo',
    }
    return render(request, 'inv/index.html',context)

def display_students(request):
    items = StudentInfo.objects.all()
    context = {
        'items': items,
        'header': 'StudentInfo',
    }
    return render(request, 'inv/index.html', context)



def add_item(request, cls):
    if request.method == "POST":
        form = cls(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request,form.errors)
            return render(request, 'inv/add_new.html', {'form' : form,'header':'Add Student Data'})

    else:
        form = cls()
        return render(request, 'inv/add_new.html', {'form' : form,'header':'Add Student Data'})


def add_student(request):
    return add_item(request, StudentInfoForm)



def edit_item(request, pk, model, cls):
    item = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = cls(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = cls(instance=item)

        return render(request, 'inv/edit_item.html', {'form': form})



def edit_student(request, pk):
    return edit_item(request, pk, StudentInfo, StudentInfoForm)



def delete_student(request, pk):

    template = 'inv/index.html'
    StudentInfo.objects.filter(id=pk).delete()

    return redirect('index')




### Student Academics Views
def display_student_academic(request,pk):
    std_info = StudentInfo.objects.get(id=pk)
    items = StudentAcademics.objects.filter(roll_no=std_info)
    context = {
        'items': items,
        'std_info':std_info,
        'header': 'StudentAcademics',
    }
    return render(request, 'inv/index.html', context)

def display_academic(request):
    items = StudentAcademics.objects.all()
    context = {
        'items': items,
        'header': 'StudentAcademics',
    }
    return render(request, 'inv/index.html', context)



def add_student_academic(request):
    if request.method == "POST":
        if StudentAcademics.objects.filter(roll_no_id=request.POST.get('roll_no')).exists():
            messages.info(request, f"This User lareday have academics")
            return redirect("add_student_academic")
    return add_item(request, StudentAcademicsForm)



def edit_academics(request, pk):
    return edit_item(request, pk, StudentAcademics, StudentAcademicsForm)



def delete_academics(request, pk):

    template = 'inv/index.html'
    StudentAcademics.objects.filter(id=pk).delete()

    return redirect('index')


## Extract Links
def extract_links(request):
    form = ExtractLinksForm()
    hyper_links = []
    if request.method == "POST":
        website = request.POST.get('website_link')
    
        if not website:
            messages.info(request, f"Please enter website url")
            return redirect("extract_links")
        else:
            try:
                reqs = requests.get(website)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                
                urls = []
                for link in soup.findAll('a'):
                    hyper_links.append(link.get('href'))
            except:
                pass        
            return render(request=request, template_name="inv/extract_links.html", context={"extract_form":form,'links':hyper_links})
    
    
    return render(request=request, template_name="inv/extract_links.html", context={"extract_form":form,'links':hyper_links})
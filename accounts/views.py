from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Qualification, Affiliation, Mediator, Category, Language
from django.contrib.auth.models import User
from django.contrib import auth, messages
from dateutil.parser import parse as date_parser

# Create your views here.

# Login functionality
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if (user is not None):
            auth.login(request, user)
            messages.success(request, 'Welcome back, ' + user.first_name)
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def view_mediator(request, id):
	mediator = Mediator.objects.get(id=id)
	context = {
		"mediator": mediator,
	}
	template = "accounts/mediator.html"
	return render(request, template, context)

	
def view_account(request, id):
	account = Account.objects.get(id=id)
	context = {
		"account": account,
	}
	template = "accounts/account.html"
	return render(request, template, context)


def create_account(request):
	categories = Category.objects.all()
	languages = Language.objects.all()
	
	template = "accounts/account_create.html"
	
	context = {
		"categories": categories,
		"languages": languages,
	}
	
	if request.method == "POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		phone = request.POST["phone"]
		password = request.POST["password"]
		languages = request.GET.getlist("languages")
		
		user = User.objects.create(username=email, password=password)
		user.save()
		
		account = Account.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, user=user)
		
		if request.FILES.get("image"):
			for _file in request.FILES.getlist("image"):
				account.image = _file
				account.save()
		
		for lang in languages:
			l = Language.objects.get(name=lang)
			account.languages.add(l)
			
		account.save()
		
		return redirect("core:dashboard")
		
	else:
		return render(request, template, context)
		

def create_mediator(request):
	categories = Category.objects.all()
	languages = Language.objects.all()
	
	template = "accounts/mediator_create.html"
	
	context = {
		"categories": categories,
		"languages": languages,
	}
	
	if request.method == "POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		summary = request.POST["summary"]
		location = request.POST["location"]
		phone = request.POST["phone"]
		password = request.POST["password"]
		languages = request.GET.getlist("languages")
		
		user = User.objects.create(username=email, password=password)
		user.save()
		
		mediator = Mediator.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, user=user, summary=summary, location=location)
		
		if request.FILES.get("image"):
			for _file in request.FILES.getlist("image"):
				mediator.image = _file
				mediator.save()
		
		for lang in languages:
			l = Language.objects.get(name=lang)
			mediator.languages.add(l)
			
		mediator.save()
		
		return redirect("core:dashboard")
		
	else:
		return render(request, template, context)
		
def add_affiliation(request):
	user = request.user
	mediator = Mediator.objects.get(user=user)
	context = {
		"mediator": mediator,
	}
	template = "accounts/affiliation_add.html"
	
	if request.method == "POST":
		name = request.POST["name"]
		
		affiliation = Affiliation.objects.create(name=name, mediator=mediator)
		affiliation.save()
		
	else:
		return render(request, template, context)
		
def add_qualification(request):
	mediator = Mediator.objects.get(user=request.user)
	template = "accounts/qualification_add.html"
	context = {
		"mediator": mediator,
	}
	
	if request.method == "POST":
		institution = request.POST["institution"]
		name = request.POST["name"]
		date_acquired = request.POST["date_acquired"]
		date_acquired = date_parser(date_acquired)
		
		qualification = Qualification.objects.create(institution=institution, name=name, date_acquired=date_acquired, mediator=mediator)
		qualification.save()
		
		return redirect("accounts:mediator", id=mediator.id)
	
	else:
		return render(request, template, context)

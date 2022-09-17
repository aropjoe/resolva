from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Mediator, Account, Category
from .models import Dispute, Session, SessionFile, SessionMessage
from decimal import Decimal
from django.views.decorators.http import require_http_methods
from dateutil.parser import parse as date_parser
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


# Create your views here.
def landing(request):
	template = "core/landing.html"
	account = Account.objects.get(user=request.user)
	context = {
		"account": account,
	}
	return render(request, template, context)


def dashboard(request):
	template = "core/dashboard.html"
	
	account = Account.objects.get(user=request.user)
	disputes = Dispute.objects.filter(parties=account)
	
	context = {
		"disputes": disputes,
		"account": account,
	}
	return render(request, template, context)


def create_dispute(request):
	template = "core/dispute_create.html"
	account = Account.objects.get(user=request.user)
	
	if request.method == "POST":
		name = request.POST["name"]
		summary = request.POST["summary"]
		parties = request.POST.getlist("parties")
		print(parties)
		selected_categories = request.POST.getlist("categories")
		
		dispute = Dispute.objects.create(name=name, summary=summary, creator=account)
		
		for category in selected_categories:
			cat = Category.objects.get(name=category)
			dispute.categories.add(cat)
		dispute.save()
		
		for party in parties:
			acc = Account.objects.filter(email=party)
			if acc:
				dispute.parties.add(acc[0])
		dispute.parties.add(account)
		dispute.save()
		
		return redirect("core:dispute", id=dispute.id)
	else:
		context = {
			"categories": Category.objects.all(),
			"account": account,
		}
		return render(request, template, context)
		
def delete_dispute(request):
	if request.method == "POST":
		dispute_id = request.POST["dispute_id"]
		dispute = Dispute.objects.get(id=dispute_id)
		if dispute.creator == request.account:
			dispute.delete()
		else:
			return redirect("core:dispute", id=dispute.id)
	else:
		return redirect("core:dispute", id=dispute.id)

def view_dispute(request, id):
	dispute = Dispute.objects.get(id=id)
	account = Account.objects.get(user=request.user)
	template = "core/dispute.html"
	context = {
		"dispute": dispute,
		"account": account,
	}
	return render(request, template, context)
	

def create_session(request, id):
	template = "core/session_create.html"
	dispute = Dispute.objects.get(id=id)
	mediator = Mediator.objects.all()[0]
	account = Account.objects.get(user=request.user)
	
	if request.method == "POST":
		datetime = request.POST["datetime"]
		datetime = date_parser(datetime)
		
		session = Session.objects.create(datetime=datetime, dispute=dispute, mediator=mediator)
		
		for party in dispute.parties.all():
			session.parties.add(party)
		session.save()
		return redirect("core:session", id=session.id)
		
	else:
		context = {
			"dispute": dispute,
			"mediators": Mediator.objects.all(),
			"account": account,
			"mediator": mediator,
		}
		return render(request, template, context)
		
		
def view_session(request, id):
	template = "core/session.html"
	account = Account.objects.get(user=request.user)
	session = Session.objects.get(id=id)
	context = {
		"session": session,	
		"account": account,
	}
	return render(request, template, context)
	

def upload_file(request, id):
	session = Session.objects.get(id=id)
	
	if request.FILES.get("upload_file[]"):
		for _file in request.FILES.getlist("upload_file[]"):
			file_name = _file.name
			file_type = file_name.split(".")[-1]
			file_size = Decimal(_file.size / (1024 * 1024))
			
			session_file = SessionFile.objects.create(file_name=file_name, file_type=file_type, file_size=file_size, session=session, file=_file)
			session_file.save()
			
			return redirect("core:session", id=id)
			
	else:
		return redirect("core:session", id=session.id)


@require_http_methods(["POST"])
def new_message(request):
	user = request.user
	if request.method == "POST":
		message = request.POST["message"]
		session_id = request.POST["session_id"]
		session = Session.objects.get(id=session_id)
		
		ses_message = SessionMessage.objects.create(session=session, content=message, sender=user)
		
		account = Account.objects.filter(user=user)
		mediator = Mediator.objects.filter(user=user)
		
		if account:
			sender = account[0]
		elif mediator:
			sender = mediator[0]

		context = {
			"sender_image_url": sender.image.url,
			"sender_name": sender.fullname(),
			"message": ses_message.content,
			"message_time": ses_message.timestamp,
		}
		
		return JsonResponse(context)
		

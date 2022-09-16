from django.db import models
from accounts.models import Account, Mediator, Category, Language

# Create your models here.

class Dispute(models.Model):
	name = models.CharField(blank=True, null=True, max_length=250)
	summary = models.TextField(blank=True, null=True)
	creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="dispute_creator")
	parties = models.ManyToManyField(Account, related_name="dispute_parties")
	date_opened = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category)
	is_ended = models.BooleanField(default=False)

	def __str__(self):
		return self.name

		
class Session(models.Model):
	dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE)
	mediator = models.ForeignKey(Mediator, on_delete=models.CASCADE)
	parties = models.ManyToManyField(Account)
	created = models.DateTimeField(auto_now_add=True)
	datetime = models.DateTimeField()
	
	def __str__(self):
		return str(self.datetime)
		
	def files(self):
		return SessionFile.objects.filter(session=self)
		
	def messages(self):
		return SessionMessage.objects.filter(session=self)
		
		
class SessionFile(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	file = models.FileField(upload_to="files")
	file_name = models.CharField(max_length=320, blank=True, null=True)
	file_type = models.CharField(max_length=10, blank=True, null=True)
	file_size = models.CharField(max_length=10, blank=True, null=True)
	date_uploaded = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.file_name


class SessionMessage(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	content = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.content

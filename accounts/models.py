from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Language(models.Model):
	name = models.CharField(blank=True, null=True, max_length=250)
	
	def __str__(self):
		return self.name

class Affiliation(models.Model):
	name = models.CharField(blank=True, null=True, max_length=300)
	
	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(blank=True, null=True, max_length=300)
	
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
	
	def __str__(self):
		return self.name
		
class Qualification(models.Model):
	name = models.CharField(blank=True, null=True, max_length=300)
	institution = models.CharField(blank=True, null=True, max_length=300)
	date_acquired = models.DateField()
	
	def __str__(self):
		return self.name
		
class Account(models.Model):
	image = models.ImageField(upload_to="images")
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(blank=True, null=True, max_length=250)
	last_name = models.CharField(blank=True, null=True, max_length=250)
	email = models.CharField(blank=True, null=True, max_length=250)
	phone = models.IntegerField()
	languages = models.ManyToManyField(Language)
	
	def fullname(self):
		return f"{self.first_name} {self.last_name}"
	
	def __str__(self):
		return self.fullname()
		
class Mediator(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images")
	first_name = models.CharField(blank=True, null=True, max_length=250)
	last_name = models.CharField(blank=True, null=True, max_length=250)
	email = models.CharField(blank=True, null=True, max_length=250)
	phone = models.IntegerField()
	location = models.CharField(blank=True, null=True, max_length=100)
	qualifications = models.ManyToManyField(Qualification, blank=True)
	summary = models.TextField(blank=True, null=True)
	affiliations = models.ManyToManyField(Affiliation, blank=True)
	categories = models.ManyToManyField(Category, blank=True)
	languages = models.ManyToManyField(Language)
	
	def fullname(self):
		return f"{self.first_name} {self.last_name}"
		
	def __str__(self):
		return self.fullname()
	

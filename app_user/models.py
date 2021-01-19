from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	phone = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	address = models.TextField()

	pub_date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.user.username
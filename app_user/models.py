from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class AppUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	order_id = models.CharField(max_length=500, default="03inim4f")
	phone = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	address = models.TextField()
	delivery_state = models.CharField(max_length=500, default="nowhere")

	pub_date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.user.username
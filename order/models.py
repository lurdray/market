from django.db import models
from cart.models import Cart
from app_user.models import AppUser
from django.utils import timezone


# Create your models here.

class Order(models.Model):
	app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE, default="")
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default="")
	order_note = models.TextField(default="Nothing")
	status = models.CharField(max_length=150, default="Pending")
	pub_date = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return self.app_user.name
	
	

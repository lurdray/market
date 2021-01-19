from django.db import models
from product.models import Product, ProductQuantity
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Cart(models.Model):
	product_quantitys = models.ManyToManyField(ProductQuantity, through="CartProductQuantityConnector", through_fields=("cart", "product_quantity"),)
	total_price = models.IntegerField(blank=True, null=True)
	total_products = models.IntegerField(blank=True, null=True)
	cart_id = models.CharField(max_length=150)
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
	pub_date = models.DateTimeField(default=timezone.now)
	
	
	def __str__(self):
		#return self.cart_id
		return str(self.user.username)

		
class CartProductQuantityConnector(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default="")
	product_quantity = models.ForeignKey(ProductQuantity, on_delete=models.CASCADE, default="")
	pub_date = models.DateTimeField(default=timezone.now)


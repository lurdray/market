from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class Review(models.Model):
	name = models.CharField(max_length=150, default="none")
	email = models.CharField(max_length=150, default="none")
	review = models.TextField(default="none")
	status = models.CharField(max_length=150, default="pending")
	pub_date = models.DateTimeField(default=timezone.now)
	
	
	
	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=150)
	tag_title = models.CharField(max_length=150, default="Sale")
	tag_title_color = models.CharField(max_length=150, default="orange")
	section = models.CharField(max_length=150, default="section_one")

	category = models.CharField(max_length=150, default=" ")

	image_1 = models.FileField(upload_to='product/image_1/', blank=True)
	image_2 = models.FileField(upload_to='product/image_2/', blank=True)
	image_3 = models.FileField(upload_to='product/image_3/', blank=True)
	image_4 = models.FileField(upload_to='product/image_4/', blank=True)
	image_5 = models.FileField(upload_to='product/image_5/', blank=True)
	image_6 = models.FileField(upload_to='product/image_6/', blank=True)

	video_link = models.CharField(max_length=150)
	pdf_link = models.CharField(max_length=150)

	description = models.TextField(default="none")
	specification = models.TextField(default="none")

	reviews = models.ManyToManyField(Review, through="ProductReviewConnector", through_fields=("product", "review"),)

	quantity = models.IntegerField(default=1)
	threshold = models.IntegerField(blank=True, null=True, default=1)
	price = models.IntegerField(default=1)
	old_price = models.IntegerField(default=1)
	rating = models.IntegerField(blank=True, null=True)
	shipping_charge = models.FloatField(default=1)

	delivery_info = models.CharField(max_length=150, default="none")

	#state shippings
	abia_shipping = models.IntegerField(default=1)
	adamawa_shipping = models.IntegerField(default=1)
	akwaibom_shipping = models.IntegerField(default=1)
	anambra_shipping = models.IntegerField(default=1)





	slug = models.SlugField(unique=True, default="rayslug")
	pub_date = models.DateTimeField(default=timezone.now)

	
	def save(self, *args, **kwargs):
		var = self.name +"-" + str(self.pub_date)
		self.slug = slugify(var)
		super().save(*args, **kwargs)
		
	def get_absolute_url(self):
		return "/product-detail/%s/"%self.slug
		
	def __str__(self):
		return self.name
		

class Quantity(models.Model):
	quantity = models.IntegerField(blank=True, null=True)

	def __str__(self):
		#never forget that _str_ function should never return an int
		return str(self.quantity)		
		
class ProductQuantity(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
	quantity = models.ForeignKey(Quantity, on_delete=models.CASCADE)
	total_shipping_charge = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.product.name)	

		
	
class ProductReviewConnector(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
	review = models.ForeignKey(Review, on_delete=models.CASCADE, default="")
	pub_date = models.DateTimeField(default=timezone.now)
	
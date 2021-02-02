from django.shortcuts import render, get_object_or_404
from product.models import Product, Quantity, ProductReviewConnector, ProductQuantity, Review
from cart.models import Cart, CartProductQuantityConnector

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate

from main.views import UserCreatorFunc
from django.contrib import messages

from geopy.distance import great_circle
import requests
import random

# Create your views here.

def GetDistance():
	ip_data= requests.get('http://ipinfo.io/json').json()
	client_latlon = ip_data['loc']
	#base_latlon = (6.4474, 3.3903)
	base_latlon = (10.5105, 7.4165)
	#base_latlon = (9.0579,7.4951)
	
	
	return great_circle(client_latlon, base_latlon).miles



def BuyNowView(request, slug):
	quantity = 1
	quantity = Quantity.objects.create(quantity=quantity)
	quantity.save()
		
	user_id = request.user.id
		
	cart = get_object_or_404(Cart, user__pk=user_id)
	product = get_object_or_404(Product, slug=slug)
	
	#code for checking if the customer orders more than the available quantity
	if product.quantity < 1:
		messages.success(request, "Sorry, There are not enough amout of this product.")
		return HttpResponseRedirect(reverse("main:index"))
			
	else:
		product.quantity -= 1
		product.save()
		#distance = GetDistance()
		#total_shipping_charge = product.shipping_charge * distance
		total_shipping_charge = 0

		product_quantity = ProductQuantity.objects.create(product=product, quantity=quantity, total_shipping_charge=total_shipping_charge)
		product_quantity.save()
		
		cp = CartProductQuantityConnector(cart=cart, product_quantity=product_quantity)
		cp.save()
		messages.success(request, "Product Successfully Added to Cart")

		return HttpResponseRedirect(reverse("checkout:checkout"))





def ProductDetailView(request, slug):
	if request.method == "POST":
		quantity_k = int(str(request.POST.get("quantity")))
		quantity = Quantity.objects.create(quantity=quantity_k)
		quantity.save()
	
		user_id = request.user.id
	
		cart = get_object_or_404(Cart, user__pk=user_id)
		product = get_object_or_404(Product, slug=slug)
	
		#var = "%s, %s" % (product.quantityhgfrxcv, quantity)
		#return HttpResponse(var)
		#code for checking if the customer orders more than the available quantity
		if quantity_k > product.quantity:
			messages.success(request, "Sorry, There are not enough amout of this product.")
			return HttpResponseRedirect(reverse("product:all_products"))

		else:
			product.quantity -= quantity_k
			product.save()
			#distance = GetDistance()
			#total_shipping_charge = (product.shipping_charge * distance)
			total_shipping_charge = 0

			product_quantity = ProductQuantity.objects.create(product=product, quantity=quantity, total_shipping_charge=total_shipping_charge)
			product_quantity.save()
	
			cp = CartProductQuantityConnector(cart=cart, product_quantity=product_quantity)
			cp.save()
			messages.success(request, "Product Successfully Added to Cart")
	
			return HttpResponseRedirect(reverse("main:index"))



	else:
		UserCreatorFunc(request)	
		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		product = Product.objects.get(slug=slug)
		section_one = sorted(Product.objects.filter(section="section_one").order_by("-pub_date"), key=lambda x: random.random())[:2]
		section_two = sorted(Product.objects.filter(section="section_two").order_by("-pub_date"), key=lambda x: random.random())[:10]
		section_three = sorted(Product.objects.filter(section="section_three").order_by("-pub_date"), key=lambda x: random.random())[:10]
		related_products = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())[:10]

		reviews = product.reviews.all()
		review_list = []
		for item in reviews:
			if item.status == "ray":
				review_list.append(item)

		all_products = Product.objects.all()
		total_price = "{:,.2f}".format(total_price)
		context = {"reviews": review_list, "related_products": related_products, "total_price": total_price, "product_quantitys": product_quantitys, "product": product, "section_one": section_one, "section_two": section_two, "section_three": section_three, "all_products": all_products}
		
		return render(request, 'product/product_detail.html', context)




def ProductReviewView(request, slug):
	if request.method == "POST":
		product = get_object_or_404(Product, slug=slug)

		name = request.POST.get('name')
		email = request.POST.get('email')
		review = request.POST.get('review')

		review = Review.objects.create(name=name, email=email, review=review)
		review.save()

		pc = ProductReviewConnector(product=product, review=review)
		pc.save()

		messages.success(request, "Review Submitted Successfully.")
		return HttpResponseRedirect(reverse("product:product_detail", args=(product.slug,)))


	else:
		return HttpResponseRedirect(reverse("main:index"))


def AllProductView(request):
	if request.method == "POST":
		pass
		
		
	else:
		UserCreatorFunc(request)
		
		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))
	
		products = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())

		total_price = "{:,.2f}".format(total_price)
		context = {"total_price": total_price, "product_quantitys": product_quantitys, "products": products}
		return render(request, 'product/all_product.html', context)



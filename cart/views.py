from django.shortcuts import render, get_object_or_404

from product.models import Product, ProductQuantity, Quantity
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



def AddProductCartView(request, slug):
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
	
		return HttpResponseRedirect(reverse("main:index"))


def RemoveProductCartView(request, slug):
	cart = get_object_or_404(Cart, user__pk=request.user.id)
	product_quantitys = cart.product_quantitys.all()
	for item in product_quantitys:
		if item.product.slug == slug:
			product = get_object_or_404(Product, slug=slug)
			product_quantity = get_object_or_404(ProductQuantity, quantity=item.quantity, product=product)
			product_quantity.delete()
			cart.save()
		else:
			pass
			
	return HttpResponseRedirect(reverse("cart:cart_detail", args=(request.user.id,)))



def CartDetailView(request, user_id):
	if request.method == "POST":
		pass
		
	else:
		UserCreatorFunc(request)

		cart = get_object_or_404(Cart, user__pk=request.user.id)

		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			qty = int(str(item.quantity))
			total_price += (item.product.price * qty) + (item.total_shipping_charge * qty)
	
		total_price = "{:,.2f}".format(total_price)
		section_two = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())[:6]
		context = {"total_price": total_price, "product_quantitys": product_quantitys, "cart": cart, "section_two": section_two}
		return render(request, 'cart/cart_detail.html', context)



def DeleteCartView(request):
	pass

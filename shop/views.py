from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from main.views import UserCreatorFunc
from product.models import *
from cart.models import *

import random

# Create your views here.


def ShopView(request):
	if request.method == "POST":
		review = request.POST.getlist('review')
		ratings = review
		min_value = int(request.POST.get('min_value'))
		max_value = int(request.POST.get('max_value'))
		
		availability = request.POST.get('availability')		
		colors = request.POST.getlist('colors')
		
		#return HttpResponse(ratings)
		
		all_products = Product.objects.all()
		filtered_products = set()
		for item in all_products:
			if item.price >=min_value and item.price <=max_value:
				filtered_products.add(item)

			#for i, j in zip(colors, list(item.colors.all())):
			#	if i == j:
			#		filtered_products.add(item)
			#	else:
			#		pass
					
				
		for rating in ratings:
			rate_match_products = Product.objects.filter(rating=int(rating))
			for eachitem in rate_match_products:
				filtered_products.add(eachitem)
				
		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))
				
		page_title = "Filtered Products"
		context = {"total_price": total_price, "product_quantitys": product_quantitys, "products": filtered_products, "page_title": page_title}
		return render(request, 'product/all_product.html', context)	
		

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

		products = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())[:12]


		context = {"total_price": total_price, "product_quantitys": product_quantitys, "cart": cart, "products": products}

		return render(request, 'shop/shop.html', context)





		

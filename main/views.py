import random
import string
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from product.models import Product
from django.contrib import messages
from cart.models import Cart
from order.models import Order
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


# Create your views here.


def get_state_shipping(product_slug, delivery_state):
	product = Product.objects.get(slug=product_slug)

	if delivery_state == "abia":
		state_shipping = product.abia_shipping

	elif delivery_state == "adamawa":
		state_shipping = product.adamawa_shipping

	elif delivery_state == "akwaibom":
		state_shipping = product.akwaibom_shipping

	elif delivery_state == "anambra":
		state_shipping = product.anambra_shipping

	else:
		state_shipping = 0




	return state_shipping 




def ray_randomiser(length=6):
	landd = string.ascii_letters + string.digits
	return ''.join((random.choice(landd) for i in range(length)))




def UserCreatorFunc(request):
	if request.user.is_active:
		user = request.user
		user = User.objects.get(id=user.id)
		user_checker = authenticate(username=user.username, password=user.password)
		#pass
		#return HttpResponse("issues ooo!")
	else:
		#return HttpResponse("i reached here ooo!")
		fake_username = "%s" % (ray_randomiser())
		fake_password = "%s" % (ray_randomiser())
		user = User.objects.create(username=fake_username)
		user.save()
		user.set_password(fake_password)
		user.save()
		user_checker = authenticate(username=fake_username, password=fake_password)
		
		if user.is_active:
			login(request, user_checker)
		else:
			pass

		cart = Cart.objects.create(user=user, pub_date=timezone.now())
		cart.user = user
		cart.save()


def IndexView(request):

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
	
		product = Product.objects.all()

		all_products = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())
		section_one = sorted(Product.objects.filter(section="section_one").order_by("-pub_date"), key=lambda x: random.random())[:2]
		section_two = sorted(Product.objects.filter(section="section_two").order_by("-pub_date"), key=lambda x: random.random())[:10]
		section_three = sorted(Product.objects.filter(section="section_three").order_by("-pub_date"), key=lambda x: random.random())[:10]
		section_four = sorted(Product.objects.filter(section="section_four").order_by("-pub_date"), key=lambda x: random.random())[:10]
		section_five = sorted(Product.objects.filter(section="section_five").order_by("-pub_date"), key=lambda x: random.random())[:10]
	
		#return HttpResponse(section_four)
		total_price = "N{:,.2f}".format(total_price)
		context = {"total_price": total_price, "product_quantitys": product_quantitys, "product": product, "all_products": all_products, "section_one": section_one, "section_two": section_two, "section_three": section_three, "section_four": section_four, "section_five": section_five}
		return render(request, 'main/index.html', context)




def CategoryView(request, category):
	if request.method == "POST":
		return HttpResponseRedirect(reverse("main:index"))
		
		
	else:
		UserCreatorFunc(request)

		products = Product.objects.filter(category=category)

		product_one = Product.objects.all()
		product_two = Product.objects.all()


		#product_one = Product.objects.filter(category=category)
		#product_two = Product.objects.filter(category=category)

		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		total_price = "N{:,.2f}".format(total_price)
		context = {"category": category, "total_price": total_price, "product_quantitys": product_quantitys, 'product_one': product_one, "product_two": product_two}
		return render(request, 'main/category.html', context)







def SearchView(request):
	if request.method == "POST":
		query = request.POST.get('query')
		category = request.POST.get('category')
		if category == None:
			category = "ALL"
			products = Product.objects.filter(name__icontains=query)

		elif category == "ALL":
			products = Product.objects.filter(name__icontains=query)

		else:
			products = Product.objects.filter(name__icontains=query, category=str(category))
		
		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		total_price = "N{:,.2f}".format(total_price)
		context = {"total_price": total_price, "product_quantitys": product_quantitys, 'products': products}
		return render(request, 'product/all_product.html', context)

		
		
	else:
		return HttpResponseRedirect(reverse("main:index"))
	





def FaqsView(request):
	if request.method == "POST":
		return HttpResponseRedirect(reverse("main:index"))
		
		
	else:
		UserCreatorFunc(request)
		
		products = Product.objects.all()[:10]

		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		total_price = "N{:,.2f}".format(total_price)
		context = {"total_price": total_price, "product_quantitys": product_quantitys, 'products': products}
		return render(request, 'main/faqs.html', context)


def PrivacyView(request):
	if request.method == "POST":
		return HttpResponseRedirect(reverse("main:index"))
		
		
	else:
		UserCreatorFunc(request)
		
		products = Product.objects.all()[:10]

		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		total_price = "N{:,.2f}".format(total_price)
		context = {"total_price": total_price, "product_quantitys": product_quantitys, 'products': products}
		return render(request, 'main/privacy.html', context)



def TermsConditionView(request):
	if request.method == "POST":
		return HttpResponseRedirect(reverse("main:index"))
		
		
	else:
		UserCreatorFunc(request)
		
		products = Product.objects.all()[:10]

		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))

		total_price = "N{:,.2f}".format(total_price)

		context = {"total_price": total_price, "product_quantitys": product_quantitys, 'products': products}
		return render(request, 'main/terms.html', context)



def ShippingView(request):
	if request.method == "POST":
		return HttpResponseRedirect(reverse("main:index"))
		
		
	else:
		UserCreatorFunc(request)
		
		products = Product.objects.all()[:10]

		cart = get_object_or_404(Cart, user__pk=request.user.id)
		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))


		total_price = "N{:,.2f}".format(total_price)
		
		context = {"total_price": total_price, "product_quantitys": product_quantitys, 'products': products}
		return render(request, 'main/shipping.html', context)




def  AdminUserView(request):
	if request.user.is_superuser == True:
		if request.method == "POST":
			return HttpResponseRedirect(reverse("main:index"))
			
			
		else:
			
			orders = Order.objects.all().order_by("-pub_date")

			context = {"orders": orders}
			return render(request, 'main/admin_user.html', context)

	else:
		return HttpResponse("Not Authorised!, Contact ICT Unit(Interior Woodwork Limited)")		












def UserLogoutView(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))





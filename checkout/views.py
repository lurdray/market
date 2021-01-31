from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from main.views import UserCreatorFunc, get_state_shipping, ray_randomiser
from cart.models import Cart
from order.models import Order
from app_user.models import AppUser
from product.models import Product


# Create your views here.

def CheckoutView(request):
	user_id = request.user.id
	if request.method == "POST":
		name = request.POST.get("name")
		phone = request.POST.get("phone")
		email = request.POST.get("email")
		address = request.POST.get("address")
		delivery_state = request.POST.get("delivery_state")

		order_note = request.POST.get("order_note")

		try:
			app_user = AppUser.objects.get(user=request.user)
			app_user.name = name
			app_user.phone = phone
			app_user.email = email
			app_user.address = address
			app_user.delivery_state = delivery_state
			app_user.order_note = order_note
			app_user.save()

		except:
			app_user = AppUser.objects.create(user=request.user, name=name, phone=phone, email=email, address=address, delivery_state=delivery_state)
			app_user.order_id = ray_randomiser()
			app_user.save()
		
		cart = get_object_or_404(Cart, user__pk=request.user.id)

		delivery_state = app_user.delivery_state

		product_quantitys = cart.product_quantitys.all()
		total_price = 0
		total_quantity = 0
		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (get_state_shipping(item.product.slug, delivery_state) * int(str(item.quantity)))
			#total_quantity += int(str(item.quantity))
		
		#messages.success(request, "Dear " +name+ ", you have successfully placed your order." )
		cart.total_price = total_price
		cart.save()

		order = Order.objects.create(app_user=app_user, cart=cart, order_note=order_note)
		order.save()
		#total_price = total_price * total_quantity
		
		
		
		#paystack comes in here
		#return HttpResponse("i got here moda fucker!")
		
		return HttpResponseRedirect(reverse("checkout:complete_order", args=(order.id,)))


		
	else:
		UserCreatorFunc(request)
		cart = get_object_or_404(Cart, user__pk=request.user.id)

		try:
			app_user = AppUser.objects.get(user__pk=request.user.id)
		except:
			app_user = None

		product_quantitys = cart.product_quantitys.all()

		total_price = 0
		total_quantity = 0

		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (item.total_shipping_charge * int(str(item.quantity)))
			
		if total_price == 0:
			return HttpResponseRedirect(reverse("checkout:checkout"))
		elif total_price > 0:
			if app_user:
				total_price = "N{:,.2f}".format(total_price)
				context = {"app_user": app_user, "total_price": total_price, "cart": cart, "product_quantitys": product_quantitys}
			else:
				total_price = "N{:,.2f}".format(total_price)
				context = {"total_price": total_price, "cart": cart, "product_quantitys": product_quantitys}
			return render(request, 'checkout/checkout.html', context)
		else:
			return HttpResponseRedirect(reverse("main:index"))





def PayView(request, order_id):
	UserCreatorFunc(request)
	order = get_object_or_404(Order, id=order_id, cart__user=request.user)

	context = {"order": order}
	return render(request, 'checkout/pay.html', context)




def ConfirmPaymentView(request, order_id):
	if request.method == "POST":
		status = "Confirmed"

		order = get_object_or_404(Order, id=order_id, cart__user=request.user)
		order.status = status	
		order.save()

		#here we reduce product quantity as planned
		cart = order.cart

		product_quantitys = cart.product_quantitys.all()
		for item in product_quantitys:
			product = Product.objects.get(slug=item.product.slug)
			product.quantity -= int(str(item.quantity))
			product.save()
		

		logout(request)
		return HttpResponseRedirect(reverse("main:index"))
		
	else:
		UserCreatorFunc(request)
		context = {}
		return render(request, 'checkout/confirm_payment.html', context)




def CompleteOrderView(request, order_id):
	if request.method == "POST":
		status = "Confirmed"

		order = get_object_or_404(Order, id=order_id, cart__user=request.user)
		order.status = status	
		order.save()

		#here we reduce product quantity as planned
		cart = order.cart

		product_quantitys = cart.product_quantitys.all()
		for item in product_quantitys:
			product = Product.objects.get(slug=item.product.slug)
			product.quantity -= int(str(item.quantity))
			product.save()
		

		logout(request)
		messages.success(request, "Dear " +order.app_user.name  +", you have successfully placed your order." )

		return HttpResponseRedirect(reverse("main:index"))
		
	else:
		UserCreatorFunc(request)
		cart = get_object_or_404(Cart, user__pk=request.user.id)

		try:
			app_user = AppUser.objects.get(user__pk=request.user.id)
		except:
			app_user = None

		delivery_state = app_user.delivery_state

		product_quantitys = cart.product_quantitys.all()
		shippings = []

		total_price = 0
		total_quantity = 0

		for item in product_quantitys:
			total_price += (item.product.price * int(str(item.quantity))) + (get_state_shipping(item.product.slug, delivery_state) * int(str(item.quantity)))
			shippings.append("N{:,.2f}".format((get_state_shipping(item.product.slug, delivery_state) * int(str(item.quantity)))))

		shippings_product_quantitys = zip(product_quantitys, shippings)
		total_price = "N{:,.2f}".format(total_price)

		context = {"app_user": app_user, "total_price": total_price, "cart": cart, "shippings_product_quantitys": shippings_product_quantitys}
		return render(request, 'checkout/complete.html', context)






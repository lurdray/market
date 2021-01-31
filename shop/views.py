from django.shortcuts import render

# Create your views here.


def ShopView(request):
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
	
		total_price = "N{:,.2f}".format(total_price)

		section_two = sorted(Product.objects.all().order_by("-pub_date"), key=lambda x: random.random())[:12]


		context = {"total_price": total_price, "product_quantitys": product_quantitys, "cart": cart, "section_two": section_two}

		return render(request, 'shop/shop.html', context)


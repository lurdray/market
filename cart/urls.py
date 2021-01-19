from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [

	path('add-product-to-cart/<slug:slug>/', views.AddProductCartView, name="add_product_to_cart"),
	path("remove-product-from-cart/<slug:slug>/", views.RemoveProductCartView, name="remove_product_cart"),
	path("cart-detail/<int:user_id>/", views.CartDetailView, name="cart_detail"),
	path("delete-cart/<int:card_id>/", views.DeleteCartView, name="delete_cart"),

]


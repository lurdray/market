from django.urls import path
from . import views

app_name = "product"

urlpatterns = [

	path("product-detail/<slug:slug>/", views.ProductDetailView, name="product_detail"),
	path("buy-now/<slug:slug>/", views.BuyNowView, name="buy_now"),
	path("product-review/<slug:slug>", views.ProductReviewView, name="product_review"),
	path("all-product/", views.AllProductView, name="all_products"),

]



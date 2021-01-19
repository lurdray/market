from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [

	path("checkout", views.CheckoutView, name="checkout"),
	path("pay/<int:order_id>/", views.PayView, name="pay"),
	path("confirm-payment/<int:order_id>/", views.ConfirmPaymentView, name="confirm_payment"),
	
]

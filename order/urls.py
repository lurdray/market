from django.urls import path
from . import views

app_name = "order"

urlpatterns = [

	path("add-order/<int:cart_id>/", views.AddOrderView, name="add_order"),

]

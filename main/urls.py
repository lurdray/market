from django.urls import path
from . import views

app_name = "main"

urlpatterns = [

	path("", views.IndexView, name="index"),
	path("search", views.SearchView, name="search"),
	path("category/<str:category>/", views.CategoryView, name="category"),

	path("faqs/", views.FaqsView, name="faqs"),
	path("privacy/", views.PrivacyView, name="privacy"),
	path("terms-and-condition/", views.TermsConditionView, name="termscondition"),
	path("shipping/", views.ShippingView, name="shipping"),

	path("admin-user/", views.AdminUserView, name="admin_user"),


	path("userlogout/", views.UserLogoutView, name="userlogout"),
]



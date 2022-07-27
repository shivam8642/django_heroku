from django.contrib import admin
from django.urls import path
from project import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name="index"),
    path('createuser',views.createuser,name="createuser"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path('cart',views.cart,name="cart"),
    path('cartdata',views.cartdata,name="cartdata"),
    path("delete",views.deletecart,name="deletecart"),
    path('checkoutSession',views.checkoutSession,name="checkoutSession"),
    path("success",views.success,name="success"),
    path("account",views.account,name="account"),
    path('order',views.order,name="order"),
    path('updateProfile',views.updateProfile,name="updateProfile"),
    path("updateQuantity",views.updateQuantity,name="updateQuantity"),
    path("passwordchange",views.passwordchange,name="passwordchange"),
    path("password_reset",auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path("password_reset_done",auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path("password_reset_complete",auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
    path('add_address', views.add_address, name='add_address'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('checkout',views.checkout,name="checkout"),
    path('updateAddress/<int:id>',views.updateAddress,name="updateAddress"),
    path('delete_address/<int:id>',views.delete_address,name="delete_address")
]
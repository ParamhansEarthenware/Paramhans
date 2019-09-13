"""PARAMHANS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PARAMHANS import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
from MainApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home),
    path('adminpage/', views.Admin),
    path('AddProduct/', views.AddProduct),
    path('edit/<str:num>/', views.EditProduct),
    path('delete/<str:num>/', views.DeleteProduct),
    path('signup/', views.Signup),
    path('Login/', views.Login),
    path('logout/', views.Logout),
    path('shop/<str:cn>/', views.Shop),
    path('productdetails/<str:num>/', views.ProductDetails),
    path('cart/',views.CartDetails),
    path('cartdelete/<str:num>/', views.CartDelete),
    path('plus/<str:num>/', views.plus),
    path('minus/<str:num>/', views.minus),
    path('checkout/<str:num>/', views.CheckoutForm),
    path('addaddress/', views.Address),
    path('orderplaced/',views.OrderPlaced),
    path('deliveredorder/<str:num>/', views.OrderDelivered),
    path('lastorders/',views.LastOrders),
    path('ordered/',views.Ordered),
    path('AdminCorner/',views.AdminCorner),
]

urlpatterns=urlpatterns+staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
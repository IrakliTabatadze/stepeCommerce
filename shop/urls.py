
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
]
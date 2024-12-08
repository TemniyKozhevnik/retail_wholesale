from django.urls import path

from . import views

app_name = 'retail'

urlpatterns = [
    path('', views.retail_list, name='retail_list'),
    path('<int:pk>/', views.retail_detail, name='retail_detail'),
    path('add/', views.retail_add, name='retail_add'),
    path('<int:pk>/edit/', views.retail_add, name='retail_edit'),
    path('<int:pk>/delete/', views.retail_delete, name='retail_delete'),
    path('product_list', views.product_list, name='product_list'),
]
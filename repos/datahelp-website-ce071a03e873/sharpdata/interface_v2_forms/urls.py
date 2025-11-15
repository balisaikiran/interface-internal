from django.urls import path
from . import views

urlpatterns = [
    path('interface_form', views.interface_form, name='interface_form'),
    path('update_interface_form', views.update_interface_form, name='update_interface_form'),
    path('interface_list_view', views.interface_list_view, name='interface_list_view'),
    path('loader', views.loader, name='loader'),
    path('success', views.success, name='success'),
]

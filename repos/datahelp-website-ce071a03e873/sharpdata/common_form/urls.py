from django.urls import path
from . import views

urlpatterns = [
    path('form', views.common_form, name='common_form'),
    path('update_form', views.update_form, name='common_form'),
    path('wufoo_form', views.wufoo_form, name='wufoo_form'),
    path('update_wufoo_form', views.update_wufoo_form, name='update_wufoo_form'),
    path('list_view', views.list_view, name='list_view'),
    path('loader', views.loader, name='loader'),
    path('success', views.success, name='success'),
    path('common_form_fields', views.common_form_fields, name='common_form_fields'),
    path('update_form_fields', views.update_form_fields, name='update_form_fields'),
    path('appoinments', views.appoinments, name='appoinments'),
    path('one_click_emb_app', views.one_click_emb_app, name='one_click_emb_app')
]

from django.urls import path
from . import views

handler404 = 'sharpdata.views.handler404'
handler500 = 'sharpdata.views.handler500'

urlpatterns = [
    path('text-templates/', views.text_templates, name='text_templates'),
    path('edit_text_template/', views.edit_text_templates, name='edit_text_templates'),
    path('delete_text_template', views.delete_text_template, name="delete_text_template"),
]

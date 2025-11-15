from django.urls import path
from . import views

handler404 = 'sharpdata.views.handler404'
handler500 = 'sharpdata.views.handler500'

urlpatterns = [
    path('about', views.about, name='about'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('contact', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('twillio_agreement/', views.twillio_agreement, name="twillio_agreement"),
    path('sisu_fub_agreement/', views.sisu_fub_agreement, name="sisu_fub_agreement"),
    path('fub_report_agreement/', views.fub_report_agreement, name="fub_report_agreement"),
    path('disclosure/', views.disclosure, name="disclosure"),
    path('pricing/<str:plan>', views.pricing, name="pricing"),
    path('pricing/', views.pricing, name="pricing"),
    path('pricing_internal/<str:plan>', views.pricing_internal, name="pricing_internal"),
    path('pricing_internal/', views.pricing_internal, name="pricing_internal"),

]

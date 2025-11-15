from django.urls import path
from . import views


urlpatterns = [
    # path('payments/', views.payments , name='payments')
    path('plans/', views.plans, name='plan'),
    path('billing/', views.billing, name='billing'),
    path('fub-con-billing/', views.fubcon_billing, name='fub-con-billing'),
    path('billing/<str:plan_id>/', views.billing_plans, name='billing_plans'),
    path('generate_hp', views.generate_hp, name='generate_hp'),
    path("get_hosted_page", views.get_hosted_page, name="get_hosted_page"),
    path('success', views.success, name='success')
]

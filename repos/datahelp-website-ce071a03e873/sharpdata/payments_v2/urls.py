from django.urls import path
from . import views


urlpatterns = [
    # path('payments/', views.payments , name='payments')
    path("plans/", views.plans, name="plan"),
    path("billing/", views.billing, name="billing"),
    path("billing/<str:plan_id>/", views.billing_plans, name="billing_plans"),
    path("generate_hp", views.generate_hp, name="generate_hp"),
]

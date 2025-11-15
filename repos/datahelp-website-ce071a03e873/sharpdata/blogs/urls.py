from django.urls import path
from . import views
handler404 = 'sharpdata.views.handler404'
handler500 = 'sharpdata.views.handler500'

urlpatterns = [
    path('', views.blogboard, name='blogboard'),
    path('Real_Estate_MoneyBall', views.Real_Estate_MoneyBall, name='Real_Estate_MoneyBall'),
    path('Tech_is_an_Arms_Race', views.Tech_is_an_Arms_Race, name='Tech_is_an_Arms_Race'),
    path('The_Holy_Grail_of_Real_Estate', views.The_Holy_Grail_of_Real_Estate, name='The_Holy_Grail_of_Real_Estate'),
    path('scalability', views.scalability, name='scalability')
]

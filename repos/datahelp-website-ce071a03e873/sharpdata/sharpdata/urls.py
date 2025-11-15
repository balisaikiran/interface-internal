from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
handler404 = 'sharpdata.views.handler404'
handler500 = 'sharpdata.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('secure/', include('login.urls')),
    path('blogs/', include('blogs.urls')),
    path('', include('landing.urls')),
    path('user/', include('users.urls')),
    path('user/', include('text_templates.urls')),
    path('common_form/', include('common_form.urls')),
    path('calendly/<str:id>', views.calendly, name='calendly'),
    path('payments/', include('payments.urls')),
    path('health', views.health_check, name='health_check'),
    path('testsite', views.test_resp, name='testsite'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('chat/', include('chat_widget.urls')),
    path('interface_forms/', include('interface_v2_forms.urls'))
]

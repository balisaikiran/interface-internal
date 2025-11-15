from django.urls import path
from . import views

handler404 = 'sharpdata.views.handler404'
handler500 = 'sharpdata.views.handler500'

urlpatterns = [
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('edit_template/', views.edit_template, name='edit_template'),
    path('credential_form', views.credential_form, name='credential_form'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('heatmap', views.heatmap, name='heatmap'),
    path('wufoo_heatmap', views.wufoo_heatmap, name='wufoo_heatmap'),
    path('check_if_file_available', views.check_if_file_available, name="check_if_file_available"),
    path('fub_user_list', views.fub_user_list, name='fub_user_list'),
    path('update-fub-user', views.update_fub_user, name='update_fub_user'),
    path('add-fub-user', views.add_fub_user, name='add_fub_user'),
    path('delete_fub_user', views.delete_fub_user, name='delete_fub_user'),
    path('helper_get_credentials', views.helper_get_credentials, name='helper_get_cred'),
    path('helper_update_credentials', views.helper_update_credentials, name='helper_update_credentials'),
    path('helper_delete_credentials', views.helper_delete_credentials, name='helper_delete_credentials'),
    path('helper_webhook', views.helper_webhook, name='helper_webhook'),
    path('helper_transfer_property_fields', views.helper_transfer_property_fields, name='helper_transfer_property_fields'),
    path('helper_custom_activity_creation', views.helper_custom_activity_creation, name='helper_custom_activity_creation'),
    path('helper_sisu_custom_fields', views.helper_sisu_custom_fields, name='helper_sisu_custom_fields'),
    path('helper_twilio_fub_webhooks', views.helper_twilio_fub_webhooks, name='helper_twilio_fub_webhooks'),
    path('custom_field_mapping', views.helper_lambda_invoker, name='custom_field_mapping'),
    path('get_wufoo_form_fields', views.helper_lambda_invoker, name='get_wufoo_form_fields'),
    path('get_sisu_fields', views.helper_lambda_invoker, name='get_sisu_fields'),
    path('get_otc_fields', views.helper_lambda_invoker, name='get_otc_fields'),
    path('autoPopulateTagsForTagIntegration', views.helper_lambda_invoker, name='autoPopulateTagsForTagIntegration'),
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('test_action/', views.test_action, name='test_action'),
    path('get_user/', views.get_user, name='get_user'),
    path('get_fub_domain', views.get_fub_domain, name='get_fub_domain'),
    # path('chargeebee_checkout_page', views.chargeebee_checkout_page, name='chargeebee_checkout_page'),
]

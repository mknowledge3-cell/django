from django.urls import path
from . import views

urlpatterns = [
    # Business demo URLs
    path('business/', views.business_demo, name='business_demo'),
    path('business/about/', views.business_about, name='business_about_demo'),
    path('business/services/', views.business_services, name='business_services_demo'),
    path('business/contact/', views.business_contact, name='business_contact_demo'),
    path('business/admin/', views.business_admin, name='business_admin_demo'),
    path('business/reset/', views.reset_business_demo, name='reset_business_demo'),

    # Membership demo URLs
    path('membership/', views.membership_demo, name='membership_demo'),
    path('membership/login/', views.membership_login, name='membership_login_demo'),
    path('membership/register/', views.membership_register, name='membership_register_demo'),
    path('membership/dashboard/', views.membership_dashboard, name='membership_dashboard_demo'),
    path('membership/premium-content/', views.membership_premium_content, name='membership_premium_content_demo'),
    path('membership/admin/', views.membership_admin, name='membership_admin_demo'),
    path('membership/logout/', views.membership_logout, name='membership_logout_demo'),
    path('membership/reset/', views.reset_membership_demo, name='reset_membership_demo'),
]
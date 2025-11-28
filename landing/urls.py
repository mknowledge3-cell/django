from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]

urlpatterns += [
    path("school-portal/", views.school_portal, name="portfolio_school_portal"),
    path("business-site/", views.business_site, name="portfolio_business_site"),
    path("ecommerce/", views.ecommerce, name="portfolio_ecommerce"),
]
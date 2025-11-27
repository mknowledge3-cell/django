from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
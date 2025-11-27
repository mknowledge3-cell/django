from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'landing/index.html'

class ServicesView(TemplateView):
    template_name = 'landing/services.html'

class PortfolioView(TemplateView):
    template_name = 'landing/portfolio.html'

class ContactView(TemplateView):
    template_name = 'landing/contact.html'
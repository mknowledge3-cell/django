from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'landing/index.html'


class ServicesView(TemplateView):
    template_name = 'landing/services.html'


class PortfolioView(TemplateView):
    template_name = 'landing/portfolio.html'

def school_portal(request):
    return render(request, "portfolios/portfolio_school_portal.html")

def business_site(request):
    return render(request, "portfolios/portfolio_business_site.html")

def ecommerce(request):
    return render(request, "portfolios/portfolio_ecommerce.html")

class ContactView(TemplateView):
    template_name = 'landing/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the service parameter from URL
        service = self.request.GET.get('service', '')
        context['preselected_service'] = service
        return context
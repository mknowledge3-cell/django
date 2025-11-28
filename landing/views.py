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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage


def contact_view(request):
    if request.method == "POST":

        # Honeypot bot protection
        if request.POST.get("website"):
            return redirect("contact")  # Silently ignore bots

        name = request.POST.get("name")
        email = request.POST.get("email")
        service = request.POST.get("service")
        budget = request.POST.get("budget")
        message = request.POST.get("message")

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            service=service,
            budget=budget,
            message=message
        )

        # Email to YOU
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"""
Name: {name}
Email: {email}
Service: {service}
Budget: {budget}

Message:
{message}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )

        # Auto-reply
        send_mail(
            subject="We received your message!",
            message=f"Hello {name},\n\nThanks for reaching out! I'll get back to you shortly.\n\n– Khume Web Agency",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "landing/contact.html")

import os

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

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
class ContactView(View):
    template_name = 'landing/contact.html'

    def get(self, request):
        service = request.GET.get('service', '')
        return render(request, self.template_name, {'service': service})

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            service = request.POST.get('service', '').strip()
            message = request.POST.get('message', '').strip()

            # Basic validation
            if not all([name, email, message]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, self.template_name, {
                    'name': name,
                    'email': email,
                    'service': service,
                    'message': message
                })

            # Prepare email content
            subject = f"New Contact Form Submission - {service}" if service else "New Contact Form Submission"

            email_message = f"""
            New contact form submission from your website:

            Name: {name}
            Email: {email}
            Service: {service if service else 'Not specified'}

            Message:
            {message}

            ---
            This message was sent from your website contact form.
            """

            # Send email (use your actual email in production)
            recipient_email = 'mknowledge3@gmail.com'

            send_mail(
                subject=subject,
                message=email_message,
                from_email='info@khume.co.za',
                recipient_list=[recipient_email],
                fail_silently=False,
            )

            # Send confirmation to user
            user_subject = "Thank you for contacting us!"
            user_message = f"""
            Hi {name},

            Thank you for reaching out to us regarding our {service if service else 'services'}. 
            We have received your message and will get back to you within 24-48 hours.

            Best regards,
            Your Web Design Team
            """

            send_mail(
                subject=user_subject,
                message=user_message,
                from_email='info@khume.co.za',
                recipient_list=[email],
                fail_silently=True,
            )

            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')

        except BadHeaderError:
            messages.error(request, 'Invalid header found.')
            return render(request, self.template_name)
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
            return render(request, self.template_name, {
                'name': name,
                'email': email,
                'service': service,
                'message': message
            })

# landing/views.py
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

def contact_view(request):

    # Capture prefilled query parameters or defaults
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    service = request.POST.get("service", request.GET.get("service", ""))
    message_text = request.POST.get("message", "")

    if request.method == "POST":

        # Prepare Brevo client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email_data = sib_api_v3_sdk.SendSmtpEmail(
            sender={"name": "khume Website", "email": "info@khume.co.za"},
            to=[{"email": "mknowledge3@gmail.com"}],
            reply_to={"email": email},
            subject=f"New Contact Form Message ({service})",
            html_content=f"""
                <h2>New Contact Form Submission</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Service:</strong> {service}</p>
                <p><strong>Message:</strong><br>{message_text}</p>
            """,
        )

        try:
            api_instance.send_transac_email(email_data)
        except ApiException as e:
            print("Brevo Error:", e)

        return redirect("/contact?success=1")

    return render(request, "landing/contact.html", {
        "name": name,
        "email": email,
        "service": service,
        "message": message_text,
    })
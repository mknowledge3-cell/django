import os

from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'landing/index.html'

def services_view(request):
    # Track page view
    request.session['ga_event'] = 'view_services'
    return render(request, 'landing/services.html')

class ServicesView(TemplateView):
    template_name = 'landing/services.html'


class PortfolioView(TemplateView):
    template_name = 'landing/portfolio.html'

class AboutView(TemplateView):
    template_name = 'landing/about.html'

def school_portal(request):
    return render(request, "portfolios/portfolio_school_portal.html")

def business_site(request):
    return render(request, "portfolios/portfolio_business_site.html")

def ecommerce(request):
    return render(request, "portfolios/portfolio_ecommerce.html")

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, request
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

import requests
import urllib.parse

def send_whatsapp_notification(phone, api_key, message):
    try:
        encoded_message = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&apikey={api_key}&text={encoded_message}"
        requests.get(url, timeout=10)
    except Exception as e:
        print("WhatsApp notification error:", e)

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
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f7; padding:40px 0;">
              <tr>
                <td align="center">

                  <!-- Email Container -->
                  <table width="600" cellpadding="0" cellspacing="0" style="background:white; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08); font-family:Arial, sans-serif;">

                    <!-- Header -->
                    <tr>
                      <td style="background:linear-gradient(90deg, #6b21a8, #2563eb); padding:30px; text-align:center;">
                        <h1 style="color:white; margin:0; font-size:24px; font-weight:700; letter-spacing:0.5px;">New Contact Form Message</h1>
                        <p style="color:#e9d5ff; margin-top:8px; font-size:14px;">A new enquiry has been submitted via the Khume website.</p>
                      </td>
                    </tr>

                    <!-- Body -->
                    <tr>
                      <td style="padding:30px;">

                        <h2 style="font-size:20px; font-weight:600; color:#333; margin-top:0;">Lead Details</h2>

                        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px; color:#444; font-size:15px;">
                          <tr>
                            <td width="30%" style="font-weight:600; padding:8px 0;">Name:</td>
                            <td>{name}</td>
                          </tr>
                          <tr>
                            <td width="30%" style="font-weight:600; padding:8px 0;">Email:</td>
                            <td>{email}</td>
                          </tr>
                          <tr>
                            <td width="30%" style="font-weight:600; padding:8px 0;">Service:</td>
                            <td>{service}</td>
                          </tr>
                        </table>

                        <!-- Message Box -->
                        <div style="margin-top:25px; padding:18px; background:#fafafa; border-left:4px solid #6b21a8; border-radius:8px;">
                          <h3 style="margin-top:0; margin-bottom:10px; font-size:16px; color:#333;">Message</h3>
                          <p style="white-space:pre-line; margin:0; font-size:15px; line-height:1.6; color:#555;">
                            {message_text}
                          </p>
                        </div>

                      </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                      <td style="background:#f9fafb; padding:20px; text-align:center; font-size:12px; color:#999;">
                        <p style="margin:4px 0;">Khume Web Design & Development</p>
                        <p style="margin:4px 0;">hello@khume.co.za</p>
                      </td>
                    </tr>

                  </table>

                </td>
              </tr>
            </table>
            """

        )
        # Send confirmation email to client
        confirmation_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email}],
            sender={"email": "info@khume.co.za", "name": "khume Web Design"},
            subject="We've received your message – Thank you!",
            html_content=f"""
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f7; padding:40px 0;">
              <tr><td align="center">

                <table width="600" cellpadding="0" cellspacing="0" style="background:white; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.08); font-family:Arial, sans-serif;">

                  <!-- Header -->
                  <tr>
                    <td style="background:linear-gradient(90deg, #6b21a8, #2563eb); padding:30px; text-align:center;">
                      <h1 style="color:white; margin:0; font-size:24px; font-weight:700;">Thank You for Reaching Out</h1>
                      <p style="color:#e9d5ff; margin-top:8px; font-size:14px;">
                        We've received your message and will get back to you soon.
                      </p>
                    </td>
                  </tr>

                  <!-- Body -->
                  <tr>
                    <td style="padding:30px;">
                      <p style="font-size:16px; color:#333; margin-top:0;">
                        Hi {name},
                      </p>

                      <p style="font-size:15px; color:#555; line-height:1.6;">
                        Thank you for contacting <strong>Khume Web Design</strong>.  
                        Your enquiry has been received successfully and our team is now reviewing your project details.
                      </p>

                      <h3 style="margin-top:25px; font-size:16px; color:#333;">Your Submission:</h3>
                      <div style="background:#fafafa; border-left:4px solid #6b21a8; padding:15px; border-radius:8px; font-size:14px; color:#555;">
                        <p style="margin:0;"><strong>Service:</strong> {service}</p>
                        <p style="margin-top:8px; white-space:pre-line;"><strong>Message:</strong><br>{message_text}</p>
                      </div>

                      <p style="font-size:15px; color:#555; margin-top:25px; line-height:1.6;">
                        We usually respond within <strong>24–48 hours</strong>.  
                        If your request is urgent, you can also reply directly to this email.
                      </p>

                      <p style="margin-top:25px; font-size:15px; color:#333;">Warm regards,<br><strong>Khume Team</strong></p>
                    </td>
                  </tr>

                  <!-- Footer -->
                  <tr>
                    <td style="background:#f9fafb; padding:20px; text-align:center; font-size:12px; color:#999;">
                      <p style="margin:4px 0;">Khume Web Design & Development</p>
                      <p style="margin:4px 0;">hello@khume.co.za</p>
                    </td>
                  </tr>
                </table>

              </td></tr>
            </table>
            """
        )
        send_whatsapp_notification(
            phone="27787779683",
            api_key="9464038",
            message=f"New enquiry from {name}. Service: {service}. Check your email."
        )

        api_instance.send_transac_email(confirmation_email)

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

class DemosView(TemplateView):
    template_name = 'landing/demos.html'
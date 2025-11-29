from django.shortcuts import render, redirect
from django.contrib import messages
import json
import uuid

# Demo data for the business template
BUSINESS_DEMO_DATA = {
    'company_name': 'Strategic Growth Consulting',
    'tagline': 'Driving Business Transformation Through Digital Innovation',
    'about': {
        'mission': 'We help businesses scale through strategic digital solutions and data-driven insights.',
        'team': [
            {'name': 'Sarah Chen', 'role': 'Lead Consultant', 'bio': '10+ years in digital transformation'},
            {'name': 'Marcus Johnson', 'role': 'UX Strategist', 'bio': 'Specialized in user-centered design'},
            {'name': 'Elena Rodriguez', 'role': 'Data Analyst', 'bio': 'Turning data into actionable insights'},
        ]
    },
    'services': [
        {
            'name': 'Digital Strategy',
            'description': 'Comprehensive digital roadmap for business growth',
            'price': 'R8,000',
            'features': ['Market Analysis', 'Competitor Research', 'Strategy Development', 'Implementation Plan']
        },
        {
            'name': 'Web Design & Development',
            'description': 'Custom websites that convert visitors into customers',
            'price': 'R12,000 - R25,000',
            'features': ['Responsive Design', 'SEO Optimization', 'Content Management', 'Ongoing Support']
        },
        {
            'name': 'E-commerce Solutions',
            'description': 'Complete online store setup and optimization',
            'price': 'R18,000 - R35,000',
            'features': ['Product Management', 'Payment Integration', 'Inventory System', 'Sales Analytics']
        }
    ],
    'testimonials': [
        {'name': 'TechStart Inc.', 'text': 'Increased our online conversions by 150% in 3 months.', 'role': 'CEO'},
        {'name': 'Global Retail Co.', 'text': 'Their e-commerce solution streamlined our operations dramatically.',
         'role': 'Operations Director'},
        {'name': 'Innovate Labs', 'text': 'The digital strategy provided clear direction and measurable results.',
         'role': 'Founder'},
    ],
    'contact_requests': []
}


def business_demo(request):
    demo_data = request.session.get('business_demo_data', BUSINESS_DEMO_DATA.copy())
    return render(request, 'sandbox/business/index.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def business_about(request):
    demo_data = request.session.get('business_demo_data', BUSINESS_DEMO_DATA.copy())
    return render(request, 'sandbox/business/about.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def business_services(request):
    demo_data = request.session.get('business_demo_data', BUSINESS_DEMO_DATA.copy())
    return render(request, 'sandbox/business/services.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def business_contact(request):
    demo_data = request.session.get('business_demo_data', BUSINESS_DEMO_DATA.copy())

    if request.method == 'POST':
        # Simulate form submission
        contact_request = {
            'id': str(uuid.uuid4())[:8],
            'name': request.POST.get('name', ''),
            'email': request.POST.get('email', ''),
            'service': request.POST.get('service', ''),
            'message': request.POST.get('message', ''),
            'status': 'New'
        }

        if 'contact_requests' not in demo_data:
            demo_data['contact_requests'] = []
        demo_data['contact_requests'].append(contact_request)
        request.session['business_demo_data'] = demo_data
        request.session.modified = True

        messages.success(request, 'Thank you! Your demo inquiry has been received.')
        return redirect('business_contact_demo')

    return render(request, 'sandbox/business/contact.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def business_admin(request):
    demo_data = request.session.get('business_demo_data', BUSINESS_DEMO_DATA.copy())
    return render(request, 'sandbox/business/admin_dashboard.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def reset_business_demo(request):
    request.session['business_demo_data'] = BUSINESS_DEMO_DATA.copy()
    messages.info(request, 'Demo has been reset to original state.')
    return redirect('business_demo')


# Add to existing views.py

MEMBERSHIP_DEMO_DATA = {
    'site_name': 'Elite Learning Portal',
    'tagline': 'Unlock Your Potential With Premium Content',
    'pricing_tiers': [
        {
            'name': 'Free',
            'price': 'R0',
            'period': 'forever',
            'features': [
                'Access to basic courses',
                'Community forum',
                'Weekly newsletter',
                'Limited downloads'
            ],
            'button_text': 'Get Started Free',
            'highlighted': False
        },
        {
            'name': 'Pro',
            'price': 'R299',
            'period': 'per month',
            'features': [
                'All Free features',
                'Premium video courses',
                'Downloadable resources',
                'Priority support',
                'Certificate of completion'
            ],
            'button_text': 'Start Pro Trial',
            'highlighted': True
        },
        {
            'name': 'Enterprise',
            'price': 'R899',
            'period': 'per month',
            'features': [
                'All Pro features',
                'Team management',
                'Custom content',
                'API access',
                'Dedicated account manager'
            ],
            'button_text': 'Contact Sales',
            'highlighted': False
        }
    ],
    'courses': {
        'free': [
            {'title': 'Getting Started Guide', 'description': 'Basic introduction to our platform',
             'duration': '15 min'},
            {'title': 'Community Forum', 'description': 'Connect with other learners', 'duration': 'Ongoing'},
        ],
        'premium': [
            {'title': 'Advanced Masterclass', 'description': 'Deep dive into advanced techniques',
             'duration': '2 hours'},
            {'title': 'Expert Workshops', 'description': 'Live sessions with industry experts', 'duration': '4 hours'},
            {'title': 'Resource Library', 'description': 'Downloadable templates and tools', 'duration': 'Unlimited'},
        ]
    },
    'demo_users': {
        'free': {'email': 'free@demo.com', 'password': 'demo123', 'tier': 'free'},
        'pro': {'email': 'pro@demo.com', 'password': 'demo123', 'tier': 'pro'},
        'admin': {'email': 'admin@demo.com', 'password': 'demo123', 'tier': 'admin'}
    },
    'members': [],
    'content_access_log': []
}


def membership_demo(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())
    return render(request, 'sandbox/membership/index.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def membership_login(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # Check demo accounts
        for user_type, user_data in demo_data['demo_users'].items():
            if email == user_data['email'] and password == user_data['password']:
                request.session['membership_user'] = {
                    'email': email,
                    'tier': user_data['tier'],
                    'type': user_type
                }
                messages.success(request, f'Successfully logged in as {user_type} user!')
                return redirect('membership_dashboard_demo')

        messages.error(request, 'Invalid login credentials. Use demo accounts provided.')

    return render(request, 'sandbox/membership/login.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def membership_register(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        tier = request.POST.get('tier', 'free')

        # Add to demo members
        new_member = {
            'id': str(uuid.uuid4())[:8],
            'name': name,
            'email': email,
            'tier': tier,
            'join_date': '2024-01-15',
            'status': 'active'
        }

        if 'members' not in demo_data:
            demo_data['members'] = []
        demo_data['members'].append(new_member)
        request.session['membership_demo_data'] = demo_data
        request.session.modified = True

        # Auto-login as new user
        request.session['membership_user'] = {
            'email': email,
            'tier': tier,
            'type': 'new_member'
        }

        messages.success(request, f'Welcome {name}! Your {tier} account has been created.')
        return redirect('membership_dashboard_demo')

    return render(request, 'sandbox/membership/register.html', {
        'demo_data': demo_data,
        'demo_mode': True
    })


def membership_dashboard(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())
    user = request.session.get('membership_user')

    if not user:
        messages.warning(request, 'Please log in to access the member dashboard.')
        return redirect('membership_login_demo')

    return render(request, 'sandbox/membership/dashboard.html', {
        'demo_data': demo_data,
        'user': user,
        'demo_mode': True
    })


def membership_premium_content(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())
    user = request.session.get('membership_user')

    if not user:
        messages.warning(request, 'Please log in to access premium content.')
        return redirect('membership_login_demo')

    # Log access attempt
    access_log = {
        'user': user['email'],
        'tier': user['tier'],
        'content': 'premium_courses',
        'timestamp': '2024-01-15 10:30:00',
        'access_granted': user['tier'] in ['pro', 'enterprise', 'admin']
    }

    if 'content_access_log' not in demo_data:
        demo_data['content_access_log'] = []
    demo_data['content_access_log'].append(access_log)
    request.session['membership_demo_data'] = demo_data
    request.session.modified = True

    return render(request, 'sandbox/membership/premium_content.html', {
        'demo_data': demo_data,
        'user': user,
        'demo_mode': True
    })


def membership_admin(request):
    demo_data = request.session.get('membership_demo_data', MEMBERSHIP_DEMO_DATA.copy())
    user = request.session.get('membership_user')

    if not user or user['type'] != 'admin':
        messages.error(request, 'Admin access required. Use admin@demo.com / demo123')
        return redirect('membership_login_demo')

    return render(request, 'sandbox/membership/admin_dashboard.html', {
        'demo_data': demo_data,
        'user': user,
        'demo_mode': True
    })


def membership_logout(request):
    if 'membership_user' in request.session:
        del request.session['membership_user']
    messages.info(request, 'You have been logged out.')
    return redirect('membership_demo')


def reset_membership_demo(request):
    request.session['membership_demo_data'] = MEMBERSHIP_DEMO_DATA.copy()
    if 'membership_user' in request.session:
        del request.session['membership_user']
    messages.info(request, 'Membership demo has been reset to original state.')
    return redirect('membership_demo')
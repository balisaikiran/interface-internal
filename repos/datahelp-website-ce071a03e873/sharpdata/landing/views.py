from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


def home(request):
    return render(request, 'main/home.html')


def privacy(request):
    return render(request, 'main/privacy-policy.html')


def contact(request):
    return render(request, 'main/contact.html')


def terms(request):
    return render(request, 'main/terms.html')


def about(request):
    return render(request, 'main/about-company.html')


def twillio_agreement(request):
    return render(request, 'main/twilio_agreement.html')


def sisu_fub_agreement(request):
    return render(request, 'main/sisu_fub_agreement.html')


def fub_report_agreement(request):
    return render(request, 'main/fub_report_agreement.html')


def disclosure(request):
    return render(request, 'main/disclosure.html')


def pricing(request, plan=None, internal=False):
    if internal:
        # without header and footer
        base_template = 'payments/base.html'
        route = 'pricing_internal'
    else:
        # with header and footer
        base_template = 'main/main-base.html'
        route = 'pricing'
    if plan in ["fub-only", "fub-sisu", "fub-otc", "fub-sisu-otc"]:
        html_file = f'payments/{plan}.html'
    else:
        html_file = 'payments/pricing.html'
    plan_template = render(request, html_file, context={'override_base': base_template, 'route': route})
    return plan_template


@xframe_options_exempt
def pricing_internal(request, plan=None):
    return pricing(request, plan, internal=True)

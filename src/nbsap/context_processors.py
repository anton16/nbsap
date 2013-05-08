from django.conf import settings
import re

pattern = re.compile(r"^/administration/")

def nbsap_admin(request):
    if re.search(pattern, request.path):
        redirect_to = '/administration'
    else:
        redirect_to = '/'

    return {
        'EU_STRATEGY': getattr(settings, 'EU_STRATEGY', ''),
        'SITE_HEADER': getattr(settings, 'SITE_HEADER', ''),
        'redirect_to': redirect_to,
    }

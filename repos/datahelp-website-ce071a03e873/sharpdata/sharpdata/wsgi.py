"""
WSGI config for sharpdata project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharpdata.settings')

sys.path.append('/var/www/sharpdata/front-end/sharpdata')
sys.path.append('/var/www/front-end/sharpdata')
# application = get_wsgi_application()

application = get_wsgi_application()

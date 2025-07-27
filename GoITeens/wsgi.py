"""
WSGI config for GoITeens project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.insert(0, "C:/Users/Роман/PycharmProjects/sessons/GoITeens")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GoITeens.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

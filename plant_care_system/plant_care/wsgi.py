# plant_care_system/plant_care/wsgi.py
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_care.settings')

application = get_wsgi_application()
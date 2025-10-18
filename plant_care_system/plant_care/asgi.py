# plant_care_system/plant_care/asgi.py
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_care.settings')

application = get_asgi_application()
import os
from celery import Celery

# Définir la variable d'environnement par défaut pour la configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hospi.settings')

app = Celery('Hospi')

# Charger la configuration de Celery à partir des paramètres Django, en utilisant le préfixe 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrir automatiquement les tâches potentielles dans les applications Django
app.autodiscover_tasks()

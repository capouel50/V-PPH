import multiprocessing

bind = "0.0.0.0:8000"  # Adresse et port auxquels Gunicorn doit écouter
workers = multiprocessing.cpu_count() * 2 + 1  # Nombre de travailleurs Gunicorn
#worker_class = "gevent"  # Utiliser le worker "gevent" pour gérer WebSocket
timeout = 60  # Temps d'attente pour une requête WebSocket

errorlog = "./logs/error.log"
accesslog = "./logs/access.log"

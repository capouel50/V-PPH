# Pour le backend en developpement
# web: python manage.py runserver 0.0.0.0:$PORT

# Pour le backend Django avec Gunicorn
web: gunicorn Hospi.wsgi:application --bind 0.0.0.0:$PORT

# Pour le back-end avec websocket
# web: source envhop/bin/activate && uvicorn Hospi.asgi:application --host=0.0.0.0 --port=$PORT
# worker: celery -A Hospi worker --loglevel=info

# Pour le frontend Vue.js
# frontend: npm run build --prefix Hospi/pphfront

# serveur express pour node
# web: npm start

# web: nginx -p /app/<%= ENV['PPH'] %> -c config/nginx.conf.erb

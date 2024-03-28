# Pour le backend Django avec Gunicorn
web: gunicorn Hospi.wsgi --chdir Hospi --config gunicorn.conf.py

# Pour le back-end avec websocket
# web: source envhop/bin/activate && uvicorn Hospi.asgi:application --host=0.0.0.0 --port=$PORT
# worker: celery -A Hospi worker --loglevel=info

# Pour le frontend Vue.js
# frontend: npm run build --prefix Hospi/pphfront

# serveur express pour node
# web: npm start

# web: nginx -p /app/<%= ENV['PPH'] %> -c config/nginx.conf.erb

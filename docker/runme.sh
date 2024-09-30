python docker/generate_nginx_conf.py
cp nginx_config.conf /etc/nginx/conf.d/django_app.conf
python manage.py migrate
python manage.py create_admin
python manage.py init_demo_user
python manage.py add_default_phone_number
uvicorn api_core.asgi:application --port 8000 & nginx -g "daemon off;"

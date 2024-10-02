set -o errexit

pip install --upgrade pip
pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --email SUPERUSER_EMAIL  --password SUPERUSER_PASSWORD 

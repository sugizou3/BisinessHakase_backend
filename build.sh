set -o errexit

pip install -r requirements.txt
pip install -U pip

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --username qwertqwertyuiop --email qazwsx@edcrfv.com --noinput

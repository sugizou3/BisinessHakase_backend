FROM python:3.9

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# ENV SECRET_KEY="ne(p*w%g!r*ztt*b*(4*rps#)4o0wgi0%b2e5o5s@o90mbxf9a"
# ENV DEBUG="False"
# ENV SUPERUSER_EMAIL="super@super.com"
# ENV SUPERUSER_PASSWORD="super"

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install -r requirements.txt

# RUN python manage.py makemigrations
# RUN python manage.py migrate

# ENV PORT=8000

# EXPOSE $PORT

# CMD ["python","manage.py","runserver","0.0.0.0:8000"]
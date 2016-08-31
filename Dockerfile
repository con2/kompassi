FROM python:2.7
WORKDIR /usr/src/app
COPY requirements.txt requirements-production.txt /usr/src/app/
RUN groupadd -r kompassi && useradd -r -g kompassi kompassi && \
    pip install --no-cache-dir -r requirements.txt -r requirements-production.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py kompassi_i18n -ac && \
    env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q .
USER kompassi
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

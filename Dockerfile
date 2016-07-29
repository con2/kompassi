FROM python:2-onbuild
EXPOSE 8000
RUN pip install -r requirements-production.txt
RUN groupadd -r kompassi && useradd -r -g kompassi kompassi
RUN env DEBUG=1 python manage.py kompassi_i18n -ac
RUN env DEBUG=1 python manage.py collectstatic --noinput
USER kompassi
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

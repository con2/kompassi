FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt requirements-production.txt /usr/src/app/
RUN groupadd -g 998 -r kompassi && useradd -r -g kompassi -u 998 kompassi && \
    pip install -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt -r requirements-production.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    env DEBUG=1 python manage.py kompassi_i18n -ac && \
    python -m compileall -q . && \
    chmod 755 manage.py scripts/*.sh
USER kompassi
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

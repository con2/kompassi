FROM python:3.13 AS deps
WORKDIR /tmp
RUN mkdir /deps
ADD requirements.txt ./
RUN pip install -U pip setuptools wheel && \
    pip wheel -r requirements.txt --no-cache-dir --wheel-dir /deps && \
    rm -f /deps/setuptools-*.whl

FROM python:3.13-slim
WORKDIR /usr/src/app
RUN groupadd -g 998 -r kompassi && useradd -r -g kompassi -u 998 kompassi && apt-get update && apt-get -y install libpq5 libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 && rm -rf /var/lib/apt/lists
ADD requirements.txt ./
RUN --mount=type=bind,from=deps,source=/deps,target=/deps \
    pip install --no-cache-dir --no-index --find-links /deps /deps/*.whl
ADD . .
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    env DEBUG=1 python manage.py kompassi_i18n -ac && \
    python -m compileall -q . && \
    chmod 755 manage.py scripts/*.sh
USER kompassi

# mount tmpfs at /tmp to silence "FontConfig: No writable cache directories" warnings
ENV HOME=/tmp

ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

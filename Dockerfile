FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS deps
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /usr/src/app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev


FROM deps AS test
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project
COPY manage.py ./
COPY scripts /usr/src/app/scripts
COPY kompassi /usr/src/app/kompassi
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
ENV PATH="/usr/src/app/.venv/bin:$PATH"


FROM deps AS build
COPY manage.py ./
COPY scripts /usr/src/app/scripts
COPY kompassi /usr/src/app/kompassi
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev
ENV PATH="/usr/src/app/.venv/bin:$PATH"
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    env DEBUG=1 python manage.py kompassi_i18n -ac && \
    chmod 755 manage.py scripts/*.sh


FROM python:3.14-slim-bookworm AS runtime

RUN groupadd -g 998 -r kompassi && useradd -r -g kompassi -u 998 kompassi && apt-get update && apt-get -y install libpq5 libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 && rm -rf /var/lib/apt/lists
WORKDIR /usr/src/app
COPY --from=build --chown=root:root /usr/src/app/.venv /usr/src/app/.venv
COPY --from=build --chown=root:root /usr/src/app/manage.py /usr/src/app/manage.py
COPY --from=build --chown=root:root /usr/src/app/scripts /usr/src/app/scripts
COPY --from=build --chown=root:root /usr/src/app/kompassi /usr/src/app/kompassi
ENV PATH="/usr/src/app/.venv/bin:$PATH"

USER kompassi
# XDG_CACHE_HOME set to /tmp (mounted as emptyDir in Kubernetes) so fontconfig
# can write its cache there and not log "No writable cache directories" errors.
ENV XDG_CACHE_HOME=/tmp

ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

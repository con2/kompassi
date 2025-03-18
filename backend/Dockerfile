FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

RUN groupadd -g 998 -r kompassi && \
    useradd -r -g kompassi -u 998 kompassi && \
    apt-get update && \
    apt-get -y install \
        git \
        libpq5 \
        libpango-1.0-0 \
        libharfbuzz0b \
        libpangoft2-1.0-0 && \
    rm -rf /var/lib/apt/lists

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev && \
    env DEBUG=1 python manage.py collectstatic --noinput && \
    env DEBUG=1 python manage.py kompassi_i18n -ac && \
    python -m compileall -q . && \
    chmod 755 manage.py scripts/*.sh

USER kompassi

# mount tmpfs at /tmp to silence "FontConfig: No writable cache directories" warnings
ENV HOME=/tmp

ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

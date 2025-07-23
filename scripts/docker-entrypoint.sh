#!/bin/bash

set -ue

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export POSTGRES_USERNAME="${POSTGRES_USERNAME:-kompassi}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-secret}"
export POSTGRES_HOSTNAME="${POSTGRES_HOSTNAME:-postgres}"
export POSTGRES_DATABASE="${POSTGRES_DATABASE:-kompassi}"
export POSTGRES_SSLMODE="${POSTGRES_SSLMODE:-allow}"
export POSTGRES_PORT="${POSTGRES_PORT:-5432}"

# Allow setting either BROKER_URL/CACHE_URL (takes precedence) or REDIS_HOSTNAME
REDIS_HOSTNAME="${REDIS_HOSTNAME:-redis}"
REDIS_BROKER_DATABASE="${REDIS_BROKER_DATABASE:-1}"
REDIS_CACHE_DATABASE="${REDIS_CACHE_DATABASE:-2}"
export BROKER_URL="${BROKER_URL:-redis://$REDIS_HOSTNAME/$REDIS_BROKER_DATABASE}"
export CACHE_URL="${CACHE_URL:-rediscache://$REDIS_HOSTNAME/$REDIS_CACHE_DATABASE}"

# Wait for postgres to be up before continuing
"$DIR/wait-for-it.sh" -s -t 120 "$POSTGRES_HOSTNAME:$POSTGRES_PORT"

# For development only, generate OIDC RSA key if it doesn't exist
if [ -n "${KOMPASSI_GENERATE_OIDC_RSA_PRIVATE_KEY_PATH:-}" ]; then
  if [ ! -f "$KOMPASSI_GENERATE_OIDC_RSA_PRIVATE_KEY_PATH" ]; then
    echo "Generating new RSA key for OIDC"
    openssl genrsa -out "$KOMPASSI_GENERATE_OIDC_RSA_PRIVATE_KEY_PATH" 2048
  fi

  OIDC_RSA_PRIVATE_KEY=$(cat "$KOMPASSI_GENERATE_OIDC_RSA_PRIVATE_KEY_PATH")
  export OIDC_RSA_PRIVATE_KEY
fi

exec "$@"

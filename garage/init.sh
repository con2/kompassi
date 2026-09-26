#!/bin/sh
# Bootstraps the development Garage node: assigns the single node into the
# cluster layout, imports the fixed development key and creates the bucket.
# Safe to run repeatedly; steps that were already done are skipped.
set -eu

until /garage status >/dev/null 2>&1; do
  echo "garage-init: waiting for garage to start"
  sleep 1
done

if /garage status | grep -q "NO ROLE ASSIGNED"; then
  node_id=$(/garage node id -q | cut -d@ -f1)
  /garage layout assign -z dev -c 1G "$node_id"
  /garage layout apply --version 1
fi

if ! /garage key info "$ACCESS_KEY_ID" >/dev/null 2>&1; then
  /garage key import --yes -n "$ACCESS_KEY_ID" "$ACCESS_KEY_ID" "$SECRET_ACCESS_KEY"
fi

if ! /garage bucket info "$BUCKET_NAME" >/dev/null 2>&1; then
  /garage bucket create "$BUCKET_NAME"
fi

/garage bucket allow --read --write --owner "$BUCKET_NAME" --key "$ACCESS_KEY_ID"
echo "garage-init: done"

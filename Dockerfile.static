ARG KOMPASSI_IMAGE=tracon/kompassi
FROM $KOMPASSI_IMAGE

FROM nginx:1-alpine
COPY --from=0 /usr/src/app/static /usr/share/nginx/html/static


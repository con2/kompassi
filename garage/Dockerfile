# The upstream image is built from scratch and has no shell, so init.sh needs
# the garage binary copied into an image that has one.
FROM dxflrs/garage:v2.4.1 AS garage
FROM alpine:3.22
COPY --from=garage /garage /garage
COPY init.sh /init.sh
ENTRYPOINT ["/bin/sh", "/init.sh"]

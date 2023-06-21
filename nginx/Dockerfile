FROM nginxinc/nginx-unprivileged:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/
COPY tempssl.key tempssl.crt /etc/nginx/certs/
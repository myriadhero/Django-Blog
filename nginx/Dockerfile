FROM nginxinc/nginx-unprivileged:alpine

RUN sed -i '/^\s*pid/s|/run/nginx.pid|/tmp/nginx.pid|' /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/
COPY nginxcert.key nginxcert.crt /etc/nginx/certs/
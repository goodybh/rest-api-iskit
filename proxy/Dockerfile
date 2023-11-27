FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="Goody"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /app/staticfiles && \
    chown -R django-user:django-user /app/staticfiles && \
    chmod -R 755 /app/staticfiles && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /app/staticfiles

USER nginx

CMD ["/run.sh"]

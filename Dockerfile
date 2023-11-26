FROM python:3.12
LABEL maintainer="Goody"
ENV PYTHONUNBUFFERED 1

# Install Microsoft ODBC Driver for SQL Server, Linux Headers, and other dependencies
RUN apt-get update && apt-get install -y gnupg2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev && \
    apt-get install -y linux-headers-amd64

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp

# Set the appropriate permissions
RUN chmod -R +x /scripts

# Create a non-root user
RUN adduser --disabled-password --no-create-home django-user

# Create staticfiles directory and set permissions
RUN mkdir -p /app/static && \
    chown -R django-user:django-user /app/static && \
    chmod -R 755 /app/static


ENV PATH="/scripts:/py/bin:$PATH"

USER django-user
CMD ["run.sh"]

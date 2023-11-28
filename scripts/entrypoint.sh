#!/bin/sh

# Check if /vol/web exists and set permissions
if [ -d "/app/staticfiles" ]; then
    chown -R django-user:django-user /app/staticfiles
fi

# Execute the command passed to docker run (e.g., starting Django)
exec "$@"

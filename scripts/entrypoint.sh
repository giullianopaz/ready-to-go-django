#!/usr/bin/env bash
set -e

# Wait for PostgreSQL
if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
    until python -c "
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(('${POSTGRES_HOST}', int('${POSTGRES_PORT:-5432}')))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
" 2>/dev/null; do
        sleep 1
    done
    echo "PostgreSQL is available!"
fi

# Run automatic database initialization if requested (default in dev)
if [ "$AUTO_INIT" = "true" ] || [ "$1" = "python" ] && [ "$2" = "manage.py" ] && [ "$3" = "runserver" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput

    echo "Ensuring cache table exists..."
    python manage.py createcachetable 2>/dev/null || true

    echo "Running seed command..."
    python manage.py seed || true
fi

exec "$@"

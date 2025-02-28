#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate && \
python manage.py collectstatic --no-input && \
gunicorn --bind 0.0.0.0:$PORT \
	 --workers 1 \
	 --timeout 60 \
	 --log-level info \
	 --log-file=- \
	 config.wsgi:application

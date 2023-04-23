#!/usr/bin/env bash

# Workaround to get rid of errors when you are trying to run django tests
mysql -u root --password="$MYSQL_ROOT_PASSWORD"  << EOF
USE ${MYSQL_DATABASE};
GRANT ALL PRIVILEGES ON  test_${MYSQL_DATABASE}.* TO '${MYSQL_USER}';
EOF

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd onestop; python manage.py createsuperuser --no-input)
fi
(cd onestop; gunicorn onestop.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
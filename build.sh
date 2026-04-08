set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [ "$RENDER" = "true" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', config('DJANGO_SUPERUSER_PASSWORD', default='changeme'))
    print('Superuser created.')
else:
    print('Superuser already exists, skipping.')
"
fi
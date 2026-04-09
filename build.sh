set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate


if [ "$RENDER" = "true" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model
from decouple import config
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', config('DJANGO_SUPERUSER_PASSWORD', default='changeme'))
    print('Superuser created.')
else:
    u = User.objects.get(username='admin')
    u.set_password(config('DJANGO_SUPERUSER_PASSWORD', default='changeme'))
    u.save()
    print('Superuser password updated.')
"
fi
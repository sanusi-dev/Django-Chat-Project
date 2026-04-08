set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [ "$RENDER" = "true" ]; then
    python manage.py createsuperuser --no-input --username admin --email admin@example.com
fi 
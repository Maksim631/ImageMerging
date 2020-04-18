release: python manage.py makemigrations && python manage.py migrate
web: gunicorn image_merging_bot.wsgi --log-file -
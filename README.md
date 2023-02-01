# pydiscord
Yet another Discord ripoff in Python for fooling around with Django.


How to run it:
1. python -m pip install -r requirements.txt
2. python utils/super_super_env.py --name your_name --email your@email.com --password your_pwd if no args given then default ones will be set from su.yaml
3. python manage.py migrate
4. python manage.py runserver localhost:8000

TODO:
- README
# <img height="64px" src="./static/images/logo.svg" alt="logo img"> PyDiscord
Yet another Discord ripoff in Python for fooling around with Django.

## What can you do with it?
- Get a sneakpeak how can you create something similar in Django
- Create some conversations
- Talk with yourself using different accounts
- Pretend to be a site admin
- Curl some request to basic API
- Clone repo and add some more functionalities for yourself

## How to run it?

```
1. python -m pip install -r requirements.txt
2. python utils/super_super_env.py --name your_name --email your@email.com --password your_pwd
3. python manage.py migrate
4. python manage.py runserver localhost:8000
```

If you just want to run it with default config for superuser replace command in `2.` with `python utils/super_super_env.py`

## How does it look with some users?
### Main
<img width="1024" src="./showcase/main.png" alt="main img">

### Room
<img width="1024" src="./showcase/room.png" alt="room img">

### Profile
<img width="1024" src="./showcase/profile.png" alt="profile img">

### API
<img width="1024" src="./showcase/api.png" alt="api img">

CSS and style inspired by Dennis Ivy one
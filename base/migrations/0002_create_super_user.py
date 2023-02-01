import os

from django.db import migrations
from dotenv import load_dotenv, find_dotenv

from base.models import User

load_dotenv(dotenv_path=find_dotenv())


def generate_superuser(apps, editor):
    superuser_name = os.environ.get('DJANGO_SU_NAME')
    superuser_email = os.environ.get('DJANGO_SU_EMAIL')
    superuser_password = os.environ.get('DJANGO_SU_PASSWORD')
    print(superuser_name, superuser_email, superuser_password)

    superuser = User.objects.create_superuser(
        username=superuser_name,
        email=superuser_email,
        password=superuser_password,
    )

    superuser.save()


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]

# Generated by Django 2.2.7 on 2019-11-27 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_projeto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projeto',
            name='ult_alt',
        ),
        migrations.AlterField(
            model_name='projeto',
            name='lider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
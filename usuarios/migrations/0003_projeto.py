# Generated by Django 2.2.7 on 2019-11-27 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20191126_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=100)),
                ('descricao', models.TextField(max_length=400)),
                ('lider', models.TextField(max_length=50)),
                ('ult_alt', models.TextField(max_length=50)),
            ],
        ),
    ]
# Generated by Django 2.2.7 on 2019-11-27 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_auto_20191127_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('prioridade', models.CharField(max_length=15, null=True)),
                ('data_limite', models.DateField(null=True)),
                ('concluido', models.BooleanField(default=False)),
                ('resp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Membro')),
            ],
        ),
    ]

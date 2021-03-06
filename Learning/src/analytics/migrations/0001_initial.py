# Generated by Django 2.0.6 on 2018-06-27 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shortener', '0003_auto_20180627_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('shortner_url', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shortener.ShortenerURL')),
            ],
        ),
    ]

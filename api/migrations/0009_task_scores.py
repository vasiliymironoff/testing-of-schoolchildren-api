# Generated by Django 3.2.7 on 2021-09-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210909_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='scores',
            field=models.SmallIntegerField(default=1, verbose_name='Максимальное количество баллов'),
            preserve_default=False,
        ),
    ]
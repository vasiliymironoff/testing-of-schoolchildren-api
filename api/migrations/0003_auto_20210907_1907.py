# Generated by Django 3.2.7 on 2021-09-07 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210907_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='Учитель'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user/', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='classroom',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Класс'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='letter',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Буква класса'),
        ),
    ]

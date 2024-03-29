# Generated by Django 3.2.7 on 2021-09-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210909_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(verbose_name='Учитель'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='classroom',
            field=models.SmallIntegerField(choices=[(1, '1 класс'), (2, '2 класс'), (3, '3 класс'), (4, '4 класс'), (5, '5 класс'), (6, '6 класс'), (7, '7 класс'), (8, '8 класс'), (9, '9 класс'), (10, '10 класс'), (11, '11 класс')], verbose_name='Класс'),
        ),
    ]

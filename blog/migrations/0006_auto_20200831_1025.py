# Generated by Django 3.1 on 2020-08-31 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200830_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.ManyToManyField(blank=True, to='blog.Type'),
        ),
    ]

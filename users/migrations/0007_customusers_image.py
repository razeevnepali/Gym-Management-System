# Generated by Django 2.1.5 on 2019-03-08 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customusers_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]

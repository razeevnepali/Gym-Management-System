# Generated by Django 2.1.5 on 2019-02-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190209_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusers',
            name='package',
            field=models.CharField(choices=[('1', '1 Month'), ('3', '3 Months'), ('6', '6 Months'), ('12', '12 Months')], default=1, max_length=20),
        ),
    ]

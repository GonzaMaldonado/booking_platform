# Generated by Django 4.2.2 on 2023-06-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_birthday_remove_profile_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('U', 'user'), ('C', 'company')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

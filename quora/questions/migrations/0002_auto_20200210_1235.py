# Generated by Django 3.0.3 on 2020-02-10 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='questions',
            new_name='question',
        ),
    ]

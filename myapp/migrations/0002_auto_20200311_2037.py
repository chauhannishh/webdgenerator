# Generated by Django 3.0.1 on 2020-03-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syllabus',
            name='id',
        ),
        migrations.AddField(
            model_name='syllabus',
            name='syllabus_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
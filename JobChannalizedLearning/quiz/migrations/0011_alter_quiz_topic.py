# Generated by Django 4.2.3 on 2023-07-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_quiz_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='topic',
            field=models.CharField(max_length=120),
        ),
    ]

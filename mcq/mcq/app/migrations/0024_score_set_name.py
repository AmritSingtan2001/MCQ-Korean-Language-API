# Generated by Django 4.2.7 on 2024-02-25 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_purchases_sets'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='set_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_set_id', to='app.questionsets'),
        ),
    ]

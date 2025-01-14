# Generated by Django 5.1.3 on 2025-01-14 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='repeat_interval',
            field=models.CharField(choices=[('none', 'Neopakovat'), ('daily', 'Denně'), ('weekly', 'Týdně'), ('monthly', 'Měsíčně')], default='none', max_length=20, verbose_name='Interval opakování'),
        ),
        migrations.CreateModel(
            name='SubtaskTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Název podúkolu')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='tasks.template', verbose_name='Šablona úkolu')),
            ],
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-07 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_alter_todo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='user',
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Incomplete', 'Incomplete')], max_length=20)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_task', to='leads.agent')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_task', to='leads.lead')),
            ],
        ),
        migrations.DeleteModel(
            name='Reminder',
        ),
        migrations.DeleteModel(
            name='ToDo',
        ),
    ]

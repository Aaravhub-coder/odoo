# core/migrations/0002_seed_groups.py
from django.db import migrations

def create_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    roles = ['Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    for role in roles:
        Group.objects.get_or_create(name=role)

def remove_roles(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    roles = ['Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    Group.objects.filter(name__in=roles).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),  # Dynamic dependency: ensure it points to your first migration file
    ]

    operations = [
        migrations.RunPython(create_roles, reverse_code=remove_roles),
    ]
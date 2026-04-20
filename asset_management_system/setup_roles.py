import os
import django

# Replace 'asset_management' with your actual folder name containing settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asset_management.settings')
django.setup()

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

def setup_system():
    # 1. Create Groups (Roles) in lowercase
    roles = ['admin', 'employee', 'technician']
    for role in roles:
        Group.objects.get_or_create(name=role)
    print("Roles synchronized: admin, employee, technician")

    # 2. Get the User model
    User = get_user_model()
    
    # Define your actors
    users_to_create = [
        {'un': 'admin', 'email': 'admin@test.com', 'pw': 'admin123', 'role': 'admin', 'is_staff': True, 'is_super': True},
        {'un': 'employee', 'email': 'emp@test.com', 'pw': 'emp123', 'role': 'employee', 'is_staff': False, 'is_super': False},
        {'un': 'technician', 'email': 'tech@test.com', 'pw': 'tech123', 'role': 'technician', 'is_staff': True, 'is_super': False},
    ]

    for u in users_to_create:
        if not User.objects.filter(username=u['un']).exists():
            if u['is_super']:
                user = User.objects.create_superuser(username=u['un'], email=u['email'], password=u['pw'])
            else:
                user = User.objects.create_user(username=u['un'], email=u['email'], password=u['pw'], is_staff=u['is_staff'])
            
            # Assign user to their specific group
            group = Group.objects.get(name=u['role'])
            user.groups.add(group)
            print(f"User created: {u['un']} assigned to role: {u['role']}")
        else:
            print(f"User {u['un']} already exists.")

if __name__ == "__main__":
    setup_system()
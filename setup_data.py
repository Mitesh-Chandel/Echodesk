#!/usr/bin/env python
"""
Setup script to initialize EchoDesk with sample data and admin user.
Run: python manage.py shell < setup_data.py
"""

from complaints.models import Category
from django.contrib.auth.models import User
from users.models import UserProfile

# Create categories
categories_data = [
    {'name': 'Electricity', 'slug': 'electricity', 'description': 'Issues related to electricity supply and outages'},
    {'name': 'Water', 'slug': 'water', 'description': 'Water supply and quality issues'},
    {'name': 'Road', 'slug': 'road', 'description': 'Road damage, potholes, and maintenance'},
    {'name': 'Garbage', 'slug': 'garbage', 'description': 'Garbage collection and disposal'},
    {'name': 'Internet', 'slug': 'internet', 'description': 'Internet connectivity issues'},
    {'name': 'College', 'slug': 'college', 'description': 'College related complaints'},
    {'name': 'Hostel', 'slug': 'hostel', 'description': 'Hostel facilities complaints'},
    {'name': 'Transport', 'slug': 'transport', 'description': 'Public transport issues'},
    {'name': 'Other', 'slug': 'other', 'description': 'Other complaints'},
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'slug': cat_data['slug'],
            'description': cat_data['description']
        }
    )
    if created:
        print(f"  ✓ Created: {category.name}")
    else:
        print(f"  - Already exists: {category.name}")

print("\nCategories setup complete!")
print("\nTo create an admin user, run:")
print("  python manage.py createsuperuser")
print("\nThen access admin at: http://localhost:8000/django-admin/")

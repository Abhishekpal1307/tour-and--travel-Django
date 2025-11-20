#!/usr/bin/env python3
"""
Idempotent seed script to create sample Hotels for listed cities.
Run: python3 scripts/seed_hotels.py
"""
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tourAndTravel.settings')
import django
django.setup()

from travelapp.models import City, Hotels

SAMPLES = {
    'UTTAR PRADESH': [
        {
            'hotel_name': 'Agra Grand Hotel',
            'hotel_address': 'Taj Ganj, Agra',
            'hotel_price': 3500,
            'hotel_rating': 4,
            'amenities': 'Free WiFi, Breakfast, Pool',
            'distfromap': 13,
            'rooms': 50,
            'image1': None,
        },
        {
            'hotel_name': 'Varanasi Riverside Inn',
            'hotel_address': 'Dashashwamedh Ghat, Varanasi',
            'hotel_price': 2500,
            'hotel_rating': 3,
            'amenities': 'River view, Breakfast',
            'distfromap': 30,
            'rooms': 30,
            'image1': None,
        }
    ],
    'BIHAR': [
        {
            'hotel_name': 'Bodh Heritage Hotel',
            'hotel_address': 'Near Mahabodhi Temple, Bodh Gaya',
            'hotel_price': 2200,
            'hotel_rating': 3,
            'amenities': 'Garden, Breakfast',
            'distfromap': 12,
            'rooms': 25,
            'image1': None,
        },
        {
            'hotel_name': 'Nalanda Stay',
            'hotel_address': 'Nalanda Road, Nalanda',
            'hotel_price': 1800,
            'hotel_rating': 3,
            'amenities': 'Parking, Guide Desk',
            'distfromap': 40,
            'rooms': 20,
            'image1': None,
        }
    ],
    'PUNJAB': [
        {
            'hotel_name': 'Amritsar Heritage Hotel',
            'hotel_address': 'Near Golden Temple, Amritsar',
            'hotel_price': 3000,
            'hotel_rating': 4,
            'amenities': 'Pool, Free WiFi, Breakfast',
            'distfromap': 10,
            'rooms': 60,
            'image1': None,
        },
        {
            'hotel_name': 'Ludhiana Comfort Inn',
            'hotel_address': 'City Center, Ludhiana',
            'hotel_price': 2000,
            'hotel_rating': 3,
            'amenities': 'Breakfast, Parking',
            'distfromap': 25,
            'rooms': 35,
            'image1': None,
        }
    ],
    'HIMACHAL PRADESH': [
        {
            'hotel_name': 'Shimla Pine Resort',
            'hotel_address': 'Mall Road, Shimla',
            'hotel_price': 4000,
            'hotel_rating': 4,
            'amenities': 'Mountain view, Fireplace',
            'distfromap': 18,
            'rooms': 40,
            'image1': None,
        },
        {
            'hotel_name': 'Manali Valley Lodge',
            'hotel_address': 'Old Manali',
            'hotel_price': 3200,
            'hotel_rating': 4,
            'amenities': 'Garden, Breakfast',
            'distfromap': 50,
            'rooms': 30,
            'image1': None,
        }
    ],
    'RAJASTHAN': [
        {
            'hotel_name': 'Jaipur Royal Palace Hotel',
            'hotel_address': 'Pink City, Jaipur',
            'hotel_price': 4500,
            'hotel_rating': 5,
            'amenities': 'Heritage, Pool, Breakfast',
            'distfromap': 15,
            'rooms': 45,
            'image1': None,
        },
        {
            'hotel_name': 'Jaisalmer Desert Inn',
            'hotel_address': 'Near Jaisalmer Fort',
            'hotel_price': 2800,
            'hotel_rating': 4,
            'amenities': 'Desert tours, Breakfast',
            'distfromap': 8,
            'rooms': 28,
            'image1': None,
        }
    ],
}

added = 0
for city_name, hotels in SAMPLES.items():
    try:
        city = City.objects.get(city__iexact=city_name)
    except City.DoesNotExist:
        print(f"City not found, skipping hotels for: {city_name}")
        continue

    for h in hotels:
        # Use case-insensitive exact match for hotel_name to avoid duplicates
        exists = Hotels.objects.filter(hotel_name__iexact=h['hotel_name'], city=city).exists()
        if exists:
            print(f"Already exists: {h['hotel_name']} ({city_name})")
            continue
        Hotels.objects.create(
            city=city,
            hotel_name=h['hotel_name'],
            hotel_address=h['hotel_address'],
            hotel_price=h['hotel_price'],
            hotel_rating=h['hotel_rating'],
            amenities=h['amenities'],
            distfromap=h['distfromap'],
            rooms=h['rooms'],
            image1=h['image1']
        )
        print(f"Added hotel: {h['hotel_name']} ({city_name})")
        added += 1

print(f"\nDone — total hotels added: {added}")

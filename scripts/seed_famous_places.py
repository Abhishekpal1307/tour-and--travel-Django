#!/usr/bin/env python3
"""
Seed script to add Famous place entries to the database.
Run from project root:

    python3 scripts/seed_famous_places.py

The script will only add entries that don't already exist (by place_name + city).
"""
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourAndTravel.settings')
django.setup()

from travelapp.models import City, Famous

# Define places to add keyed by city name (must match City.city values)
PLACES = {
    'DELHI': [
        ("Red Fort","Historic fort complex and UNESCO site."),
        ("Qutub Minar","Tall minaret and archaeological complex."),
        ("India Gate","War memorial in the heart of Delhi."),
    ],
    'MUMBAI': [
        ("Gateway of India","Iconic arch on the waterfront."),
        ("Marine Drive","Coastal promenade with skyline views."),
        ("Elephanta Caves","Rock-cut temples on Elephanta Island."),
    ],
    'DARJEELING': [
        ("Tiger Hill","Sunrise views over Kanchenjunga."),
        ("Batasia Loop","Scenic railway loop and memorial garden."),
    ],
    'LONDON': [
        ("Tower of London","Historic castle on the Thames."),
        ("British Museum","Extensive collection of human history."),
    ],
    'NEW YORK': [
        ("Statue of Liberty","Famous US national monument."),
        ("Central Park","Large urban park in Manhattan."),
    ],
    'ZURICH': [
        ("Old Town","Historic center with medieval buildings."),
    ],
    'COCHIN': [
        ("Fort Kochi","Historic neighborhood with colonial buildings."),
    ],
    'SRINAGAR': [
        ("Dal Lake","Famous lake with houseboats and shikaras."),
    ],
}

added = 0
for city_name, places in PLACES.items():
    try:
        city = City.objects.get(city__iexact=city_name)
    except City.DoesNotExist:
        print(f"City not found in DB: {city_name} — skipping")
        continue

    for place_name, desc in places:
        # avoid duplicates by place_name + city
        exists = Famous.objects.filter(city=city, place_name__iexact=place_name).exists()
        if exists:
            print(f"Already exists: {place_name} ({city_name})")
            continue
        f = Famous(city=city, place_name=place_name, desc=desc, image=None)
        f.save()
        print(f"Added: {place_name} ({city_name})")
        added += 1

print(f"\nDone — total new places added: {added}")

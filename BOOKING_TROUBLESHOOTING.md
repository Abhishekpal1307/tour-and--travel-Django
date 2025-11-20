# Booking System Troubleshooting Guide

## Issue Fixed: Form Submissions and Bookings Not Working

### Problem Description
When users filled out search forms (hotels, flights, packages), the form would submit but nothing would appear - staying on the same page. Similarly, booking links might not trigger properly.

### Root Causes and Fixes Applied

#### 1. **Date Field Parsing Issue (FIXED)**
**Problem:** DateField forms didn't specify input formats, so dates in YYYY-MM-DD format were rejected.

**Fix Applied:**
```python
# In travelapp/forms.py - Added input_formats to DateField
date = forms.DateField(
    initial=datetime.date.today,
    label='Date',
    widget=forms.TextInput(attrs={'class': 'fd-form form-control', 'placeholder': 'YYYY-MM-DD'}),
    input_formats=['%Y-%m-%d'],  # ← ADDED THIS
    required=False
)
```

**Files Updated:**
- `HotelForm.date` (line 48)
- `FlightForm.date` (line 39)

#### 2. **ALLOWED_HOSTS Configuration (FIXED)**
**Problem:** Django rejected requests with invalid host headers in testing/production.

**Fix Applied:**
```python
# In tourAndTravel/settings.py
ALLOWED_HOSTS = ['*']  # Changed from []
```

### Complete Booking Flow (How It Works)

1. **User navigates to search page**
   - `/flights/`, `/hotels/`, or `/package/`
   - Form displays with city/source/destination and date fields

2. **User fills form and clicks SEARCH**
   - Form validates (date must be YYYY-MM-DD format)
   - View filters available flights/hotels by location
   - Calculates remaining availability (seats/rooms)
   - Displays filtered results on same page

3. **User clicks on a flight/hotel BOOK button**
   - Navigates to confirmation page: `/bookflight/<flight_num>/<date>` or `/bookhotel/<hotel_name>/<date>`
   - Shows availability and total price
   - User enters quantity (seats/rooms)
   - Clicks SEARCH button on confirmation page

4. **Confirmation page shows availability**
   - If available: Shows BOOK button as clickable link
   - If unavailable: Shows "BOOKED" text (disabled)
   - User clicks the BOOK link to proceed

5. **Booking is created and user redirected**
   - `FlightSubmit()` / `HotelSubmit()` / `PackageSubmit()` view creates booking record
   - Saves to database with user ID, item details, date, and quantity
   - Redirects to dashboard (`/accounts/profile/`)
   - Booking appears in user's dashboard table

### Troubleshooting Steps

**If search still returns empty results:**
1. Verify data exists in admin: `http://127.0.0.1:8000/admin/`
   - Check `City` entries
   - Check `Hotels`/`Flights` entries with matching cities
2. Test form directly in Django shell:
   ```bash
   python manage.py shell
   >>> from travelapp.forms import HotelForm
   >>> form = HotelForm(data={'city': 'delhi', 'date': '2025-11-15'})
   >>> form.is_valid()
   True
   ```

**If search works but booking doesn't appear in dashboard:**
1. Ensure you're logged in (check top-right corner)
2. Clear browser cache and cookies
3. Verify booking was saved:
   ```bash
   python manage.py shell
   >>> from django.contrib.auth.models import User
   >>> from travelapp.models import BookHotel
   >>> user = User.objects.get(username='your_username')
   >>> BookHotel.objects.filter(username_id=user)
   ```

**If BOOK button doesn't work on confirmation page:**
1. Check that you're logged in (required by `@login_required` decorator)
2. Verify availability shows "available" (not "unavailable")
3. Check browser console for JavaScript errors
4. Manually test URL: `/userhotel/The%20Lalit%20New%20Delhi/2025-11-15/2` (replace spaces with %20)

### Database Structure

**Booking Records:**
- `BookFlight` - flight bookings (flight number, date, seats, user)
- `BookHotel` - hotel bookings (hotel name, date, rooms, user)
- `BookPackage` - combined bookings (flight + hotel, date, quantities, user)

**Availability Calculation Logic:**
The system counts existing bookings and subtracts from total capacity:
```python
# Count existing bookings for this flight/date from BOTH BookFlight and BookPackage
existing_seats = sum(booking.seat for booking in BookFlight.objects.filter(...))
existing_seats += sum(booking.seat for booking in BookPackage.objects.filter(...))
remaining_seats = total_seats - existing_seats
```

### URL Pattern Reference

| Action | URL | Method | Requires Login |
|--------|-----|--------|---|
| Search flights | `/flights/` | POST | No |
| Search hotels | `/hotels/` | POST | No |
| Search packages | `/package/` | POST | No |
| Book flight confirmation | `/bookflight/<flight_num>/<date>` | GET/POST | Yes |
| Complete flight booking | `/userflight/<flight_num>/<date>/<seats>` | GET | Yes |
| Book hotel confirmation | `/bookhotel/<hotel>/<date>` | GET/POST | Yes |
| Complete hotel booking | `/userhotel/<hotel>/<date>/<rooms>` | GET | Yes |
| Book package confirmation | `/bookpackage/<source>/<city>/<date>` | GET/POST | Yes |
| Complete package booking | `/userpackage/<flight>/<hotel>/<date>/<rooms>/<seats>` | GET | Yes |
| View dashboard | `/accounts/profile/` | GET | Yes |

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Date format error | Use YYYY-MM-DD format (e.g., 2025-11-15) |
| "BOOKED" shows instead of BOOK button | No availability - try different date or item |
| Booking doesn't appear after clicking BOOK | Ensure logged in; refresh dashboard page |
| Hotel names with spaces in URLs | Django auto-encodes as %20 (e.g., "The Lalit New Delhi" → "The%20Lalit%20New%20Delhi") |
| Form shows errors but looks valid | Check if required fields are empty despite placeholder text |

### Testing Bookings Manually

```bash
# Start Django shell
python manage.py shell

# Create a test user
from django.contrib.auth.models import User
from travelapp.models import BookHotel, Hotels

user = User.objects.create_user(username='testuser', password='test123')

# Search for hotels
hotels = Hotels.objects.filter(city__city__contains='DELHI')
print(hotels)

# Create a booking
booking = BookHotel(
    username_id=user,
    hotel_name=hotels[0].hotel_name,
    date='2025-11-15',
    room=2
)
booking.save()

# Verify it was created
BookHotel.objects.filter(username_id=user)
```

---
**Last Updated:** November 13, 2025  
**Fixed By:** AI Code Assistant  
**Status:** All booking functionality tested and working ✓

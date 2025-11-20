# Tour & Travel Django App - System Architecture

## High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                                                                  │
│  Hotels (/hotels/) │ Flights (/flights/) │ Packages (/package/)│
└────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Search Forms       │
                    │  (City, Date, Qty)  │
                    └─────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Form Validation    │
                    │  Date: YYYY-MM-DD   │
                    └─────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Database Query     │
                    │  Filter by Location │
                    └─────────────────────┘
                              ↓
        ┌──────────────────────────────────────────────┐
        │     Results Page with Items                 │
        │  (Hotels/Flights with Availability)         │
        └──────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Confirmation Page  │
                    │  (Show Price, Avail)│
                    └─────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Complete Booking   │
                    │  Save to Database   │
                    └─────────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Dashboard Display  │
                    │  Show All Bookings  │
                    └─────────────────────┘
```

## Database Schema

```
┌──────────────────────────────────────────────────────────────┐
│                      REFERENCE TABLES                         │
├──────────────────────────────────────────────────────────────┤
│  City                                                          │
│  ├─ city (CharField)                                         │
│  ├─ bestlink (CharField)                                     │
│  └─ weekgetlinks (CharField)                                 │
│                                                               │
│  Hotels  ◄──────── FK ────────┐                              │
│  ├─ id (AutoField)            │                              │
│  ├─ city (FK → City)           │                              │
│  ├─ hotel_name (CharField)     │                              │
│  ├─ hotel_price (IntegerField) │                              │
│  ├─ rooms (IntegerField)       │                              │
│  └─ image1 (ImageField)        │                              │
│                                │                              │
│  Flights  ◄──────── FK ────────┤                              │
│  ├─ id (AutoField)             │                              │
│  ├─ city (FK → City) ──────────┘                              │
│  ├─ flight_num (CharField)                                    │
│  ├─ eprice (IntegerField)                                     │
│  └─ seats (IntegerField)                                      │
│                                                               │
│  Famous  ◄──────── FK ────────┐                               │
│  ├─ city (FK → City) ──────────┘                              │
│  ├─ place_name (CharField)                                    │
│  └─ image (ImageField)                                        │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      BOOKING TABLES                           │
├──────────────────────────────────────────────────────────────┤
│  BookFlight                                                    │
│  ├─ id (AutoField)                                            │
│  ├─ username_id (FK → User) ──────────┐                       │
│  ├─ flight (CharField) ────────────────┼─ Stores actual       │
│  ├─ date (CharField) ──────────────────┼─ values, NOT FK      │
│  └─ seat (IntegerField)                │                      │
│                                        │                      │
│  BookHotel                             │                      │
│  ├─ id (AutoField)                     │                      │
│  ├─ username_id (FK → User) ──────────┤                       │
│  ├─ hotel_name (CharField) ────────────┼─ to Flights/Hotels  │
│  ├─ date (CharField) ──────────────────┼─ models (allows     │
│  └─ room (IntegerField)                │  deletion)          │
│                                        │                      │
│  BookPackage                           │                      │
│  ├─ id (AutoField)                     │                      │
│  ├─ username_id (FK → User) ──────────┤                       │
│  ├─ flight (CharField) ──────────────┬─┘                      │
│  ├─ hotel_name (CharField) ──────────┤                        │
│  ├─ date (CharField)                  │ Combined booking     │
│  ├─ seat (IntegerField)               │ of flight + hotel    │
│  └─ room (IntegerField)               │                      │
└──────────────────────────────────────────────────────────────┘
```

## Availability Calculation Algorithm

```python
# For each flight/hotel on a specific date:

total_capacity = Flight.seats  # or Hotel.rooms

# Count existing regular bookings
regular_bookings = sum(
    booking.seat  # or room
    for booking in BookFlight.objects.filter(
        flight=flight_num,
        date=target_date
    )
)

# Count existing package bookings
# (packages consume seats/rooms from the same pool)
package_bookings = sum(
    booking.seat  # or room
    for booking in BookPackage.objects.filter(
        flight=flight_num,  # or hotel_name
        date=target_date
    )
)

# Calculate remaining capacity
remaining = total_capacity - regular_bookings - package_bookings

# Determine availability status
if remaining > requested_quantity:
    status = "available"  # ✓ User can book
else:
    status = "unavailable"  # ✗ Show "BOOKED" button
```

## Form Validation Flow

```
User Input
├─ city/source/destination (CharField)
│  └─ Converted to .upper() for case-insensitive search
│
└─ date (DateField)
   ├─ Expected format: YYYY-MM-DD
   ├─ Widget shows: placeholder="YYYY-MM-DD"
   ├─ Validator: input_formats=['%Y-%m-%d']  ← CRITICAL
   └─ Parsed to: datetime.date object
      (used in database queries as string '2025-11-15')
```

## URL Routing Structure

```
/
├─ Empty (IndexView) - home page
├─ accounts/login/ - Django auth
├─ register/ - Sign up
├─ flights/ - Search flights
├─ hotels/ - Search hotels  
├─ package/ - Search packages
├─ places/ - View famous places
│
├─ bookflight/<flight_num>/<date> - Confirmation page
│  └─ POST back to same URL to enter quantity
│
├─ userflight/<flight_num>/<date>/<seats> - Complete booking
│  └─ @login_required → Create BookFlight → Redirect to /accounts/profile/
│
├─ bookhotel/<hotel>/<date> - Confirmation page
│  └─ POST back to same URL to enter quantity
│
├─ userhotel/<hotel>/<date>/<rooms> - Complete booking
│  └─ @login_required → Create BookHotel → Redirect to /accounts/profile/
│
├─ bookpackage/<source>/<city>/<date> - Select flight & hotel
│  └─ POST back to get confirmation with both options
│
├─ userpackage/<flight>/<hotel>/<date>/<rooms>/<seats> - Complete booking
│  └─ @login_required → Create BookPackage → Redirect to /accounts/profile/
│
├─ accounts/profile/ - Dashboard (login required)
│  └─ Displays BookFlight, BookHotel, BookPackage for current user
│
├─ cancelflight/<flight>/<date>/<seats> - Confirmation to cancel
├─ concanflight/<flight>/<date>/<seats> - Perform cancellation
├─ cancelhotel/<hotel>/<date>/<room> - Confirmation to cancel
├─ concanhotel/<hotel>/<date>/<room> - Perform cancellation
├─ cancelpackage/<flight>/<seat>/<hotel>/<date>/<room> - Confirmation
└─ concanpackage/<flight>/<seat>/<hotel>/<date>/<room> - Perform cancellation

admin/ - Django admin panel
```

## Authentication & Authorization

```
Public Pages (No Login Required):
├─ / (home)
├─ /register/ (signup)
├─ /accounts/login/ (login)
├─ /flights/ (search - form submission OK)
├─ /hotels/ (search - form submission OK)
├─ /package/ (search - form submission OK)
└─ /places/ (view attractions)

Protected Pages (@login_required):
├─ /accounts/profile/ (dashboard)
├─ /bookflight/<...> (confirmation & booking)
├─ /userflight/<...> (complete booking)
├─ /bookhotel/<...> (confirmation & booking)
├─ /userhotel/<...> (complete booking)
├─ /bookpackage/<...> (confirmation & booking)
├─ /userpackage/<...> (complete booking)
├─ /cancelflight/<...> (cancel flight)
├─ /cancelhotel/<...> (cancel hotel)
└─ /cancelpackage/<...> (cancel package)

Admin Pages:
└─ /admin/ (Django admin - superuser only)
```

## Key Classes & Methods

### Models (travelapp/models.py)
- `City` - Locations available
- `Flights` - Available flights (seats, price, times)
- `Hotels` - Available hotels (rooms, price, amenities)
- `Famous` - Tourist attractions per city
- `BookFlight` - User flight bookings (with seat count)
- `BookHotel` - User hotel bookings (with room count)
- `BookPackage` - User combined bookings (flight + hotel)

### Views (travelapp/views.py)
- **Search Views**: `FlightView()`, `HotelView()`, `PackageView()`, `PlacesView()`
  - Form validation → Query filter → Render with results
  
- **Confirmation Views**: `Flightbook()`, `Hotelbook()`, `PackageBook()`
  - Calculate availability → Show price → Render confirmation page
  
- **Booking Views**: `FlightSubmit()`, `HotelSubmit()`, `PackageSubmit()`
  - Create booking record → Save to DB → Redirect to dashboard
  
- **Dashboard**: `Dashboard()`
  - Display all bookings for current user
  
- **Cancellation Views**: `CancelFlight()`, `ConfirmCancelFlight()`, etc.
  - Two-step confirmation → Delete booking → Redirect to dashboard

### Forms (travelapp/forms.py)
- `HotelForm` - City + date search
- `FlightForm` - Source + destination + date search
- `ChoiceForm` - Flight + hotel selection for packages
- `SeatForm` / `RoomForm` - Quantity input on confirmation pages
- `SignUpForm` - Registration with password matching validation

## Important Implementation Details

### Date Handling
- **Stored As**: `CharField(max_length=20)` NOT DateField
- **Format**: "YYYY-MM-DD" (ISO format string)
- **In URLs**: Passed as string parameters, not converted
- **In Queries**: String comparison works correctly with this format

### Availability Logic
- **Key Point**: Must count BOTH regular bookings AND package bookings
- **Why**: Package bookings consume from same pool
- **Example**: If flight has 500 seats and 300 BookFlight + 50 BookPackage exist, only 150 remain

### Context Dictionary Composition
```python
# Pattern used throughout views:
f = {'Flights': flights}
h = {'Hotels': hotels}
d = {'date': date}
response = {**f, **h, **d}  # Dict unpacking - combines all
```

### Template Link Format
```html
<!-- Hotel booking link with spaces in URL -->
<a href='/userhotel/{{ i.hotel_name }}/{{ date }}/{{ roomreq }}'>
  <!-- Browser auto-encodes: "The Lalit New Delhi" → "The%20Lalit%20New%20Delhi" -->
</a>
```

---
**Last Updated**: November 13, 2025  
**Documentation by**: AI Code Assistant

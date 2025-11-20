# Tour & Travel Django App

A full-featured Django web application for booking flights, hotels, and travel packages. Users can search for available flights and hotels, make bookings, manage their bookings, and cancel reservations.

## 🎯 Features

- **User Authentication**: Register and login securely
- **Flight Search & Booking**: Search flights by source/destination and date, book seats
- **Hotel Search & Booking**: Search hotels by city and date, book rooms
- **Package Bookings**: Combined flight + hotel bookings for complete travel packages
- **Famous Places**: Explore popular tourist destinations in different cities
- **Dashboard**: View, manage, and cancel all your bookings
- **Admin Panel**: Manage cities, hotels, flights, famous places, and bookings
- **Date Validation**: Automatic date format parsing (YYYY-MM-DD)
- **Availability Tracking**: Real-time seat/room availability calculation

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite3 (included)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Python**: 3.11+
- **Additional Libraries**: Pillow (image handling), asgiref, sqlparse

## 📋 Prerequisites

- Python 3.11 or higher
- Git (optional, for version control)
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Abhishekpal1307/tour-and--travel-Django.git
cd tour-and--travel-Django
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with:
- Username
- Email
- Password (enter twice for confirmation)

### 6. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## 📖 Usage Guide

### Home Page
- Navigate to http://127.0.0.1:8000/
- Click on "Register" to create a new account
- Log in with your credentials

### Booking Flights
1. Click **Flights** in the navigation menu
2. Enter:
   - **Source**: City name (e.g., "MUMBAI")
   - **Destination**: City name (e.g., "DELHI")
   - **Date**: Format YYYY-MM-DD (e.g., "2025-12-30")
3. Click **SEARCH** to view available flights
4. Click **BOOK** on a flight to proceed
5. Enter number of seats and click **SEARCH**
6. Click the **BOOK** link to confirm the booking
7. Your booking will appear on the **Dashboard**

### Booking Hotels
1. Click **Hotels** in the navigation menu
2. Enter:
   - **City**: Hotel location (e.g., "DELHI")
   - **Date**: Format YYYY-MM-DD (e.g., "2025-12-30")
3. Click **SEARCH** to view available hotels
4. Click **BOOK** on a hotel to proceed
5. Enter number of rooms and click **SEARCH**
6. Click the **BOOK** link to confirm the booking
7. Your booking will appear on the **Dashboard**

### Booking Packages
1. Click **Packages** in the navigation menu
2. Enter:
   - **Source**: Flight departure city
   - **Destination**: Flight arrival & hotel location
   - **Date**: Travel date (YYYY-MM-DD format)
3. Click **SEARCH** to view available flights and hotels
4. Click **BOOK** on desired items
5. Enter flight seats and hotel rooms
6. Confirm the booking
7. View package booking on **Dashboard**

### Explore Famous Places
1. Click **Places** in the navigation menu
2. Select a city to see famous tourist destinations
3. View descriptions and images of popular attractions

### Manage Bookings
1. Log in to your account
2. Click **Dashboard** (top-right corner)
3. View all your:
   - **Flight Bookings**: With flight number, date, seats booked
   - **Hotel Bookings**: With hotel name, date, rooms booked
   - **Package Bookings**: Combined flight + hotel bookings
4. Click **Cancel** to cancel any booking
5. Confirm cancellation when prompted

### Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Log in with superuser credentials
3. Manage:
   - **Cities**: Add/edit/delete cities
   - **Flights**: Add/edit/delete flights with details
   - **Hotels**: Add/edit/delete hotels with amenities
   - **Famous Places**: Add/edit tourist attractions
   - **Bookings**: View/delete all user bookings

## 📁 Project Structure

```
tour-and--travel-Django/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── manage.py                          # Django management script
├── db.sqlite3                         # SQLite database (auto-created)
│
├── tourAndTravel/                     # Project configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── asgi.py                        # ASGI config
│   └── wsgi.py                        # WSGI config
│
├── travelapp/                         # Main Django app
│   ├── models.py                      # Database models
│   ├── views.py                       # View functions
│   ├── forms.py                       # Django forms
│   ├── urls.py                        # App URL routing
│   ├── admin.py                       # Admin configuration
│   ├── migrations/                    # Database migrations
│   └── tests.py                       # Tests
│
├── templates/                         # HTML templates
│   ├── index.html                     # Home page
│   ├── flights.html                   # Flight search
│   ├── hotels.html                    # Hotel search
│   ├── package.html                   # Package search
│   ├── places.html                    # Famous places
│   ├── dashboard.html                 # User dashboard
│   ├── bookflight.html                # Flight booking confirmation
│   ├── bookhotel.html                 # Hotel booking confirmation
│   ├── bookpackage.html               # Package booking confirmation
│   ├── cancelflight.html              # Flight cancellation
│   ├── cancelhotel.html               # Hotel cancellation
│   ├── cancelpackage.html             # Package cancellation
│   └── registration/                  # Auth templates
│       ├── login.html
│       └── register.html
│
├── static/                            # Static files
│   ├── css/                           # Stylesheets
│   │   ├── style.css
│   │   └── styleone.css
│   └── img/                           # Images
│       ├── logo.png
│       ├── travel.png
│       ├── plane.png
│       └── hotel*.png
│
├── media/                             # User-uploaded files (created at runtime)
│   └── img/                           # Hotel and place images
│
└── scripts/                           # Utility scripts
    ├── seed_hotels.py                 # Seed hotel data
    └── seed_famous_places.py          # Seed famous places data
```

## 🔧 Database Models

### City
- `city`: City name (CharField)
- `bestlink`: Link to city info
- `weekgetlinks`: Weekend getaway links

### Flights
- `flight_num`: Flight number (unique)
- `source`: Departure city
- `destination`: Arrival city
- `city`: Foreign key to City
- `eprice`: Price per seat
- `dept_time`: Departure time
- `dest_time`: Arrival time
- `company`: Airline company
- `seats`: Total seats available

### Hotels
- `hotel_name`: Hotel name
- `city`: Foreign key to City
- `hotel_address`: Address
- `hotel_price`: Price per room
- `hotel_rating`: Star rating
- `amenities`: List of amenities
- `distfromap`: Distance from airport
- `rooms`: Total rooms available
- `image1`: Hotel image

### Famous
- `city`: Foreign key to City
- `place_name`: Attraction name
- `image`: Place image
- `desc`: Description

### BookFlight
- `username`: Foreign key to User
- `flight_num`: Flight booked
- `date`: Booking date
- `seat`: Number of seats

### BookHotel
- `username`: Foreign key to User
- `hotel_name`: Hotel booked
- `date`: Booking date
- `room`: Number of rooms

### BookPackage
- `username`: Foreign key to User
- `flight_num`: Flight in package
- `hotel_name`: Hotel in package
- `date`: Booking date
- `seat`: Seats in package
- `room`: Rooms in package

## 🐛 Troubleshooting

### Date Format Errors
- Ensure dates are in **YYYY-MM-DD** format (e.g., `2025-12-30`)
- The app will not accept other formats

### No Search Results
- Verify data exists in the admin panel
- Check that city names match exactly (case-sensitive in some filters)
- Ensure the date is in the future

### Booking Not Appearing
- Confirm you're logged in
- Refresh the dashboard page
- Check that availability wasn't fully booked

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Clear browser cache (Ctrl+Shift+Delete)

### Database Issues
- To reset the database: `rm db.sqlite3` then run `python manage.py migrate`
- WARNING: This will delete all existing bookings and user accounts

## 📝 Important Notes

- **Login Required**: All booking operations require user authentication
- **Date Format**: All dates must be in YYYY-MM-DD format (e.g., 2025-11-15)
- **Availability**: System automatically calculates remaining seats/rooms by counting existing bookings
- **Hotel Names**: Spaces are auto-encoded as %20 in URLs
- **Development Server**: Not suitable for production use

## 🔐 Security Notes

- Change `SECRET_KEY` in `tourAndTravel/settings.py` for production
- Set `DEBUG = False` in production
- Update `ALLOWED_HOSTS` with your domain in production
- Use environment variables for sensitive data
- Never commit database files or `.env` files to Git

## 📦 Dependencies

All dependencies are listed in `requirements.txt`:
- Django 5.2.8 - Web framework
- Pillow - Image processing
- asgiref - ASGI utilities
- sqlparse - SQL parsing

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Abhishek Pal**

## 🔗 Links

- **GitHub Repository**: https://github.com/Abhishekpal1307/tour-and--travel-Django
- **Issues**: Report bugs and request features in the Issues tab
- **Discussions**: Share ideas and ask questions

## ❓ FAQ

**Q: Can I use this in production?**
A: No, the development server is not suitable for production. Use a production WSGI server like Gunicorn or uWSGI with a reverse proxy like Nginx.

**Q: How do I add more cities/flights/hotels?**
A: Use the Django admin panel at `/admin/` to add, edit, or delete entries.

**Q: Can I customize the design?**
A: Yes! Modify the CSS files in `static/css/` and HTML templates in `templates/`.

**Q: How do I seed the database with demo data?**
A: Run the scripts: `python scripts/seed_hotels.py` and `python scripts/seed_famous_places.py`

**Q: Is this production-ready?**
A: No, this is a learning/demo project. For production, add proper error handling, validation, logging, and security measures.

---

**Last Updated**: November 20, 2025  
**Django Version**: 5.2.8  
**Python**: 3.11+  
**Status**: ✅ Fully Functional

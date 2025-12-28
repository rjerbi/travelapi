# Travel Booking API

A Flask-based API for managing clients, reservations, reviews, and packages. Includes JWT authentication for admins, MongoDB integration, and data validation with Marshmallow. Enables CRUD operations and secure access to manage travel or service bookings.

---

## Features

### Clients
- Add, update, delete, and retrieve client information
- Handles personal details, preferred destinations, languages, and budgets
- Validates emails and prevents duplicates

### Reservations
- Create, update, delete, and retrieve reservations
- Link reservations to clients
- Automatic reservation date assignment

### Reviews (Avis)
- Add, retrieve, and delete reviews
- Link reviews to clients and optional reservations

### Admin
- JWT authentication for secure access
- Admin dashboard endpoint to view all clients, reservations, reviews, and packages

### Packages
- Add, update, delete, and retrieve packages
- Filter packages by rent type, property type, city, and price range
- Automatic timestamp for creation and updates

---

## Technologies Used

- **Backend:** Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, Marshmallow-SQLAlchemy
- **Database:** MongoDB
- **Authentication:** JWT tokens
- **Other Tools:** Python-dotenv for environment variables, Werkzeug for password hashing

---

## Installation

### 1. Create virtual environment :
python -m venv env
env\Scripts\activate

### 2. Install dependencies : 
pip install -r requirements.txt

### 3. Run the server : 
python app.py







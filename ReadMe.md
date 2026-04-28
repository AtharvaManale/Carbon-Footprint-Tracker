# Carbon Emission Monitoring System

A full-stack system to track vendor sales, calculate CO2 emission scores, analyze trends, and help auditors evaluate vendors based on environmental performance.

---

## Tech Stack

### Backend
- Python (Flask)
- PostgreSQL (hosted on Render)
- SQLAlchemy ORM
- Session-based Authentication
- Flask-Migrate for DB migrations
- Gunicorn for production server

### Frontend (Android)
- Java (Android Studio)
- Retrofit2 + OkHttp3 for API calls
- JavaNetCookieJar for session cookie persistence
- MPAndroidChart for emission trend graphs
- RecyclerView for lists
- Navigation Component (NavGraph)
- Material Design 3 (green environmental theme)

---

## User Roles

| Role | Description |
|------|-------------|
| auditor | Manages and monitors a group of vendors |
| vendor | Logs daily sales, tracked by an auditor |

Every vendor is assigned to one auditor at signup. Vendors have a contract end date managed by the auditor.

---

## Project Structure

```
Backend/
├── routes/
│   ├── auth.py         # Authentication routes
│   ├── sales.py        # Sales management routes
│   ├── analytics.py    # CO2 analytics routes
│   └── auditor.py      # Auditor panel routes
├── models/
│   └── models.py       # Database models
├── extensions.py       # DB and Migrate instances
├── config.py           # Environment config
└── __init__.py         # App factory
run.py                  # App entry point
```

---

## Database Models

### users
| Field | Type | Description |
|-------|------|-------------|
| id | Integer PK | Auto increment |
| username | String | Unique username |
| password | String | Hashed password |
| shop_name | String | Vendor shop name (null for auditors) |
| role | String | vendor or auditor |
| auditor_id | FK → users.id | Assigned auditor (vendors only) |
| created_at | DateTime | Registration date |
| ending_at | Date | Contract end date (vendors only) |

### products
| Field | Type | Description |
|-------|------|-------------|
| product_id | Integer PK | Auto increment |
| name | String | Product name |
| emission_factor | Float | CO2 score per unit |

### sales_data
| Field | Type | Description |
|-------|------|-------------|
| sales_id | Integer PK | Auto increment |
| vendor_id | FK → users.id | Vendor who made the sale |
| product_id | FK → products.id | Product sold |
| quantity | Integer | Quantity sold |
| sales_date | Date | Date of sale |

### daily_emissions
| Field | Type | Description |
|-------|------|-------------|
| emission_id | Integer PK | Auto increment |
| vendor_id | FK → users.id | Vendor |
| total_co2 | Numeric(8,2) | Total CO2 score for the day |
| sales_date | Date | Date of emission record |

---

## API Reference

### Auth — /auth

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | /auth/auditors | Public | Get list of all auditors |
| POST | /auth/signup | Public | Register new user |
| POST | /auth/login | Public | Login user |
| GET | /auth/logout | Any | Logout user |
| GET | /auth/check | Any | Check current session |

#### POST /auth/signup
```json
{
  "user_name": "john",
  "password": "pass123",
  "confirm_password": "pass123",
  "role": "vendor",
  "shop_name": "John's Shop",
  "auditor_id": 1,
  "end": "31-12-2025"
}
```

#### GET /auth/check Response
```json
{
  "user": {
    "id": 1,
    "username": "john",
    "shop_name": "John's Shop",
    "role": "vendor"
  }
}
```

---

### Sales — /sales

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | /sales/products | Vendor | Get all available products |
| POST | /sales/add | Vendor | Add or update today's sale |
| PUT | /sales/update | Vendor | Overwrite quantity for a sale |
| GET | /sales/data | Vendor | Get own last 7 days sales with daily CO2 scores |

#### POST /sales/add
```json
{
  "product": "Plastic Cup",
  "quantity": 50
}
```

#### GET /sales/data Response
```json
{
  "sales": {
    "28-04-2026": [
      { "product": "Plastic Cup", "quantity": 50 }
    ]
  },
  "daily_emission_score": {
    "28-04-2026": 780.0
  }
}
```

---

### Analytics — /analytics

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | /analytics/totalCO2 | Vendor | Calculate and save today's emission score |
| GET | /analytics/emission-trend/<id> | Auditor | Get 7-day emission trend for a vendor |
| GET | /analytics/ratings | Any | Get vendor ratings and rankings |

#### GET /analytics/ratings Response (vendor)
```json
{
  "ratings": [...],
  "rating": 4,
  "rank": 2
}
```

#### GET /analytics/emission-trend/<id> Response
```json
{
  "emission_trend": [
    { "date": "28-04-2026", "total_co2": 780.0 }
  ],
  "days_recorded": 6,
  "date_issue": false
}
```

---

### Auditor — /auditor

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | /auditor/vendors | Auditor | List all vendors under this auditor |
| GET | /auditor/sales/<id> | Auditor | Get vendor last 7 days sales and daily emission scores |
| GET | /auditor/recommendations | Auditor | Get recommendations for all vendors |

#### GET /auditor/vendors Response
```json
{
  "vendors": [
    {
      "vendor_id": 2,
      "vendor_name": "Vendor 1",
      "shop_name": "Canteen 1",
      "end_at": "2025-12-31"
    }
  ]
}
```

#### GET /auditor/sales/<id> Response
```json
{
  "sales": {
    "28-04-2026": [
      { "product": "Plastic Cup", "quantity": 95 }
    ]
  },
  "daily_emissions": {
    "28-04-2026": 780.0
  }
}
```

#### GET /auditor/recommendations Response
```json
{
  "data": [
    {
      "vendor_id": 2,
      "vendor_name": "Vendor 1",
      "shop_name": "Canteen 1",
      "avg_co2": 550.0,
      "trend": "increasing",
      "recommendation": "Replace vendor"
    }
  ]
}
```

---

## Core Logic

### CO2 Score Calculation
```
CO2 Score = Quantity x Emission Factor
Daily Score = Sum of all products sold that day
```

Example:
```
Plastic Cup x 80   = 80 x 2.5 = 200
Plastic Plate x 60 = 60 x 3.0 = 180
Straw Plastic x 50 = 50 x 1.2 = 60
Total Day Score    = 440
```

### Product Emission Factors

Emission factors represent the relative environmental impact per unit of each product based on lifecycle assessment data for single-use food service items.

| Product | Emission Factor |
|---------|----------------|
| Plastic Cup | 2.5 |
| Paper Cup | 1.2 |
| Plastic Plate | 3.0 |
| Paper Plate | 1.5 |
| Plastic Spoon | 1.8 |
| Wooden Spoon | 0.9 |
| Steel Bottle | 6.5 |
| Plastic Bottle | 3.5 |
| Aluminum Can | 4.0 |
| Glass Bottle | 5.0 |
| Food Packaging Plastic | 2.8 |
| Food Packaging Paper | 1.4 |
| Straw Plastic | 1.2 |
| Straw Paper | 0.6 |
| Carry Bag Plastic | 2.2 |
| Carry Bag Cloth | 0.5 |
| Thermocol Plate | 3.8 |
| Reusable Container | 1.0 |

---

### Rating System

Based on average daily CO2 score over last 7 days. Thresholds are calibrated for a college canteen serving approximately 150 to 300 students per day.

| Avg CO2 Score | Rating |
|---------------|--------|
| 300 or below | 5 stars |
| 301 to 450 | 4 stars |
| 451 to 600 | 3 stars |
| 601 to 800 | 2 stars |
| above 800 | 1 star |

Vendors are ranked among all vendors under the same auditor, sorted by lowest average CO2 score.

---

### Recommendation Logic

Recommendations are based on two factors — average CO2 score and emission trend direction over the last 7 days. This prevents low-volume vendors from appearing eco-friendly simply due to fewer sales.

| Avg CO2 Score | Trend | Recommendation |
|---------------|-------|----------------|
| 400 or below | Decreasing | Excellent vendor |
| 400 or below | Increasing | Monitor vendor |
| 400 or below | Stable | Excellent vendor |
| 401 to 600 | Decreasing | Acceptable |
| 401 to 600 | Increasing | Warning |
| 401 to 600 | Stable | Stable performance |
| above 600 | Decreasing | Give improvement time |
| above 600 | Increasing | Replace vendor |
| above 600 | Stable | Stable performance |

---

## Android App Screens

### Vendor Flow
```
Login / Signup
     |
Vendor Dashboard
  |-- Profile card (name, shop name, contract end date)
  |-- Performance card (star rating, rank, avg CO2 score)
  |-- Add Today's Sales button
  |-- Last 7 Days Sales (grouped by date, newest first)
       |-- Each card shows products, quantities and daily CO2 score
       |-- Update button on today's card to correct quantity
  |-- Logout
```

### Auditor Flow
```
Login / Signup
     |
Auditor Dashboard
  |-- Auditor profile
  |-- Vendors list (clickable cards with rating and rank)
  |     |
  |   Vendor Detail Screen
  |     |-- Performance card (stars, rank, avg CO2 score)
  |     |-- Last 7 Days Sales (grouped by date, newest first)
  |     |-- Emission Trend Line Chart
  |
  |-- Recommendations panel (color coded by severity)
  |-- Logout
```

---

## Setup and Running

### Backend

1. Clone the repo and create a virtual environment:
```bash
python -m venv .mini
.mini\Scripts\activate      # Windows
source .mini/bin/activate   # Mac/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file:
```
Key=your_secret_key
DATABASE_URL=postgresql://user:password@host/dbname
```

4. Run migrations:
```bash
flask db upgrade
```

5. Start the server locally:
```bash
python run.py
```
Server runs on http://127.0.0.1:5000

### Android App

- Open project in Android Studio
- Run on emulator (Medium Phone recommended)
- Backend must be running
- For local testing, app connects to http://10.0.2.2:5000
- For production, update BASE_URL in ApiClient.java to deployed Render URL

### Deployment

Backend is deployed on Render using Gunicorn:
- Start command: gunicorn run:app
- Database: PostgreSQL hosted on Render
- Environment variables: Key and DATABASE_URL set in Render dashboard

---

## Important Notes

- Session-based auth — cookies are persisted across requests using JavaNetCookieJar
- Android requires network_security_config.xml to allow HTTP to 10.0.2.2 during local development
- All protected routes return 401 if not logged in, 403 if wrong role
- total_co2 stored as Numeric(8,2) — always cast to float() before arithmetic in Python
- Render free tier sleeps after 15 minutes of inactivity — first request after sleep takes 30 to 50 seconds
- CO2 Score label used throughout UI instead of kg unit as scores use a normalized emission scale

---

## Project Goal

To help auditors evaluate vendors based on environmental impact and encourage sustainable practices through data-driven insights. The system creates accountability and transparency in canteen environmental performance, scalable to any institution.

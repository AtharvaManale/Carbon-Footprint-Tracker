# 🌱 Carbon Emission Monitoring System

A full-stack system to track vendor sales, calculate CO₂ emissions, analyze trends, and help auditors evaluate vendors based on environmental performance.

---

## 🚀 Tech Stack

### Backend
- Python (Flask)
- MySQL
- SQLAlchemy ORM
- Session-based Authentication
- Flask-Migrate for DB migrations
- Flask-CORS for cross-origin support

---

## 👥 User Roles

| Role | Description |
|------|-------------|
| `auditor` | Manages and monitors a group of vendors |
| `vendor` | Logs daily sales, tracked by an auditor |

Every vendor is assigned to one auditor at signup. Vendors have a contract end date managed by the auditor.

---

## 📁 Project Structure

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

## 🗄️ Database Models

### `users`
| Field | Type | Description |
|-------|------|-------------|
| id | Integer PK | Auto increment |
| username | String | Unique username |
| password | String | Hashed password |
| shop_name | String | Vendor shop name (null for auditors) |
| role | String | `vendor` or `auditor` |
| auditor_id | FK → users.id | Assigned auditor (vendors only) |
| created_at | DateTime | Registration date |
| ending_at | Date | Contract end date (vendors only) |

### `products`
| Field | Type | Description |
|-------|------|-------------|
| product_id | Integer PK | Auto increment |
| name | String | Product name |
| emission_factor | Float | CO₂ per unit |

### `sales_data`
| Field | Type | Description |
|-------|------|-------------|
| sales_id | Integer PK | Auto increment |
| vendor_id | FK → users.id | Vendor who made the sale |
| product_id | FK → products.id | Product sold |
| quantity | Integer | Quantity sold |
| sales_date | Date | Date of sale |

### `daily_emissions`
| Field | Type | Description |
|-------|------|-------------|
| emission_id | Integer PK | Auto increment |
| vendor_id | FK → users.id | Vendor |
| total_co2 | Numeric(5,2) | Total CO₂ for the day |
| sales_date | Date | Date of emission record |

---

## 🔌 API Reference

### 🔐 Auth — `/auth`

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | `/auth/auditors` | Public | Get list of all auditors |
| POST | `/auth/signup` | Public | Register new user |
| POST | `/auth/login` | Public | Login user |
| GET | `/auth/logout` | Any | Logout user |
| GET | `/auth/check` | Any | Check current session |

#### POST `/auth/signup`
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

#### GET `/auth/check` Response
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

### 🛒 Sales — `/sales`

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | `/sales/products` | Vendor | Get all available products |
| POST | `/sales/add` | Vendor | Add or update today's sale |
| PUT | `/sales/update` | Vendor | Overwrite quantity for a sale |
| GET | `/sales/data` | Vendor | Get own last 7 days sales |

#### POST `/sales/add`
```json
{
  "product": "Plastic Cup",
  "quantity": 50
}
```

#### GET `/sales/data` Response
```json
{
  "sales": {
    "28-03-2026": [
      { "product": "Plastic Cup", "quantity": 50 }
    ]
  }
}
```

---

### 📊 Analytics — `/analytics`

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | `/analytics/totalCO2` | Vendor | Calculate and save today's emission |
| GET | `/analytics/emission-trend/<id>` | Auditor | Get 7-day emission trend for a vendor |
| GET | `/analytics/ratings` | Any | Get vendor ratings and rankings |

#### GET `/analytics/ratings` Response (vendor)
```json
{
  "ratings": [...],
  "rating": 4,
  "rank": 2
}
```

#### GET `/analytics/emission-trend/<id>` Response
```json
{
  "emission_trend": [
    { "date": "28-03-2026", "total_co2": 450.5 }
  ],
  "days_recorded": 5,
  "date_issue": true
}
```

---

### 🧑‍💼 Auditor — `/auditor`

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | `/auditor/vendors` | Auditor | List all vendors under this auditor |
| GET | `/auditor/sales/<id>` | Auditor | Get vendor's last 7 days sales + emissions |
| GET | `/auditor/recommendations` | Auditor | Get recommendations for all vendors |

#### GET `/auditor/vendors` Response
```json
{
  "vendors": [
    {
      "vendor_id": 2,
      "vendor_name": "john",
      "shop_name": "John's Shop",
      "end_at": "2025-12-31"
    }
  ]
}
```

#### GET `/auditor/recommendations` Response
```json
{
  "data": [
    {
      "vendor_id": 2,
      "vendor_name": "john",
      "shop_name": "John's Shop",
      "avg_co2": 320.5,
      "trend": "increasing",
      "recommendation": "Warning"
    }
  ]
}
```

---

## 🧠 Core Logic

### CO₂ Calculation
```
CO₂ = Quantity × Emission Factor
```

### Product Emission Factors

| Product | Factor (kg CO₂/unit) |
|---------|----------------------|
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

### ⭐ Rating System

Based on average CO₂ over last 7 days:

| Avg CO₂ | Rating |
|---------|--------|
| ≤ 50 | ⭐⭐⭐⭐⭐ |
| ≤ 100 | ⭐⭐⭐⭐ |
| ≤ 200 | ⭐⭐⭐ |
| ≤ 350 | ⭐⭐ |
| > 350 | ⭐ |

Vendors are also ranked among all vendors under the same auditor, sorted by lowest average CO₂.

---

### 📈 Recommendation Logic

Based on average CO₂ and emission trend direction:

| Avg CO₂ | Trend | Recommendation |
|---------|-------|----------------|
| ≤ 200 | Decreasing | Excellent vendor |
| ≤ 200 | Increasing | Monitor vendor |
| 200–350 | Decreasing | Acceptable |
| 200–350 | Increasing | Warning |
| > 500 | Decreasing | Give improvement time |
| > 500 | Increasing | Replace vendor |
| Any | Stable | Stable performance |

---

## 📱 Android App Screens

### Vendor Flow
```
Login / Signup
     ↓
Vendor Dashboard
  ├── Profile (name, shop, contract end date)
  ├── Last 7 Days Sales list
  ├── Add Today's Sales → Sales Input Screen
  └── Logout
```

### Auditor Flow
```
Login / Signup
     ↓
Auditor Dashboard
  ├── Auditor Profile
  ├── Vendors List (clickable)
  │     ↓
  │   Vendor Detail Screen
  │     ├── Last 7 Days Sales
  │     ├── Rating & Rank
  │     └── Emission Trend Chart
  ├── Recommendations Panel
  └── Logout
```

---

## ⚙️ Setup & Running

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

3. Create a `.env` file:
```
Key=your_secret_key
DATABASE_URL=mysql://user:password@localhost/dbname
```

4. Run migrations:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Start the server:
```bash
python run.py
```
Server runs on `http://127.0.0.1:5000`


---

## 🎯 Project Goal

To help auditors evaluate vendors based on environmental impact and encourage sustainable practices through data-driven insights.

# 🌱 Carbon Emission Monitoring System (Backend)

This backend provides APIs for a system that tracks vendor sales, calculates CO₂ emissions, analyzes trends, and helps auditors evaluate vendors based on environmental performance.

---

# 🚀 Tech Stack

- Python (Flask)
- MySQL / SQLite
- SQLAlchemy ORM
- Session-based Authentication

---

# 📌 Project Workflow

## 1️⃣ Authentication

- Vendors and Auditors can **Sign Up / Login**
- Session-based authentication is used
- After login, user role determines access:
  - `vendor`
  - `auditor`

---

# 📱 Android App Flow (UI Guide)

## 👤 Vendor Side

### 🔐 1. Signup / Login Screen

- Fields:
  - Username
  - Password
  - Shop Name (for vendors)

- APIs:
  - `POST /signup`
  - `POST /login`

---

### 🏠 2. Vendor Home Dashboard

Display:

- Username
- Shop Name
- ⭐ Rating
- 🏆 Rank
- 📊 Average CO₂ Emission

APIs:

- `GET /ratings`
- `GET /emission-trend`

---

### 📝 3. Daily Sales Input Form

Dynamic form:

- Dropdown to select product
- Input field for quantity
- Multiple entries allowed

API:

- `POST /sales/add`

---

### 📊 4. Emission Trend Graph

- Show last 7 days CO₂ emission graph

API:

- `GET /emission-trend`

---

## 🧑‍💼 Auditor Side

### 🔐 1. Login / Signup

Same as vendor (role = auditor)

---

### 📋 2. Auditor Dashboard (Vendor List)

Display:

- Vendor Name
- Shop Name

API:

- `GET /vendors`

---

### 📊 3. Vendor Detail Screen

When auditor clicks a vendor:

Show:

- Last 7 days sales
- Daily emissions graph

API:

- `GET /sales/<vendor_id>`

---

### 🧠 4. Recommendations Panel

Show:

- Avg CO₂
- Trend (increasing/decreasing)
- Recommendation

API:

- `GET /recommendations`

---

# 🔌 API Endpoints Summary

## 🔐 Auth

| Method | Endpoint | Description   |
| ------ | -------- | ------------- |
| POST   | /signup  | Register user |
| POST   | /login   | Login user    |

---

## 🛒 Sales

| Method | Endpoint    | Description              |
| ------ | ----------- | ------------------------ |
| POST   | /sales/add  | Add/update daily sales   |
| GET    | /sales/data | Vendor last 7 days sales |

---

## 📊 Analytics

| Method | Endpoint        | Description               |
| ------ | --------------- | ------------------------- |
| POST   | /totalCO2       | Calculate daily emission  |
| GET    | /emission-trend | Get emission graph data   |
| GET    | /ratings        | Get vendor ratings & rank |

---

## 🧑‍💼 Auditor

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | /vendors         | List all vendors         |
| GET    | /sales/<id>      | Vendor sales + emissions |
| GET    | /recommendations | Vendor evaluation        |

---

# 🧠 Core Logic

## CO₂ Calculation

```bash
    "CO2 = Quantity * Emission Factor"
```

Emission factors are predefined for each product.

('Plastic Cup', 2.5),
('Paper Cup', 1.2),
('Plastic Plate', 3.0),
('Paper Plate', 1.5),
('Plastic Spoon', 1.8),
('Wooden Spoon', 0.9),
('Steel Bottle', 6.5),
('Plastic Bottle', 3.5),
('Aluminum Can', 4.0),
('Glass Bottle', 5.0),
('Food Packaging Plastic', 2.8),
('Food Packaging Paper', 1.4),
('Straw Plastic', 1.2),
('Straw Paper', 0.6),
('Carry Bag Plastic', 2.2),
('Carry Bag Cloth', 0.5),
('Thermocol Plate', 3.8),
('Reusable Container', 1.0)

---

## 📈 Rating System

Based on **average CO₂ (last 7 days)**:

| Avg CO₂ | Rating     |
| ------- | ---------- |
| ≤ 5     | ⭐⭐⭐⭐⭐ |
| ≤ 10    | ⭐⭐⭐⭐   |
| ≤ 15    | ⭐⭐⭐     |
| ≤ 20    | ⭐⭐       |
| > 20    | ⭐         |

---

## 📊 Recommendation Logic

Based on:

- Average CO₂
- Emission Trend

| Condition           | Recommendation |
| ------------------- | -------------- |
| Low + Decreasing    | Excellent      |
| Low + Increasing    | Monitor        |
| Medium + Increasing | Warning        |
| High + Increasing   | Replace Vendor |

---

# 💡 Notes for Android Developers

- Use **dropdown for product selection**
- Store `vendor_id` from `/vendors` API
- Use **RecyclerView** for lists
- Use **Graph library** for emission trends
- All APIs return JSON

---

# 🎯 Project Goal

To help auditors evaluate vendors based on environmental impact and encourage sustainable practices using data-driven insights.

---

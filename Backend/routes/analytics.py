from flask import session, Blueprint, jsonify
from Backend.models.models import products, sales_data, daily_emissions, users
from datetime import date, timedelta
from Backend.extensions import db
from collections import defaultdict

analytics = Blueprint("analytics", __name__)

@analytics.route('/totalCO2', methods = ['GET', 'POST'])
def total_CO2():
    if "user_id" in session:
        if session["user_role"] == "vendor":
            today = date.today()
            sales = sales_data.query.filter_by(vendor_id = session["user_id"],sales_date = today).all()

            totalco2 = 0
            for sale in sales:
                product = products.query.get(sale.product_id)
                product_co2 = product.emission_factor * sale.quantity
                totalco2 += product_co2

            todays_emission = daily_emissions.query.filter_by(sales_date = today, vendor_id = session["user_id"]).first()

            if todays_emission:
                todays_emission.total_co2 = totalco2

                db.session.commit()
                return jsonify({"message":"total co2 emissions updated!",
                                "emission": totalco2 }), 200
            
            new_emission = daily_emissions(
                vendor_id = session["user_id"],
                total_co2 = totalco2,
                sales_date = today
            )

            db.session.add(new_emission)
            db.session.commit()

            return jsonify({"message" : "emissions calculated successfully!",
                            "emission": totalco2 }), 202
        
        return jsonify({"error": "Only vendors can add or update sale!"}), 403
    
    return jsonify({"error":"Not logged in!"}), 401

@analytics.route("/emission-trend/<int:id>", methods = ['GET'])
def trends(id):
    if "user_id" in session:
        if session["user_role"] == "auditor":
            limit_date = date.today() - timedelta(days=7)

            emissions = daily_emissions.query.filter(daily_emissions.vendor_id == id, daily_emissions.sales_date >= limit_date).all()
            emission_trend = []
            for emission in emissions:
                emission_trend.append({"date": emission.sales_date.strftime("%d-%m-%Y"), 
                                    "total_co2": float(emission.total_co2)})
            days = len(emission_trend)
            date_issue = False
            if days < 7:
                date_issue = True

            return jsonify({"message":"Emission trend!",
                            "emission_trend" : emission_trend,
                            "days_recorded":days,
                            "date_issue":date_issue}), 200
        
        return jsonify({"error":"Only auditors have access to emission trends"})

    return jsonify({"error":"Not logged in!"}), 401

@analytics.route("/ratings", methods = ['GET'])
def ratings():
    if "user_id" in session:
        vendors = users.query.filter_by(role = "vendor", auditor_id = session['user_id']).all()
        limit_date = date.today() - timedelta(days=7)

        ratings = []

        for vendor in vendors:
            emissions = daily_emissions.query.filter(
                daily_emissions.vendor_id == vendor.id,
                daily_emissions.sales_date >= limit_date
            ).all()

            if not emissions:
                continue

            emissions_by_date = defaultdict(float)

            for e in emissions:
                emissions_by_date[e.sales_date] += e.total_co2

            total = sum(emissions_by_date.values())

            num_days = len(emissions_by_date)

            avg_emission = total / num_days if num_days > 0 else 0

            if avg_emission <= 200:
                rating = 5
            elif avg_emission <= 350:
                rating = 4
            elif avg_emission <= 500:
                rating = 3
            elif avg_emission <= 700:
                rating = 2
            else:
                rating = 1

            ratings.append({
                "vendor": vendor.username,
                "shop_name": vendor.shop_name,
                "avg_co2": float(avg_emission),
                "rating": rating
            })

        ratings.sort(key=lambda x: x["avg_co2"])

        for i, vendor in enumerate(ratings, start=1):
            vendor["rank"] = i

        return jsonify({
            "message": "Vendors ratings!",
            "ratings": ratings
        }), 200
    
    return jsonify({"error":"Not logged in!"}), 401

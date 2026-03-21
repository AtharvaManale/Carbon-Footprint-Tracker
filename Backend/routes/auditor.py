from flask import session, request, jsonify, Blueprint
from Backend.extensions import db
from Backend.models.models import users, daily_emissions, sales_data, products
from datetime import date, timedelta

auditor = Blueprint("auditor", __name__)

@auditor.route("/vendors", methods = ["GET"])
def panel():
    if "user_id" in session:
        if session["user_role"] == "auditor":
            vendors = users.query.filter_by(role = "vendor").all()
            vendors_data = []
            for vendor in vendors:
                vendors_data.append({"id": vendor.id,
                                    "vendor": vendor.username,
                                     "shop": vendor.shop_name,
                                     "end": vendor.ending_at})
        
            return jsonify({"message":"Vendors data for dashboard!",
                           "vendors": vendors_data }), 200
        
        return jsonify({"error": "Only auditors can access this panel!"}), 403
    
    return jsonify("Not logged in!"), 401

@auditor.route("/sales/<int:id>", methods = ["GET"])
def vendors_sales_data(id):
    if "user_id" in session:
        if session["user_role"] == "auditor":
            limit_date = date.today() - timedelta(days=7)
            sales = sales_data.query.filter(sales_data.vendor_id == id, sales_data.sales_date >= limit_date).all()

            data = {}

            for sale in sales:
                sdate = sale.sales_date.strftime("%d-%m-%Y")
                product = products.query.get(sale.product_id)
                if sdate not in data:
                    data[sdate] = []

                data[sdate].append({
                    "product":product.name,
                    "quantity":sale.quantity
                })

            emissions = daily_emissions.query.filter(daily_emissions.vendor_id == id, daily_emissions.sales_date >= limit_date).all()

            daily_emissions_data = []

            for emission in emissions:
                edate = emission.sales_date.strftime("%d-%m-%Y")
                daily_emissions_data.append({edate : emission.total_co2})

            return jsonify({"message":"sales of last 7 days!",
                        "sales": data,
                        "daily_emissions": daily_emissions_data}), 200
        
        return jsonify({"error": "Only auditors can access this panel!"}), 403

    return jsonify("Not logged in!"), 401


@auditor.route("/recommendations", methods=["GET"])
def recommendations():
    if "user_id" in session:
        if session["user_role"] == "auditor":
            vendors = users.query.filter_by(role="vendor").all()
            limit_date = date.today() - timedelta(days=7)

            results = []

            for vendor in vendors:

                emissions = daily_emissions.query.filter(daily_emissions.vendor_id == vendor.id,daily_emissions.sales_date >= limit_date).order_by(daily_emissions.sales_date).all()

                if not emissions:
                    continue

                values = [float(e.total_co2) for e in emissions]

                avg = sum(values) / len(values)

                trend_value = values[-1] - values[0]

                if trend_value > 0:
                    trend = "increasing"
                elif trend_value < 0:
                    trend = "decreasing"
                else:
                    trend = "stable"

                if avg <= 5 and trend == "increasing":
                    suggestion = "Monitor vendor"

                elif avg <= 5 and trend == "decreasing":
                    suggestion = "Excellent vendor"

                elif 5 < avg <= 10 and trend == "increasing":
                    suggestion = "Warning"

                elif 5 < avg <= 10 and trend == "decreasing":
                    suggestion = "Acceptable"

                elif avg > 10 and trend == "increasing":
                    suggestion = "Replace vendor"

                elif avg > 10 and trend == "decreasing":
                    suggestion = "Give improvement time"

                else:
                    suggestion = "Stable performance"

                results.append({"id": vendor.id,
                                "vendor": vendor.username,
                                "shop": vendor.shop_name,
                                "avg_co2": round(avg, 2),
                                "trend": trend,
                                "recommendation": suggestion
                                })

            return jsonify({"message": "Vendor recommendations",
                            "data": results
                            }), 200
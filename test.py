from Backend import create_app
from Backend.extensions import db
from Backend.models.models import sales_data, daily_emissions, products
from datetime import date, timedelta
from decimal import Decimal

app = create_app()

with app.app_context():

    # Clear existing data
    db.session.query(sales_data).delete()
    db.session.query(daily_emissions).delete()
    db.session.commit()
    print("Cleared existing data!")

    today = date.today()  # 28-04-2026
    day1 = date(2026, 4, 23)
    day2 = date(2026, 4, 24)
    day3 = date(2026, 4, 25)
    day4 = date(2026, 4, 26)
    day5 = date(2026, 4, 27)
    day6 = date(2026, 4, 28)  # today

    def get_product(name):
        return products.query.filter_by(name=name).first()

    # ─────────────────────────────────────────
    # VENDOR 1 - Canteen 1 - INCREASING TREND
    # Scores: 350 → 420 → 500 → 580 → 670 → 780
    # Recommendation: Replace vendor
    # ─────────────────────────────────────────
    vendor1_sales = [
        # Day 1 - 23 Apr - ~350
        (2, 'Plastic Cup', 40, day1),
        (2, 'Plastic Plate', 30, day1),
        (2, 'Plastic Spoon', 25, day1),
        (2, 'Carry Bag Plastic', 20, day1),
        (2, 'Straw Plastic', 30, day1),

        # Day 2 - 24 Apr - ~420
        (2, 'Plastic Cup', 50, day2),
        (2, 'Plastic Plate', 35, day2),
        (2, 'Plastic Spoon', 30, day2),
        (2, 'Carry Bag Plastic', 25, day2),
        (2, 'Straw Plastic', 35, day2),
        (2, 'Plastic Bottle', 10, day2),

        # Day 3 - 25 Apr - ~500
        (2, 'Plastic Cup', 60, day3),
        (2, 'Plastic Plate', 45, day3),
        (2, 'Thermocol Plate', 15, day3),
        (2, 'Plastic Spoon', 35, day3),
        (2, 'Carry Bag Plastic', 28, day3),
        (2, 'Straw Plastic', 40, day3),
        (2, 'Plastic Bottle', 12, day3),

        # Day 4 - 26 Apr - ~580
        (2, 'Plastic Cup', 70, day4),
        (2, 'Plastic Plate', 55, day4),
        (2, 'Thermocol Plate', 18, day4),
        (2, 'Plastic Spoon', 40, day4),
        (2, 'Carry Bag Plastic', 32, day4),
        (2, 'Straw Plastic', 45, day4),
        (2, 'Plastic Bottle', 15, day4),
        (2, 'Food Packaging Plastic', 10, day4),

        # Day 5 - 27 Apr - ~670
        (2, 'Plastic Cup', 80, day5),
        (2, 'Plastic Plate', 65, day5),
        (2, 'Thermocol Plate', 22, day5),
        (2, 'Plastic Spoon', 45, day5),
        (2, 'Carry Bag Plastic', 38, day5),
        (2, 'Straw Plastic', 52, day5),
        (2, 'Plastic Bottle', 18, day5),
        (2, 'Food Packaging Plastic', 15, day5),

        # Day 6 - 28 Apr (today) - ~780
        (2, 'Plastic Cup', 95, day6),
        (2, 'Plastic Plate', 75, day6),
        (2, 'Thermocol Plate', 28, day6),
        (2, 'Plastic Spoon', 52, day6),
        (2, 'Carry Bag Plastic', 44, day6),
        (2, 'Straw Plastic', 58, day6),
        (2, 'Plastic Bottle', 20, day6),
        (2, 'Food Packaging Plastic', 22, day6),
    ]

    # ─────────────────────────────────────────
    # VENDOR 2 - Canteen 2 - DECREASING TREND
    # Scores: 750 → 630 → 520 → 420 → 320 → 220
    # Recommendation: Excellent vendor
    # ─────────────────────────────────────────
    vendor2_sales = [
        # Day 1 - 23 Apr - ~750
        (3, 'Plastic Cup', 95, day1),
        (3, 'Plastic Plate', 75, day1),
        (3, 'Thermocol Plate', 25, day1),
        (3, 'Plastic Spoon', 55, day1),
        (3, 'Carry Bag Plastic', 42, day1),
        (3, 'Straw Plastic', 58, day1),
        (3, 'Plastic Bottle', 20, day1),

        # Day 2 - 24 Apr - ~630
        (3, 'Plastic Cup', 75, day2),
        (3, 'Plastic Plate', 55, day2),
        (3, 'Thermocol Plate', 15, day2),
        (3, 'Plastic Spoon', 40, day2),
        (3, 'Carry Bag Plastic', 30, day2),
        (3, 'Straw Plastic', 45, day2),
        (3, 'Plastic Bottle', 15, day2),
        (3, 'Paper Plate', 20, day2),

        # Day 3 - 25 Apr - ~520
        (3, 'Plastic Cup', 55, day3),
        (3, 'Paper Plate', 55, day3),
        (3, 'Plastic Spoon', 30, day3),
        (3, 'Carry Bag Plastic', 22, day3),
        (3, 'Straw Paper', 45, day3),
        (3, 'Food Packaging Paper', 28, day3),
        (3, 'Paper Cup', 30, day3),

        # Day 4 - 26 Apr - ~420
        (3, 'Paper Cup', 60, day4),
        (3, 'Paper Plate', 60, day4),
        (3, 'Wooden Spoon', 35, day4),
        (3, 'Carry Bag Cloth', 20, day4),
        (3, 'Straw Paper', 50, day4),
        (3, 'Food Packaging Paper', 30, day4),
        (3, 'Plastic Cup', 20, day4),

        # Day 5 - 27 Apr - ~320
        (3, 'Paper Cup', 75, day5),
        (3, 'Paper Plate', 65, day5),
        (3, 'Wooden Spoon', 45, day5),
        (3, 'Carry Bag Cloth', 30, day5),
        (3, 'Straw Paper', 58, day5),
        (3, 'Food Packaging Paper', 35, day5),
        (3, 'Reusable Container', 15, day5),

        # Day 6 - 28 Apr (today) - ~220
        (3, 'Paper Cup', 85, day6),
        (3, 'Paper Plate', 75, day6),
        (3, 'Wooden Spoon', 55, day6),
        (3, 'Carry Bag Cloth', 40, day6),
        (3, 'Straw Paper', 65, day6),
        (3, 'Reusable Container', 25, day6),
        (3, 'Food Packaging Paper', 40, day6),
    ]

    # ─────────────────────────────────────────
    # VENDOR 3 - Canteen 3 - STABLE TREND
    # Scores: 460 → 480 → 455 → 475 → 465 → 470
    # Recommendation: Stable performance
    # ─────────────────────────────────────────
    vendor3_sales = [
        # Day 1 - 23 Apr - ~460
        (4, 'Plastic Cup', 48, day1),
        (4, 'Paper Plate', 48, day1),
        (4, 'Plastic Spoon', 28, day1),
        (4, 'Carry Bag Plastic', 18, day1),
        (4, 'Straw Plastic', 32, day1),
        (4, 'Food Packaging Paper', 22, day1),

        # Day 2 - 24 Apr - ~480
        (4, 'Plastic Cup', 52, day2),
        (4, 'Paper Plate', 52, day2),
        (4, 'Plastic Spoon', 30, day2),
        (4, 'Carry Bag Plastic', 20, day2),
        (4, 'Straw Plastic', 35, day2),
        (4, 'Food Packaging Paper', 25, day2),

        # Day 3 - 25 Apr - ~455
        (4, 'Plastic Cup', 46, day3),
        (4, 'Paper Plate', 46, day3),
        (4, 'Plastic Spoon', 27, day3),
        (4, 'Carry Bag Plastic', 17, day3),
        (4, 'Straw Plastic', 30, day3),
        (4, 'Food Packaging Paper', 20, day3),

        # Day 4 - 26 Apr - ~475
        (4, 'Plastic Cup', 50, day4),
        (4, 'Paper Plate', 50, day4),
        (4, 'Plastic Spoon', 29, day4),
        (4, 'Carry Bag Plastic', 19, day4),
        (4, 'Straw Plastic', 33, day4),
        (4, 'Food Packaging Paper', 24, day4),

        # Day 5 - 27 Apr - ~465
        (4, 'Plastic Cup', 49, day5),
        (4, 'Paper Plate', 49, day5),
        (4, 'Plastic Spoon', 28, day5),
        (4, 'Carry Bag Plastic', 18, day5),
        (4, 'Straw Plastic', 31, day5),
        (4, 'Food Packaging Paper', 22, day5),

        # Day 6 - 28 Apr (today) - ~470
        (4, 'Plastic Cup', 50, day6),
        (4, 'Paper Plate', 50, day6),
        (4, 'Plastic Spoon', 29, day6),
        (4, 'Carry Bag Plastic', 19, day6),
        (4, 'Straw Plastic', 32, day6),
        (4, 'Food Packaging Paper', 23, day6),
    ]

    # ─────────────────────────────────────────
    # INSERT ALL SALES
    # ─────────────────────────────────────────
    all_sales = vendor1_sales + vendor2_sales + vendor3_sales

    for vendor_id, product_name, quantity, sale_date in all_sales:
        product = get_product(product_name)
        if product:
            sale = sales_data(
                vendor_id=vendor_id,
                product_id=product.product_id,
                quantity=quantity,
                sales_date=sale_date
            )
            db.session.add(sale)
        else:
            print(f"❌ Product not found: {product_name}")

    db.session.commit()
    print("Sales inserted!")

    # ─────────────────────────────────────────
    # CALCULATE AND INSERT DAILY EMISSIONS
    # ─────────────────────────────────────────
    all_vendor_ids = [2, 3, 4]
    all_dates = [day1, day2, day3, day4, day5, day6]

    for vendor_id in all_vendor_ids:
        for sale_date in all_dates:
            sales = sales_data.query.filter_by(
                vendor_id=vendor_id,
                sales_date=sale_date
            ).all()

            if not sales:
                continue

            total_co2 = 0
            for sale in sales:
                product = products.query.get(sale.product_id)
                if product:
                    total_co2 += product.emission_factor * sale.quantity

            emission = daily_emissions(
                vendor_id=vendor_id,
                total_co2=Decimal(str(round(total_co2, 2))),
                sales_date=sale_date
            )
            db.session.add(emission)

    db.session.commit()
    print("Daily emissions inserted!")

    # ─────────────────────────────────────────
    # VERIFY
    # ─────────────────────────────────────────
    print("\n--- VERIFICATION ---")
    vendor_names = {2: "Canteen 1", 3: "Canteen 2", 4: "Canteen 3"}
    for vendor_id in all_vendor_ids:
        print(f"\n{vendor_names[vendor_id]}:")
        emissions = daily_emissions.query.filter_by(
            vendor_id=vendor_id
        ).order_by(daily_emissions.sales_date).all()
        for e in emissions:
            print(f"  {e.sales_date} → CO₂ Score: {e.total_co2}")

    print("\nDone! All data inserted successfully!")
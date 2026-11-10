import csv
import random
from datetime import date, timedelta

random.seed(42)

countries=["Germany", "France", "Spain", "Italy", "Poland", "germany", "FRANCE", "sPAIN"]
categories=["Electronics", "Clothing", "Food", "", "Electronics"]
products=["Widget", "Gadget", "Gizmo", "Doohickey"]

rows=[]
start=date(2024, 1,1)

for i in range(1, 501):
    order_date=start+timedelta(days=random.randint(0,364))
    rows.append({
        "order_id": i,
        "order_date": order_date.isoformat(),
        "customer":f"customer_{random.randint(1,50)}",
        "country": random.choice(countries),
        "category": random.choice(categories),
        "product": random.choice(products),
        "quantity": random.randint(1,100),
        "unit_price": round(random.uniform(5,200),2),
    })

rows.extend([dict(r) for r in random.sample(rows,20)])

for r in random.sample(rows,15):
    r["unit_price"] = ""

random.shuffle(rows)

with open("data/raw/sales.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Done: {len(rows)} rows was wrote to data/raw/sales.csv")

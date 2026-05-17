import pandas as pd
import numpy as np
from faker import Faker
import random
import datetime

# Initialize Faker and Seed
fake = Faker()
random.seed(42)

# PART 1: Generate 100 Companies
customers = []
for _ in range(100):
    customers.append({
        "customer_id": f"CUST-{1000 + _}",
        "company_name": fake.company(),
        "industry": random.choice(["Tech", "Manufacturing", "Retail", "Healthcare", "Logistics"]),
        "credit_limit": random.randint(10000, 150000),
        "years_in_business": random.randint(1, 15)
    })
df_customers = pd.DataFrame(customers)

# PART 2: Generate 2,500 Invoices
invoices = []
start_date = datetime.date(2025, 1, 1)

for i in range(2500):
    cust = df_customers.sample(1).iloc[0]
    issue_date = start_date + datetime.timedelta(days=random.randint(0, 480))
    due_date = issue_date + datetime.timedelta(days=30)
    
    # Risk Simulation: Rigging the data so Retail is riskier
    if cust['industry'] == "Retail":
        days_late = random.choices([-5, 0, 20, 50, 100], weights=[5, 10, 30, 35, 20])[0]
    elif cust['industry'] == "Manufacturing":
        days_late = random.choices([-10, 0, 5, 15], weights=[20, 60, 15, 5])[0]
    else:
        days_late = random.choices([-2, 0, 10, 95], weights=[15, 60, 20, 5])[0]

    is_default = 1 if days_late > 90 else 0
    
    invoices.append({
        "invoice_id": f"INV-{50000 + i}",
        "customer_id": cust['customer_id'],
        "invoice_amount": random.randint(1000, 20000),
        "issue_date": issue_date,
        "due_date": due_date,
        "days_late": days_late,
        "is_default": is_default
    })

df_invoices = pd.DataFrame(invoices)
df_master = pd.merge(df_invoices, df_customers, on="customer_id")

# Save as the raw ledger
df_master.to_csv("b2b_ledger.csv", index=False)
print("✅ Success! 'b2b_ledger.csv' created with 2,500 records.")
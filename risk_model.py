import pandas as pd

# 1. Load the raw ledger you created in the last step
try:
    df = pd.read_csv("b2b_ledger.csv")
    print("📖 Successfully loaded b2b_ledger.csv")
except FileNotFoundError:
    print("❌ Error: b2b_ledger.csv not found! Run data_engine.py first.")

# 2. Group by Customer to calculate their habits
# We are turning 2,500 individual invoices into 100 customer summaries
customer_behavior = df.groupby(['customer_id', 'company_name', 'industry']).agg({
    'days_late': 'mean',        # Avg days late
    'invoice_amount': 'sum',    # Total money owed
    'is_default': 'sum'         # Total times they defaulted
}).reset_index()

# 3. The Risk Logic (Our Custom Algorithm)
# We start every company at 100 points and deduct for 'Bad Behavior'
def calculate_credit_score(row):
    score = 100
    
    # Penalty 1: Deduct points for being late on average
    if row['days_late'] > 0:
        score -= (row['days_late'] * 1.5)
        
    # Penalty 2: Massive deduction for any past default (>90 days late)
    if row['is_default'] > 0:
        score -= 40
        
    # Penalty 3: Industry risk multiplier
    if row['industry'] == "Retail":
        score -= 10
        
    return max(0, min(100, score)) # Keep score between 0 and 100

# Apply the math to every row
customer_behavior['credit_score'] = customer_behavior.apply(calculate_credit_score, axis=1)

# 4. SAVE THE NEW FILE
customer_behavior.to_csv("processed_risk_data.csv", index=False)

print("✅ SUCCESS: 'processed_risk_data.csv' has been created!")
print(customer_behavior[['company_name', 'credit_score']].head())
import pandas as pd

# Define the 'Normal' market behavior for 2025
benchmark_data = {
    'industry': ['Retail', 'Manufacturing', 'Tech', 'Healthcare', 'Construction'],
    'market_avg_delay': [15, 5, 3, 2, 25],  # Average days people pay late in these sectors
    'industry_risk_index': [0.8, 0.2, 0.3, 0.1, 0.9] # 0 to 1 riskiness scale
}

bench_df = pd.DataFrame(benchmark_data)
bench_df.to_csv("industry_benchmarks.csv", index=False)
print("✅ industry_benchmarks.csv created successfully!")
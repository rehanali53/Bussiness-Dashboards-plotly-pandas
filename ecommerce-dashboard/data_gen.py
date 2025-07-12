import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for consistent results
np.random.seed(42)
random.seed(42)

# Generate monthly sales data for 2024 and 2025
months_2024 = pd.date_range('2024-01-01', '2024-12-01', freq='M')
months_2025 = pd.date_range('2025-01-01', '2025-12-01', freq='M')

# Regions and their characteristics
regions = {
    'North America': {'base_sales': 150000, 'growth': 0.08},
    'Europe': {'base_sales': 120000, 'growth': 0.12},
    'Asia Pacific': {'base_sales': 180000, 'growth': 0.15},
    'Latin America': {'base_sales': 80000, 'growth': 0.10},
    'Middle East': {'base_sales': 60000, 'growth': 0.07}
}

# Product categories
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty']

# Create monthly sales data
monthly_sales = []

for year in [2024, 2025]:
    months = months_2024 if year == 2024 else months_2025
    
    for month in months:
        for region_name, region_info in regions.items():
            base = region_info['base_sales']
            growth = region_info['growth'] if year == 2025 else 0
            
            # Add seasonal effects
            seasonal_boost = 1.0
            if month.month in [11, 12]:  # Holiday season
                seasonal_boost = 1.3
            elif month.month in [6, 7, 8]:  # Summer season
                seasonal_boost = 1.1
            
            # Calculate sales with growth and random variation
            monthly_revenue = base * (1 + growth) * seasonal_boost * np.random.uniform(0.85, 1.15)
            orders = int(monthly_revenue / np.random.uniform(45, 85))
            
            monthly_sales.append({
                'date': month,
                'year': year,
                'month': month.month,
                'region': region_name,
                'revenue': round(monthly_revenue, 2),
                'orders': orders,
                'avg_order_value': round(monthly_revenue / orders, 2)
            })

# Create regional performance data
regional_data = []
for region_name, region_info in regions.items():
    # Calculate 2025 vs 2024 performance
    total_2024 = sum([row['revenue'] for row in monthly_sales if row['region'] == region_name and row['year'] == 2024])
    total_2025 = sum([row['revenue'] for row in monthly_sales if row['region'] == region_name and row['year'] == 2025])
    
    growth_rate = ((total_2025 - total_2024) / total_2024) * 100
    
    regional_data.append({
        'region': region_name,
        'revenue_2024': total_2024,
        'revenue_2025': total_2025,
        'growth_rate': round(growth_rate, 1),
        'market_share_2025': round((total_2025 / sum([row['revenue'] for row in monthly_sales if row['year'] == 2025])) * 100, 1)
    })

# Create product category data
category_sales = []
for category in categories:
    for year in [2024, 2025]:
        # Base sales vary by category
        base_sales = {
            'Electronics': 180000,
            'Clothing': 120000,
            'Home & Garden': 90000,
            'Sports': 75000,
            'Books': 45000,
            'Beauty': 85000
        }
        
        annual_revenue = base_sales[category] * 12
        if year == 2025:
            growth_rates = {
                'Electronics': 0.18,
                'Clothing': 0.08,
                'Home & Garden': 0.12,
                'Sports': 0.15,
                'Books': 0.05,
                'Beauty': 0.22
            }
            annual_revenue *= (1 + growth_rates[category])
        
        # Add random variation
        annual_revenue *= np.random.uniform(0.9, 1.1)
        
        category_sales.append({
            'category': category,
            'year': year,
            'revenue': round(annual_revenue, 2),
            'units_sold': int(annual_revenue / np.random.uniform(25, 150))
        })

# Create customer acquisition data
customer_data = []
months_all = list(months_2024) + list(months_2025)

for month in months_all:
    year = month.year
    base_customers = 2500
    
    # Growth in customer acquisition
    if year == 2025:
        base_customers *= 1.25
    
    # Seasonal effects
    seasonal_multiplier = 1.0
    if month.month in [11, 12]:
        seasonal_multiplier = 1.4
    elif month.month in [1, 2]:
        seasonal_multiplier = 0.8
    
    new_customers = int(base_customers * seasonal_multiplier * np.random.uniform(0.85, 1.15))
    retention_rate = np.random.uniform(0.82, 0.88)
    
    customer_data.append({
        'date': month,
        'year': year,
        'month': month.month,
        'new_customers': new_customers,
        'retention_rate': round(retention_rate * 100, 1),
        'total_active_customers': new_customers + int(base_customers * 8 * retention_rate)
    })

# Save all data to CSV files
monthly_sales_df = pd.DataFrame(monthly_sales)
regional_performance_df = pd.DataFrame(regional_data)
category_performance_df = pd.DataFrame(category_sales)
customer_metrics_df = pd.DataFrame(customer_data)

# Create datasets folder
import os
os.makedirs('ecommerce-dashboard/datasets', exist_ok=True)

monthly_sales_df.to_csv('ecommerce-dashboard/datasets/monthly_sales_data.csv', index=False)
regional_performance_df.to_csv('ecommerce-dashboard/datasets/regional_performance.csv', index=False)
category_performance_df.to_csv('ecommerce-dashboard/datasets/category_sales.csv', index=False)
customer_metrics_df.to_csv('ecommerce-dashboard/datasets/customer_metrics.csv', index=False)

print("E-commerce data files created successfully!")
print("Files generated in datasets/ folder:")
print("1. monthly_sales_data.csv - Monthly sales by region (2024-2025)")
print("2. regional_performance.csv - Regional comparison data (2024-2025)")
print("3. category_sales.csv - Product category performance (2024-2025)")
print("4. customer_metrics.csv - Customer acquisition and retention (2024-2025)")

print(f"\nSample data preview:")
print(f"Total records in monthly_sales_data.csv: {len(monthly_sales_df)}")
print(f"Total records in regional_performance.csv: {len(regional_performance_df)}")
print(f"Total records in category_sales.csv: {len(category_performance_df)}")
print(f"Total records in customer_metrics.csv: {len(customer_metrics_df)}")

print(f"\nYears covered: 2024 and 2025")
print(f"Regions: {list(regions.keys())}")
print(f"Product categories: {categories}")
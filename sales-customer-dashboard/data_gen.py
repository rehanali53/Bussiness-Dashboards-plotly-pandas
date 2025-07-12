import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for consistent results
np.random.seed(42)
random.seed(42)

# Generate sales data for 2023
months_2023 = pd.date_range('2023-01-01', '2023-12-31', freq='D')

# Customer information
customers = [
    {'customer_id': 'C001', 'customer_name': 'PrimeCore Innovations', 'customer_group': 'NEW'},
    {'customer_id': 'C002', 'customer_name': 'ClearWater Tech', 'customer_group': 'REGULAR'},
    {'customer_id': 'C003', 'customer_name': 'Silverline Industries', 'customer_group': 'NEW'},
    {'customer_id': 'C004', 'customer_name': 'AquaVita Industries', 'customer_group': 'VIP'},
    {'customer_id': 'C005', 'customer_name': 'NutriMax Solutions', 'customer_group': 'REGULAR'},
    {'customer_id': 'C006', 'customer_name': 'FreshFarm Products', 'customer_group': 'VIP'},
    {'customer_id': 'C007', 'customer_name': 'HealthCore Systems', 'customer_group': 'REGULAR'},
    {'customer_id': 'C008', 'customer_name': 'VitalLife Corp', 'customer_group': 'SENSITIVE'},
    {'customer_id': 'C009', 'customer_name': 'GreenLeaf Enterprises', 'customer_group': 'VIP'},
    {'customer_id': 'C010', 'customer_name': 'PureFit Industries', 'customer_group': 'NEW'}
]

# Add more customers to reach 50 total
for i in range(11, 51):
    group = np.random.choice(['NEW', 'REGULAR', 'VIP', 'SENSITIVE'], p=[0.22, 0.38, 0.35, 0.05])
    customers.append({
        'customer_id': f'C{i:03d}',
        'customer_name': f'Company {i}',
        'customer_group': group
    })

# Product categories and groups
products = [
    {'product_id': 'P001', 'product_name': 'Organic Juice', 'product_group': 'Food and Beverages'},
    {'product_id': 'P002', 'product_name': 'Protein Powder', 'product_group': 'Nutrition Supplements'},
    {'product_id': 'P003', 'product_name': 'Vitamin D3', 'product_group': 'Nutrition Supplements'},
    {'product_id': 'P004', 'product_name': 'Sports Drinks', 'product_group': 'Food and Beverages'},
    {'product_id': 'P005', 'product_name': 'Fitness Equipment', 'product_group': 'Fitness and Exercise Equipment'},
    {'product_id': 'P006', 'product_name': 'Wellness Kit', 'product_group': 'Personal Care and Wellness Products'},
    {'product_id': 'P007', 'product_name': 'Energy Bars', 'product_group': 'Food and Beverages'},
    {'product_id': 'P008', 'product_name': 'Yoga Mat', 'product_group': 'Fitness and Exercise Equipment'},
    {'product_id': 'P009', 'product_name': 'Skincare Set', 'product_group': 'Personal Care and Wellness Products'},
    {'product_id': 'P010', 'product_name': 'Multivitamins', 'product_group': 'Nutrition Supplements'}
]

# Generate invoice/sales data
sales_data = []
invoice_number = 1001

# Create sales throughout 2023
for month in range(1, 13):
    # Generate 60-65 invoices per month to reach ~750 total
    monthly_invoices = random.randint(60, 65)
    
    for _ in range(monthly_invoices):
        # Random date in the month
        day = random.randint(1, 28)  # Safe day for all months
        invoice_date = datetime(2023, month, day)
        
        # Select random customer and product
        customer = random.choice(customers)
        product = random.choice(products)
        
        # Generate invoice amount based on customer group
        base_amount = random.uniform(5000, 30000)
        if customer['customer_group'] == 'VIP':
            invoice_amount = base_amount * random.uniform(1.5, 2.5)
        elif customer['customer_group'] == 'REGULAR':
            invoice_amount = base_amount * random.uniform(1.0, 1.8)
        elif customer['customer_group'] == 'NEW':
            invoice_amount = base_amount * random.uniform(0.8, 1.3)
        else:  # SENSITIVE
            invoice_amount = base_amount * random.uniform(0.5, 1.0)
        
        # Generate quantity and unit price
        quantity = random.randint(1, 10)
        unit_price = invoice_amount / quantity
        
        sales_data.append({
            'invoice_id': f'INV{invoice_number:04d}',
            'invoice_date': invoice_date,
            'month': month,
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_group': customer['customer_group'],
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'product_group': product['product_group'],
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'invoice_amount': round(invoice_amount, 2)
        })
        
        invoice_number += 1

# Create monthly aggregated data
monthly_sales = []
for month in range(1, 13):
    month_data = [sale for sale in sales_data if sale['month'] == month]
    total_sales = sum([sale['invoice_amount'] for sale in month_data])
    invoice_count = len(month_data)
    
    # Generate previous year data for comparison (slightly lower)
    prev_year_sales = total_sales * random.uniform(0.85, 0.95)
    
    monthly_sales.append({
        'month': month,
        'month_name': datetime(2023, month, 1).strftime('%b'),
        'year': 2023,
        'total_sales': round(total_sales, 2),
        'total_sales_previous': round(prev_year_sales, 2),
        'invoice_count': invoice_count,
        'avg_invoice_amount': round(total_sales / invoice_count, 2) if invoice_count > 0 else 0
    })

# Create customer summary data
customer_summary = []
for customer in customers:
    customer_sales = [sale for sale in sales_data if sale['customer_id'] == customer['customer_id']]
    if customer_sales:
        total_amount = sum([sale['invoice_amount'] for sale in customer_sales])
        total_purchases = len(customer_sales)
        avg_purchase = total_amount / total_purchases if total_purchases > 0 else 0
        
        customer_summary.append({
            'customer_id': customer['customer_id'],
            'customer_name': customer['customer_name'],
            'customer_group': customer['customer_group'],
            'total_sales': round(total_amount, 2),
            'total_purchases': total_purchases,
            'avg_purchase_amount': round(avg_purchase, 2)
        })

# Create product group summary
product_groups = ['Food and Beverages', 'Nutrition Supplements', 'Fitness and Exercise Equipment', 'Personal Care and Wellness Products']
product_summary = []

for group in product_groups:
    group_sales = [sale for sale in sales_data if sale['product_group'] == group]
    total_amount = sum([sale['invoice_amount'] for sale in group_sales])
    
    product_summary.append({
        'product_group': group,
        'total_sales': round(total_amount, 2),
        'percentage': 0  # Will calculate after creating dataframe
    })

# Convert to DataFrames
sales_df = pd.DataFrame(sales_data)
monthly_df = pd.DataFrame(monthly_sales)
customer_df = pd.DataFrame(customer_summary)
product_df = pd.DataFrame(product_summary)

# Calculate product group percentages
total_sales_amount = sales_df['invoice_amount'].sum()
product_df['percentage'] = round((product_df['total_sales'] / total_sales_amount) * 100, 2)

# Create datasets folder
import os
os.makedirs('sales-customer-dashboard/datasets', exist_ok=True)

# Save to CSV files
sales_df.to_csv('sales-customer-dashboard/datasets/sales_transactions.csv', index=False)
monthly_df.to_csv('sales-customer-dashboard/datasets/monthly_sales_summary.csv', index=False)
customer_df.to_csv('sales-customer-dashboard/datasets/customer_summary.csv', index=False)
product_df.to_csv('sales-customer-dashboard/datasets/product_group_summary.csv', index=False)

print("Sales dashboard data created successfully!")
print("Files generated in datasets/ folder:")
print("1. sales_transactions.csv - Individual sales transactions")
print("2. monthly_sales_summary.csv - Monthly aggregated data")
print("3. customer_summary.csv - Customer profiling data")
print("4. product_group_summary.csv - Product group analysis")

print(f"\nData Summary:")
print(f"Total Sales Amount: ${total_sales_amount:,.0f}")
print(f"Total Invoices: {len(sales_df)}")
print(f"Average Invoice Amount: ${sales_df['invoice_amount'].mean():,.0f}")
print(f"Total Customers: {len(customer_df)}")
print(f"Date Range: 2023-01-01 to 2023-12-31")

# Show sample data
print(f"\nSample records:")
print(f"Sales transactions: {len(sales_df)} rows")
print(f"Monthly summary: {len(monthly_df)} rows")
print(f"Customer summary: {len(customer_df)} rows")
print(f"Product groups: {len(product_df)} rows")
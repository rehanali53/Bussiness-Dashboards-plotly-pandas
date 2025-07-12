import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Load the generated data from datasets folder
sales_df = pd.read_csv('sales-customer-dashboard/datasets/sales_transactions.csv')
monthly_df = pd.read_csv('sales-customer-dashboard/datasets/monthly_sales_summary.csv')
customer_df = pd.read_csv('sales-customer-dashboard/datasets/customer_summary.csv')
product_df = pd.read_csv('sales-customer-dashboard/datasets/product_group_summary.csv')

# Convert date columns
sales_df['invoice_date'] = pd.to_datetime(sales_df['invoice_date'])

# Calculate key metrics for the header cards
total_sales = sales_df['invoice_amount'].sum()
total_invoices = len(sales_df)
avg_invoice_amount = sales_df['invoice_amount'].mean()
total_customers = len(customer_df)

# Create the dashboard with multiple subplots
fig = make_subplots(
    rows=4, cols=4,
    subplot_titles=[
        'Key Metrics', '', '', '',
        'Total Sales ($) Over Time', '', '', '',
        'Sales vs Purchases by Customer', '', 'Product Group Sales', '',
        'Customer Group Distribution', '', '', ''
    ],
    specs=[
        [{"colspan": 4}, None, None, None],
        [{"colspan": 4, "secondary_y": True}, None, None, None],
        [{"colspan": 2}, None, {"type": "pie"}, None],
        [{"type": "pie"}, None, {"colspan": 2}, None]
    ],
    vertical_spacing=0.08,
    horizontal_spacing=0.1,
    row_heights=[0.15, 0.35, 0.35, 0.15]
)

# 1. Key Metrics Cards (Top Row) - Using annotations instead of traces
metrics_annotations = [
    dict(x=0.125, y=0.95, xref='paper', yref='paper',
         text=f'<b>${total_sales/1000000:.2f}M</b><br>Sum of Invoices',
         showarrow=False, font=dict(size=16, color='white'),
         bgcolor='rgba(52, 73, 94, 0.8)', bordercolor='white', borderwidth=2,
         xanchor='center', yanchor='middle'),
    dict(x=0.375, y=0.95, xref='paper', yref='paper',
         text=f'<b>{total_invoices}</b><br>Count of Invoices',
         showarrow=False, font=dict(size=16, color='white'),
         bgcolor='rgba(52, 73, 94, 0.8)', bordercolor='white', borderwidth=2,
         xanchor='center', yanchor='middle'),
    dict(x=0.625, y=0.95, xref='paper', yref='paper',
         text=f'<b>${avg_invoice_amount/1000:.1f}K</b><br>Average Invoice Amount',
         showarrow=False, font=dict(size=16, color='white'),
         bgcolor='rgba(52, 73, 94, 0.8)', bordercolor='white', borderwidth=2,
         xanchor='center', yanchor='middle'),
    dict(x=0.875, y=0.95, xref='paper', yref='paper',
         text=f'<b>{total_customers}</b><br>Customer Count',
         showarrow=False, font=dict(size=16, color='white'),
         bgcolor='rgba(52, 73, 94, 0.8)', bordercolor='white', borderwidth=2,
         xanchor='center', yanchor='middle')
]

# 2. Monthly Sales Trends (Second Row)
# Current year sales
fig.add_trace(
    go.Bar(
        x=monthly_df['month_name'],
        y=monthly_df['total_sales'],
        name='2023 Sales',
        marker=dict(color='#ff7f0e'),
        text=[f'${x/1000:.0f}K' for x in monthly_df['total_sales']],
        textposition='outside',
        hovertemplate='%{x}<br>2023 Sales: $%{y:,.0f}<extra></extra>'
    ),
    row=2, col=1
)

# Previous year sales (comparison)
fig.add_trace(
    go.Bar(
        x=monthly_df['month_name'],
        y=monthly_df['total_sales_previous'],
        name='2022 Sales (Previous)',
        marker=dict(color='rgba(52, 73, 94, 0.7)'),
        hovertemplate='%{x}<br>2022 Sales: $%{y:,.0f}<extra></extra>'
    ),
    row=2, col=1
)

# 3. Customer Analysis Scatter Plot (Bottom Left)
# Prepare data for scatter plot
scatter_data = customer_df.copy()
colors = {'NEW': '#2ecc71', 'REGULAR': '#3498db', 'VIP': '#e74c3c', 'SENSITIVE': '#f39c12'}

for group in scatter_data['customer_group'].unique():
    group_data = scatter_data[scatter_data['customer_group'] == group]
    
    fig.add_trace(
        go.Scatter(
            x=group_data['total_purchases'],
            y=group_data['total_sales'],
            mode='markers',
            name=group,
            marker=dict(
                size=12,
                color=colors.get(group, '#95a5a6'),
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=group_data['customer_name'],
            hovertemplate='%{text}<br>Purchases: %{x}<br>Sales: $%{y:,.0f}<br>Group: ' + group + '<extra></extra>'
        ),
        row=3, col=1
    )

# 4. Product Group Pie Chart (Middle Right)
fig.add_trace(
    go.Pie(
        labels=product_df['product_group'],
        values=product_df['total_sales'],
        hole=0.4,
        marker=dict(colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='%{label}<br>Sales: $%{value:,.0f}<br>%{percent}<extra></extra>'
    ),
    row=3, col=3
)

# 5. Customer Group Distribution (Bottom Left)
customer_group_counts = customer_df['customer_group'].value_counts()
customer_group_sales = customer_df.groupby('customer_group')['total_sales'].sum()

fig.add_trace(
    go.Pie(
        labels=customer_group_counts.index,
        values=customer_group_sales.values,
        hole=0.4,
        marker=dict(colors=['#3498db', '#e74c3c', '#2ecc71', '#f39c12']),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='%{label}<br>Sales: $%{value:,.0f}<br>%{percent}<extra></extra>'
    ),
    row=4, col=1
)


# 6. Customer Details Table (Bottom Right)
# Create a simple table using annotations
table_data = customer_df.nlargest(8, 'total_sales')[['customer_group', 'customer_name', 'total_sales']]
table_y = 0.25
table_annotations = []

# Table header
table_annotations.append(
    dict(x=0.75, y=table_y + 0.08, xref='paper', yref='paper',
         text='<b>Top Customers by Sales</b>',
         showarrow=False, font=dict(size=14, color='#2c3e50'),
         xanchor='center')
)

# Table rows
for i, (_, row) in enumerate(table_data.iterrows()):
    y_pos = table_y - (i * 0.02)
    table_annotations.append(
        dict(x=0.75, y=y_pos, xref='paper', yref='paper',
             text=f'{row["customer_group"]} | {row["customer_name"][:20]} | ${row["total_sales"]:,.0f}',
             showarrow=False, font=dict(size=10, color='#34495e'),
             xanchor='center')
    )

# Update layout and axes
fig.update_xaxes(title_text="Month", row=2, col=1)
fig.update_yaxes(title_text="Sales Amount ($)", row=2, col=1)

fig.update_xaxes(title_text="Number of Purchases", row=3, col=1)
fig.update_yaxes(title_text="Total Sales ($)", row=3, col=1)

# Format y-axis for sales
fig.update_yaxes(tickformat="$,.0s", row=2, col=1)
fig.update_yaxes(tickformat="$,.0s", row=3, col=1)

# Update overall layout
fig.update_layout(
    title={
        'text': "Sales Customer Profiling Dashboard - 2023",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28, 'color': '#2c3e50'}
    },
    height=1000,
    showlegend=True,
    template='plotly_white',
    font=dict(family="Arial, sans-serif", size=11),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    annotations=metrics_annotations + table_annotations
)

# Add background colors for sections
fig.add_shape(
    type="rect",
    x0=0, y0=0.92, x1=1, y1=0.98,
    xref="paper", yref="paper",
    fillcolor="rgba(52, 73, 94, 0.1)",
    layer="below",
    line_width=0,
)

# Export to HTML
fig.write_html("sales-customer-dashboard/sales_customer_profiling_dashboard.html")

print("Sales Customer Profiling Dashboard created successfully!")
print("\nDashboard Features:")
print("- Key business metrics display")
print("- Monthly sales trends with year-over-year comparison")
print("- Customer purchase behavior analysis")
print("- Product group performance breakdown")
print("- Customer segmentation visualization")
print("- Top customer details summary")
print("\nHTML file saved as: sales_customer_profiling_dashboard.html")

# Print summary statistics
print(f"\nBusiness Summary:")
print(f"Total Sales: ${total_sales:,.0f}")
print(f"Total Invoices: {total_invoices:,}")
print(f"Average Invoice: ${avg_invoice_amount:,.0f}")
print(f"Total Customers: {total_customers}")
print(f"Top Product Group: {product_df.loc[product_df['total_sales'].idxmax(), 'product_group']}")
print(f"Largest Customer Group: {customer_group_sales.idxmax()}")
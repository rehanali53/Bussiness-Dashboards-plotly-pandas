import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Load the generated data from datasets folder
monthly_sales = pd.read_csv('ecommerce-dashboard/datasets/monthly_sales_data.csv')
regional_performance = pd.read_csv('ecommerce-dashboard/datasets/regional_performance.csv')
category_sales = pd.read_csv('ecommerce-dashboard/datasets/category_sales.csv')
customer_metrics = pd.read_csv('ecommerce-dashboard/datasets/customer_metrics.csv')

# Convert date columns to datetime
monthly_sales['date'] = pd.to_datetime(monthly_sales['date'])
customer_metrics['date'] = pd.to_datetime(customer_metrics['date'])

# Create the main dashboard with multiple subplots
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=[
        'Monthly Revenue Trends (2024 vs 2025)',
        'Regional Market Share 2025',
        'Product Category Performance',
        'Regional Growth Comparison',
        'Customer Acquisition Trends',
        'Regional Revenue Map'
    ],
    specs=[
        [{"secondary_y": False}, {"type": "pie"}],
        [{"secondary_y": False}, {"secondary_y": False}],
        [{"secondary_y": True}, {"type": "geo"}]
    ],
    vertical_spacing=0.08,
    horizontal_spacing=0.1,
    row_heights=[0.35, 0.35, 0.3]
)

# 1. Monthly Revenue Trends Line Chart (Top Left)
revenue_2024 = monthly_sales[monthly_sales['year'] == 2024].groupby('date')['revenue'].sum().reset_index()
revenue_2025 = monthly_sales[monthly_sales['year'] == 2025].groupby('date')['revenue'].sum().reset_index()

fig.add_trace(
    go.Scatter(
        x=revenue_2024['date'],
        y=revenue_2024['revenue'],
        mode='lines+markers',
        name='2024 Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6),
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=revenue_2025['date'],
        y=revenue_2025['revenue'],
        mode='lines+markers',
        name='2025 Revenue',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6),
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ),
    row=1, col=1
)

# 2. Regional Market Share Pie Chart (Top Right)
market_share_data = regional_performance.sort_values('market_share_2025', ascending=False)

fig.add_trace(
    go.Pie(
        labels=market_share_data['region'],
        values=market_share_data['market_share_2025'],
        hole=0.4,
        marker=dict(colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']),
        textinfo='label+percent',
        hovertemplate='%{label}<br>Market Share: %{value}%<br>Revenue: $%{customdata:,.0f}<extra></extra>',
        customdata=market_share_data['revenue_2025']
    ),
    row=1, col=2
)

# 3. Product Category Performance Bar Chart (Middle Left)
category_2025 = category_sales[category_sales['year'] == 2025].sort_values('revenue', ascending=True)

fig.add_trace(
    go.Bar(
        x=category_2025['revenue'],
        y=category_2025['category'],
        orientation='h',
        name='Category Revenue 2025',
        marker=dict(color='#2ca02c'),
        text=[f'${x/1000000:.1f}M' for x in category_2025['revenue']],
        textposition='outside',
        hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>'
    ),
    row=2, col=1
)

# 4. Regional Growth Comparison Bar Chart (Middle Right)
regional_sorted = regional_performance.sort_values('growth_rate', ascending=True)

colors = ['#d62728' if x < 0 else '#2ca02c' for x in regional_sorted['growth_rate']]

fig.add_trace(
    go.Bar(
        x=regional_sorted['growth_rate'],
        y=regional_sorted['region'],
        orientation='h',
        name='Growth Rate %',
        marker=dict(color=colors),
        text=[f'{x}%' for x in regional_sorted['growth_rate']],
        textposition='outside',
        hovertemplate='%{y}<br>Growth Rate: %{x}%<extra></extra>'
    ),
    row=2, col=2
)

# 5. Customer Acquisition Trends (Bottom Left - with secondary y-axis)
customer_2025 = customer_metrics[customer_metrics['year'] == 2025]

fig.add_trace(
    go.Scatter(
        x=customer_2025['date'],
        y=customer_2025['new_customers'],
        mode='lines+markers',
        name='New Customers 2025',
        line=dict(color='#9467bd', width=2),
        yaxis='y5',
        hovertemplate='%{x}<br>New Customers: %{y:,.0f}<extra></extra>'
    ),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
        x=customer_2025['date'],
        y=customer_2025['retention_rate'],
        mode='lines+markers',
        name='Retention Rate %',
        line=dict(color='#8c564b', width=2),
        yaxis='y6',
        hovertemplate='%{x}<br>Retention: %{y}%<extra></extra>'
    ),
    row=3, col=1
)

# 6. Map visualization (Bottom Right) - Simulated regional data
region_coords = {
    'North America': {'lat': 45, 'lon': -100, 'size': 30},
    'Europe': {'lat': 50, 'lon': 10, 'size': 25},
    'Asia Pacific': {'lat': 35, 'lon': 120, 'size': 35},
    'Latin America': {'lat': -15, 'lon': -60, 'size': 20},
    'Middle East': {'lat': 25, 'lon': 45, 'size': 15}
}

map_data = []
for region in regional_performance.itertuples():
    region_name = str(region.region)  # Convert to string for type safety
    coords = region_coords[region_name]
    map_data.append({
        'region': region_name,
        'lat': coords['lat'],
        'lon': coords['lon'],
        'revenue': region.revenue_2025,
        'size': coords['size']
    })

map_df = pd.DataFrame(map_data)

fig.add_trace(
    go.Scattergeo(
        lat=map_df['lat'],
        lon=map_df['lon'],
        text=map_df['region'],
        mode='markers+text',
        marker=dict(
            size=map_df['size'],
            color=map_df['revenue'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Revenue ($)", x=1.02)
        ),
        textposition='middle center',
        hovertemplate='%{text}<br>Revenue: $%{customdata:,.0f}<extra></extra>',
        customdata=map_df['revenue'],
        name='Regional Revenue'
    ),
    row=3, col=2
)

# Update layout for each subplot
fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)

fig.update_xaxes(title_text="Revenue ($)", row=2, col=1)
fig.update_yaxes(title_text="Product Category", row=2, col=1)

fig.update_xaxes(title_text="Growth Rate (%)", row=2, col=2)
fig.update_yaxes(title_text="Region", row=2, col=2)

fig.update_xaxes(title_text="Date", row=3, col=1)
fig.update_yaxes(title_text="New Customers", row=3, col=1)

# Configure the map
fig.update_geos(
    projection_type="orthographic",
    showland=True,
    landcolor="lightgray",
    showocean=True,
    oceancolor="lightblue",
    row=3, col=2
)

# Update overall layout
fig.update_layout(
    title={
        'text': "E-commerce Business Performance Dashboard - 2024 vs 2025",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#2c3e50'}
    },
    height=1200,
    showlegend=True,
    template='plotly_white',
    font=dict(family="Arial, sans-serif", size=11),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    )
)

# Add secondary y-axis for customer metrics
fig.update_layout(
    yaxis5=dict(title="New Customers", side="left"),
    yaxis6=dict(title="Retention Rate (%)", side="right", overlaying="y5")
)

# Format axes
fig.update_yaxes(tickformat="$,.0f", row=1, col=1)
fig.update_xaxes(tickformat="$,.0s", row=2, col=1)

# Add annotations with key insights
annotations = [
    dict(
        x=0.02, y=0.98,
        xref='paper', yref='paper',
        text='<b>Key Insights:</b><br>• Asia Pacific leads with highest market share<br>• Beauty category shows strongest growth<br>• Overall revenue increased year-over-year',
        showarrow=False,
        font=dict(size=12, color='#34495e'),
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#bdc3c7',
        borderwidth=1,
        xanchor='left',
        yanchor='top'
    )
]

fig.update_layout(annotations=annotations)

# Export to HTML
fig.write_html("ecommerce_dashboard.html")

print("E-commerce Dashboard created successfully!")
print("\nDashboard Features:")
print("- Monthly revenue trends comparison (2024 vs 2025)")
print("- Regional market share visualization")
print("- Product category performance analysis")
print("- Regional growth rate comparison")
print("- Customer acquisition and retention metrics")
print("- Interactive geographic revenue mapping")
print("\nHTML file saved as: ecommerce_dashboard.html")

# Print some summary statistics
total_2024 = monthly_sales[monthly_sales['year'] == 2024]['revenue'].sum()
total_2025 = monthly_sales[monthly_sales['year'] == 2025]['revenue'].sum()
growth = ((total_2025 - total_2024) / total_2024) * 100

print(f"\nBusiness Summary:")
print(f"2024 Total Revenue: ${total_2024:,.0f}")
print(f"2025 Total Revenue: ${total_2025:,.0f}")
print(f"Year-over-Year Growth: {growth:.1f}%")
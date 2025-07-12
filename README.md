# Business Dashboards Portfolio

Welcome to my collection of interactive business dashboards! This project shows two different business stories using real-world data patterns and professional visualizations.

## 🎯 What's Inside

This portfolio contains **two complete dashboard projects**:

1. **E-commerce Performance Dashboard** - Shows online store sales trends
2. **Sales Customer Profiling Dashboard** - Analyzes customer buying patterns

Each dashboard tells a different business story and uses different types of charts and data.

## 📊 Live Dashboard Previews

### Dashboard 1: E-commerce Performance
**Business Question:** *"Show me how our online store is doing this year compared to last year and which regions are selling the most."*

**🔗 [View Live Dashboard](https://rehanali53.github.io/Business-Dashboards-Portfolio/ecommerce-dashboard/ecommerce_dashboard.html)**

**Key Features:**
- Monthly sales trends (2024 vs 2025)
- Regional market share analysis  
- Product category performance
- Customer acquisition metrics
- Interactive world map

**Data Overview:**
- 120 monthly sales records across 5 global regions
- 2-year comparison (2024 vs 2025)
- 6 product categories with growth analysis
- Geographic revenue mapping

### Dashboard 2: Sales Customer Profiling  
**Business Question:** *"Show me our sales performance and customer buying patterns for this year."*

**🔗 [View Live Dashboard](https://rehanali53.github.io/Business-Dashboards-Portfolio/sales-customer-dashboard/sales_customer_profiling_dashboard.html)**

**Key Features:**
- Key business metrics display
- Monthly sales with year-over-year comparison
- Customer behavior analysis by segments
- Product group breakdown
- Top customer rankings

**Data Overview:**
- 750+ individual sales transactions
- 50 customers across 4 segments (NEW, REGULAR, VIP, SENSITIVE)
- 4 product groups with performance tracking
- Monthly trends with previous year comparison

## 🗂️ Project Structure

```
Business-Dashboards-Portfolio/
├── README.md                           # This file
├── requirements.txt                    # Python packages needed
├── ecommerce-dashboard/               # Dashboard 1 files
│   ├── data_gen.py                   # Creates dummy data
│   ├── viz.py                        # Creates the dashboard
│   ├── datasets/                     # Generated data files
│   │   ├── monthly_sales_data.csv
│   │   ├── regional_performance.csv
│   │   ├── category_sales.csv
│   │   └── customer_metrics.csv
│   └── ecommerce_dashboard.html      # Final dashboard
└── sales-customer-dashboard/          # Dashboard 2 files
    ├── data_gen.py                   # Creates dummy data
    ├── viz.py                        # Creates the dashboard
    ├── datasets/                     # Generated data files
    │   ├── sales_transactions.csv
    │   ├── monthly_sales_summary.csv
    │   ├── customer_summary.csv
    │   └── product_group_summary.csv
    └── sales_customer_profiling_dashboard.html  # Final dashboard
```

## 🚀 How to Use

### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Generate Data and Create Dashboards

**For E-commerce Dashboard:**
```bash
python ecommerce-dashboard/data_gen.py      # Creates the data files
python ecommerce-dashboard/viz.py           # Creates the dashboard
```

**For Sales Customer Dashboard:**
```bash
python sales-customer-dashboard/data_gen.py      # Creates the data files
python sales-customer-dashboard/viz.py           # Creates the dashboard
```

### Step 3: View the Dashboards
Open the HTML files in your web browser:
- `ecommerce-dashboard/ecommerce_dashboard.html`
- `sales-customer-dashboard/sales_customer_profiling_dashboard.html`

## 📈 Dashboard Details

### E-commerce Dashboard Features
- **6 different chart types**: Line charts, pie charts, bar charts, scatter plots, geographic maps
- **120 data records**: Monthly sales across 5 regions for 2 years
- **Interactive features**: Hover tooltips, zoom, pan, and filtering
- **Business insights**: Regional performance, product trends, customer growth

### Sales Customer Dashboard Features  
- **5 different chart types**: Metrics cards, bar charts, scatter plots, pie charts, data tables
- **750+ data records**: Individual sales transactions throughout 2023
- **Customer segments**: NEW, REGULAR, VIP, and SENSITIVE customer groups
- **Business insights**: Customer behavior, product performance, sales trends

## 🛠️ Technologies Used

- **Python**: Main programming language
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **NumPy**: Numerical computations
- **HTML**: Dashboard output format

## 💡 Key Skills Demonstrated

- **Data Generation**: Creating realistic business datasets
- **Data Analysis**: Processing and aggregating business data
- **Data Visualization**: Building interactive dashboards
- **Business Intelligence**: Telling stories with data
- **Web Development**: Creating shareable HTML reports

## 📧 Contact

**Rehan Ali**  
[LinkedIn](https://www.linkedin.com/in/rehan-ali-me/)
Feel free to reach out if you have questions about these dashboards or want to discuss data visualization projects!

---

*Created by Rehan Ali with Python, Plotly, and lots of coffee ☕*
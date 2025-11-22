"""
E-commerce Sales Analysis Web Application
Flask-based dashboard with interactive visualizations
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)

# Load data
def load_data():
    """Load and cache the sales data"""
    try:
        df = pd.read_csv('powerbi_data/SalesData_Complete.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except FileNotFoundError:
        # If powerbi_data doesn't exist, create it
        import os
        if not os.path.exists('powerbi_data'):
            os.system('python prepare_powerbi_data.py')
        df = pd.read_csv('powerbi_data/SalesData_Complete.csv')
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df

# Cache data on startup
sales_data = load_data()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/summary')
def get_summary():
    """Get summary statistics"""
    summary = {
        'total_revenue': float(sales_data['Sales'].sum()),
        'total_orders': int(len(sales_data)),
        'total_quantity': int(sales_data['Quantity Ordered'].sum()),
        'avg_order_value': float(sales_data['Sales'].mean()),
        'unique_products': int(sales_data['Product'].nunique()),
        'unique_cities': int(sales_data['City'].nunique())
    }
    return jsonify(summary)

@app.route('/api/monthly-sales')
def get_monthly_sales():
    """Get monthly sales data"""
    monthly = sales_data.groupby('Month Name').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    
    # Sort by month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly['Month Name'] = pd.Categorical(monthly['Month Name'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('Month Name')
    
    return jsonify({
        'months': monthly['Month Name'].tolist(),
        'sales': monthly['Sales'].tolist(),
        'orders': monthly['Order ID'].tolist()
    })

@app.route('/api/top-cities')
def get_top_cities():
    """Get top 10 cities by sales"""
    cities = sales_data.groupby('City_State').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    cities = cities.sort_values('Sales', ascending=False).head(10)
    
    return jsonify({
        'cities': cities['City_State'].tolist(),
        'sales': cities['Sales'].tolist(),
        'orders': cities['Order ID'].tolist()
    })

@app.route('/api/top-products')
def get_top_products():
    """Get top 10 products by sales"""
    products = sales_data.groupby('Product').agg({
        'Sales': 'sum',
        'Quantity Ordered': 'sum'
    }).reset_index()
    products = products.sort_values('Sales', ascending=False).head(10)
    
    return jsonify({
        'products': products['Product'].tolist(),
        'sales': products['Sales'].tolist(),
        'quantity': products['Quantity Ordered'].tolist()
    })

@app.route('/api/hourly-sales')
def get_hourly_sales():
    """Get sales by hour of day"""
    hourly = sales_data.groupby('Hour').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    hourly = hourly.sort_values('Hour')
    
    return jsonify({
        'hours': hourly['Hour'].tolist(),
        'sales': hourly['Sales'].tolist(),
        'orders': hourly['Order ID'].tolist()
    })

@app.route('/api/category-sales')
def get_category_sales():
    """Get sales by product category"""
    categories = sales_data.groupby('Product Category').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    categories = categories.sort_values('Sales', ascending=False)
    
    return jsonify({
        'categories': categories['Product Category'].tolist(),
        'sales': categories['Sales'].tolist(),
        'orders': categories['Order ID'].tolist()
    })

@app.route('/api/state-sales')
def get_state_sales():
    """Get sales by state"""
    states = sales_data.groupby('State').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    states = states.sort_values('Sales', ascending=False)
    
    return jsonify({
        'states': states['State'].tolist(),
        'sales': states['Sales'].tolist(),
        'orders': states['Order ID'].tolist()
    })

@app.route('/api/daily-trend')
def get_daily_trend():
    """Get daily sales trend"""
    daily = sales_data.groupby('Date').agg({
        'Sales': 'sum',
        'Order ID': 'count'
    }).reset_index()
    daily = daily.sort_values('Date')
    
    # Convert dates to strings for JSON
    daily['Date'] = daily['Date'].astype(str)
    
    return jsonify({
        'dates': daily['Date'].tolist(),
        'sales': daily['Sales'].tolist(),
        'orders': daily['Order ID'].tolist()
    })

@app.route('/geographic')
def geographic():
    """Geographic analysis page"""
    return render_template('geographic.html')

@app.route('/products')
def products():
    """Product analysis page"""
    return render_template('products.html')

@app.route('/time-analysis')
def time_analysis():
    """Time analysis page"""
    return render_template('time_analysis.html')

if __name__ == '__main__':
    print("=" * 60)
    print("E-commerce Sales Analysis Dashboard")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Dashboard will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

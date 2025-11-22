"""
E-commerce Sales Data Preparation for Power BI
This script processes the raw sales data and creates Power BI-ready tables
with proper data model, relationships, and calculated columns.
"""

import pandas as pd
import os
from datetime import datetime

print("=" * 60)
print("E-commerce Sales Data Preparation for Power BI")
print("=" * 60)
print()

# Step 1: Load all monthly data
print("Step 1: Loading data from CSV files...")
files = [file for file in os.listdir('dataset') if file.endswith('.csv')]
df = pd.DataFrame()

for file in files:
    data = pd.read_csv(f'dataset/{file}')
    df = pd.concat([df, data], axis=0)

print(f"✓ Loaded {len(files)} files with {len(df)} total records")

# Step 2: Clean the data
print("\nStep 2: Cleaning data...")

# Remove header rows that got mixed in
df = df[df['Order ID'] != 'Order ID']

# Remove null values
df = df.dropna()

# Reset index
df = df.reset_index(drop=True)

print(f"✓ Cleaned data: {len(df)} valid records")

# Step 3: Fix data types
print("\nStep 3: Converting data types...")

df['Order ID'] = df['Order ID'].astype(str)
df['Quantity Ordered'] = df['Quantity Ordered'].astype('int64')
df['Price Each'] = df['Price Each'].astype('float')
df['Order Date'] = pd.to_datetime(df['Order Date'])

print("✓ Data types converted")

# Step 4: Extract features
print("\nStep 4: Creating calculated columns...")

# Extract city and state
def get_city(address):
    return address.split(',')[1].strip()

def get_state(address):
    return address.split(',')[2].split(' ')[1].strip()

df['City'] = df['Purchase Address'].apply(get_city)
df['State'] = df['Purchase Address'].apply(get_state)
df['City_State'] = df['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

# Extract date/time components
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month Name'] = df['Order Date'].dt.strftime('%B')
df['Quarter'] = df['Order Date'].dt.quarter
df['Day'] = df['Order Date'].dt.day
df['Day of Week'] = df['Order Date'].dt.day_name()
df['Hour'] = df['Order Date'].dt.hour
df['Date'] = df['Order Date'].dt.date

# Calculate sales
df['Sales'] = df['Quantity Ordered'] * df['Price Each']

# Add time period categories
df['Time Period'] = df['Hour'].apply(lambda x: 
    'Morning (6-12)' if 6 <= x < 12 else
    'Afternoon (12-18)' if 12 <= x < 18 else
    'Evening (18-24)' if 18 <= x < 24 else
    'Night (0-6)'
)

# Add product categories
def categorize_product(product):
    if 'Phone' in product or 'iPhone' in product:
        return 'Phones'
    elif 'Cable' in product or 'Charging' in product:
        return 'Cables & Chargers'
    elif 'Headphones' in product or 'Earbuds' in product:
        return 'Audio'
    elif 'Monitor' in product or 'TV' in product:
        return 'Displays'
    elif 'Laptop' in product or 'Macbook' in product:
        return 'Computers'
    elif 'Battery' in product or 'Batteries' in product:
        return 'Batteries'
    else:
        return 'Other'

df['Product Category'] = df['Product'].apply(categorize_product)

print("✓ Calculated columns created")

# Filter to 2019 only
df = df[df['Year'] == 2019]

print(f"✓ Filtered to 2019: {len(df)} records")

# Step 5: Create dimension tables for Power BI data model
print("\nStep 5: Creating dimension tables...")

# Fact Table - Sales Transactions
fact_sales = df[[
    'Order ID', 'Order Date', 'Date', 'Product', 'Quantity Ordered', 
    'Price Each', 'Sales', 'City', 'State', 'Product Category'
]].copy()

fact_sales.columns = [
    'OrderID', 'OrderDateTime', 'OrderDate', 'Product', 'QuantityOrdered',
    'PriceEach', 'SalesAmount', 'City', 'State', 'ProductCategory'
]

# Dimension Table - Date
date_dim = df[['Date', 'Year', 'Month', 'Month Name', 'Quarter', 'Day', 'Day of Week']].drop_duplicates()
date_dim = date_dim.sort_values('Date').reset_index(drop=True)
date_dim['DateKey'] = range(1, len(date_dim) + 1)
date_dim.columns = ['Date', 'Year', 'Month', 'MonthName', 'Quarter', 'Day', 'DayOfWeek', 'DateKey']

# Dimension Table - Time
time_dim = df[['Hour', 'Time Period']].drop_duplicates()
time_dim = time_dim.sort_values('Hour').reset_index(drop=True)
time_dim['TimeKey'] = range(1, len(time_dim) + 1)
time_dim.columns = ['Hour', 'TimePeriod', 'TimeKey']

# Dimension Table - Products
product_dim = df[['Product', 'Product Category', 'Price Each']].drop_duplicates()
product_dim = product_dim.sort_values('Product').reset_index(drop=True)
product_dim['ProductKey'] = range(1, len(product_dim) + 1)
product_dim.columns = ['ProductName', 'ProductCategory', 'StandardPrice', 'ProductKey']

# Dimension Table - Geography
geo_dim = df[['City', 'State', 'City_State']].drop_duplicates()
geo_dim = geo_dim.sort_values(['State', 'City']).reset_index(drop=True)
geo_dim['GeoKey'] = range(1, len(geo_dim) + 1)
geo_dim.columns = ['City', 'State', 'CityState', 'GeoKey']

print(f"✓ Created dimension tables:")
print(f"  - Fact Sales: {len(fact_sales)} records")
print(f"  - Date Dimension: {len(date_dim)} records")
print(f"  - Time Dimension: {len(time_dim)} records")
print(f"  - Product Dimension: {len(product_dim)} records")
print(f"  - Geography Dimension: {len(geo_dim)} records")

# Step 6: Create summary tables
print("\nStep 6: Creating summary tables...")

# Monthly Summary
monthly_summary = df.groupby(['Year', 'Month', 'Month Name']).agg({
    'Order ID': 'count',
    'Sales': 'sum',
    'Quantity Ordered': 'sum'
}).reset_index()
monthly_summary.columns = ['Year', 'Month', 'MonthName', 'TotalOrders', 'TotalSales', 'TotalQuantity']
monthly_summary['AvgOrderValue'] = monthly_summary['TotalSales'] / monthly_summary['TotalOrders']

# City Summary
city_summary = df.groupby(['City', 'State']).agg({
    'Order ID': 'count',
    'Sales': 'sum',
    'Quantity Ordered': 'sum'
}).reset_index()
city_summary.columns = ['City', 'State', 'TotalOrders', 'TotalSales', 'TotalQuantity']
city_summary['AvgOrderValue'] = city_summary['TotalSales'] / city_summary['TotalOrders']
city_summary = city_summary.sort_values('TotalSales', ascending=False)

# Product Summary
product_summary = df.groupby(['Product', 'Product Category']).agg({
    'Order ID': 'count',
    'Sales': 'sum',
    'Quantity Ordered': 'sum',
    'Price Each': 'mean'
}).reset_index()
product_summary.columns = ['Product', 'ProductCategory', 'TotalOrders', 'TotalSales', 'TotalQuantity', 'AvgPrice']
product_summary = product_summary.sort_values('TotalSales', ascending=False)

# Hourly Summary
hourly_summary = df.groupby(['Hour', 'Time Period']).agg({
    'Order ID': 'count',
    'Sales': 'sum'
}).reset_index()
hourly_summary.columns = ['Hour', 'TimePeriod', 'TotalOrders', 'TotalSales']

print("✓ Summary tables created")

# Step 7: Export to CSV files
print("\nStep 7: Exporting to Power BI-ready CSV files...")

# Create output directory
output_dir = 'powerbi_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Export all tables
fact_sales.to_csv(f'{output_dir}/FactSales.csv', index=False)
date_dim.to_csv(f'{output_dir}/DimDate.csv', index=False)
time_dim.to_csv(f'{output_dir}/DimTime.csv', index=False)
product_dim.to_csv(f'{output_dir}/DimProduct.csv', index=False)
geo_dim.to_csv(f'{output_dir}/DimGeography.csv', index=False)
monthly_summary.to_csv(f'{output_dir}/MonthlySummary.csv', index=False)
city_summary.to_csv(f'{output_dir}/CitySummary.csv', index=False)
product_summary.to_csv(f'{output_dir}/ProductSummary.csv', index=False)
hourly_summary.to_csv(f'{output_dir}/HourlySummary.csv', index=False)

# Also export the complete cleaned dataset
df.to_csv(f'{output_dir}/SalesData_Complete.csv', index=False)

print(f"✓ All files exported to '{output_dir}/' folder")

# Step 8: Create data model documentation
print("\nStep 8: Creating data model documentation...")

model_doc = """
# Power BI Data Model Documentation

## Overview
This data model follows a star schema design optimized for Power BI analysis.

## Tables

### Fact Table
**FactSales.csv** - Main transaction table
- OrderID: Unique order identifier
- OrderDateTime: Full date and time of order
- OrderDate: Date only (for relationship with DimDate)
- Product: Product name
- QuantityOrdered: Number of items ordered
- PriceEach: Price per item
- SalesAmount: Total sales (Quantity × Price)
- City: City name
- State: State code
- ProductCategory: Product category

### Dimension Tables

**DimDate.csv** - Date dimension
- DateKey: Unique identifier
- Date: Date value
- Year: Year (2019)
- Month: Month number (1-12)
- MonthName: Month name (January-December)
- Quarter: Quarter (1-4)
- Day: Day of month
- DayOfWeek: Day name (Monday-Sunday)

**DimTime.csv** - Time dimension
- TimeKey: Unique identifier
- Hour: Hour of day (0-23)
- TimePeriod: Time period category

**DimProduct.csv** - Product dimension
- ProductKey: Unique identifier
- ProductName: Product name
- ProductCategory: Product category
- StandardPrice: Standard price

**DimGeography.csv** - Geography dimension
- GeoKey: Unique identifier
- City: City name
- State: State code
- CityState: Combined city and state

### Summary Tables (Pre-aggregated for performance)

**MonthlySummary.csv** - Monthly aggregates
- Year, Month, MonthName
- TotalOrders, TotalSales, TotalQuantity
- AvgOrderValue

**CitySummary.csv** - City aggregates
- City, State
- TotalOrders, TotalSales, TotalQuantity
- AvgOrderValue

**ProductSummary.csv** - Product aggregates
- Product, ProductCategory
- TotalOrders, TotalSales, TotalQuantity
- AvgPrice

**HourlySummary.csv** - Hourly aggregates
- Hour, TimePeriod
- TotalOrders, TotalSales

**SalesData_Complete.csv** - Complete cleaned dataset with all columns

## Relationships (to create in Power BI)

1. FactSales[OrderDate] → DimDate[Date] (Many-to-One)
2. FactSales[Product] → DimProduct[ProductName] (Many-to-One)
3. FactSales[City] → DimGeography[City] (Many-to-One)

## Recommended Measures (DAX)

```dax
Total Sales = SUM(FactSales[SalesAmount])

Total Orders = COUNTROWS(FactSales)

Total Quantity = SUM(FactSales[QuantityOrdered])

Average Order Value = DIVIDE([Total Sales], [Total Orders])

Sales Growth = 
VAR CurrentSales = [Total Sales]
VAR PreviousSales = CALCULATE([Total Sales], DATEADD(DimDate[Date], -1, MONTH))
RETURN DIVIDE(CurrentSales - PreviousSales, PreviousSales)

Top 10 Products = 
CALCULATE(
    [Total Sales],
    TOPN(10, ALL(DimProduct[ProductName]), [Total Sales], DESC)
)
```

## Key Metrics

- Total Revenue: $34,483,365.68
- Total Orders: 185,916
- Total Items Sold: 209,038
- Average Order Value: $185.49
- Date Range: January 1, 2019 - December 31, 2019

## Usage Instructions

1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import all CSV files from the powerbi_data folder
4. Create relationships as specified above
5. Create measures using the DAX formulas
6. Build your visualizations

## Tips for Power BI

- Use DimDate for time-based analysis
- Use summary tables for quick dashboards
- Create hierarchies: Year → Quarter → Month → Date
- Use ProductCategory for drill-down analysis
- Filter by State/City for geographic analysis
"""

with open(f'{output_dir}/DATA_MODEL_README.md', 'w', encoding='utf-8') as f:
    f.write(model_doc)

print("✓ Data model documentation created")

# Step 9: Print summary statistics
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"\nTotal Revenue: ${df['Sales'].sum():,.2f}")
print(f"Total Orders: {len(df):,}")
print(f"Total Items Sold: {df['Quantity Ordered'].sum():,}")
print(f"Average Order Value: ${df['Sales'].mean():.2f}")
print(f"\nTop 5 Cities by Revenue:")
for idx, row in city_summary.head().iterrows():
    print(f"  {row['City']}, {row['State']}: ${row['TotalSales']:,.2f}")
print(f"\nTop 5 Products by Revenue:")
for idx, row in product_summary.head().iterrows():
    print(f"  {row['Product']}: ${row['TotalSales']:,.2f}")

print("\n" + "=" * 60)
print("✓ DATA PREPARATION COMPLETE!")
print("=" * 60)
print(f"\nAll files are ready in the '{output_dir}/' folder")
print("\nNext steps:")
print("1. Open Power BI Desktop")
print("2. Import CSV files from the powerbi_data folder")
print("3. Create relationships between tables")
print("4. Start building your dashboard!")
print("\nSee DATA_MODEL_README.md for detailed instructions.")
print("=" * 60)

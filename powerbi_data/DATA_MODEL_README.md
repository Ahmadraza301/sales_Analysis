
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

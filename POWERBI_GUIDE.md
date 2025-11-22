# Power BI Integration Guide

## 🎯 Quick Start

### Step 1: Prepare the Data
```cmd
# Double-click this file:
prepare_for_powerbi.bat

# Or run manually:
python prepare_powerbi_data.py
```

This will create a `powerbi_data` folder with 10 CSV files ready for Power BI.

### Step 2: Import into Power BI
1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to the `powerbi_data` folder
4. Import all CSV files

### Step 3: Create Relationships
See the detailed instructions below.

---

## 📊 Data Model Structure

### Star Schema Design

```
                    DimDate
                       ↓
    DimProduct → FactSales ← DimGeography
                       ↓
                    DimTime
```

### Tables Overview

| Table | Type | Records | Purpose |
|-------|------|---------|---------|
| FactSales | Fact | 185,916 | Main transaction data |
| DimDate | Dimension | 365 | Date attributes |
| DimTime | Dimension | 24 | Time attributes |
| DimProduct | Dimension | 19 | Product details |
| DimGeography | Dimension | 9 | Location details |
| MonthlySummary | Aggregate | 12 | Pre-calculated monthly stats |
| CitySummary | Aggregate | 9 | Pre-calculated city stats |
| ProductSummary | Aggregate | 19 | Pre-calculated product stats |
| HourlySummary | Aggregate | 24 | Pre-calculated hourly stats |
| SalesData_Complete | Full | 185,916 | Complete dataset (backup) |

---

## 🔗 Creating Relationships in Power BI

### Method 1: Automatic Detection
1. After importing all tables, go to "Model" view
2. Click "Manage Relationships"
3. Click "Autodetect"
4. Verify the relationships created

### Method 2: Manual Creation

#### Relationship 1: Sales to Date
- **From:** FactSales[OrderDate]
- **To:** DimDate[Date]
- **Cardinality:** Many-to-One (*)
- **Cross filter direction:** Single
- **Make this relationship active:** Yes

#### Relationship 2: Sales to Product
- **From:** FactSales[Product]
- **To:** DimProduct[ProductName]
- **Cardinality:** Many-to-One (*)
- **Cross filter direction:** Single
- **Make this relationship active:** Yes

#### Relationship 3: Sales to Geography
- **From:** FactSales[City]
- **To:** DimGeography[City]
- **Cardinality:** Many-to-One (*)
- **Cross filter direction:** Single
- **Make this relationship active:** Yes

---

## 📐 Creating Measures (DAX)

### Basic Measures

```dax
// Total Sales
Total Sales = SUM(FactSales[SalesAmount])

// Total Orders
Total Orders = COUNTROWS(FactSales)

// Total Quantity
Total Quantity = SUM(FactSales[QuantityOrdered])

// Average Order Value
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)

// Average Items per Order
Avg Items per Order = DIVIDE([Total Quantity], [Total Orders], 0)
```

### Advanced Measures

```dax
// Sales Growth (Month over Month)
Sales Growth MoM = 
VAR CurrentSales = [Total Sales]
VAR PreviousSales = 
    CALCULATE(
        [Total Sales],
        DATEADD(DimDate[Date], -1, MONTH)
    )
RETURN 
    DIVIDE(CurrentSales - PreviousSales, PreviousSales, 0)

// Sales Growth % (formatted)
Sales Growth % = 
FORMAT([Sales Growth MoM], "0.0%")

// Year-to-Date Sales
YTD Sales = 
TOTALYTD([Total Sales], DimDate[Date])

// Previous Year Sales
PY Sales = 
CALCULATE(
    [Total Sales],
    DATEADD(DimDate[Date], -1, YEAR)
)

// Year over Year Growth
YoY Growth = 
DIVIDE([Total Sales] - [PY Sales], [PY Sales], 0)

// Top 10 Products by Sales
Top 10 Products Sales = 
CALCULATE(
    [Total Sales],
    TOPN(
        10,
        ALL(DimProduct[ProductName]),
        [Total Sales],
        DESC
    )
)

// Running Total
Running Total = 
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(DimDate[Date]),
        DimDate[Date] <= MAX(DimDate[Date])
    )
)

// Sales Rank by City
City Rank = 
RANKX(
    ALL(DimGeography[City]),
    [Total Sales],
    ,
    DESC,
    DENSE
)

// Percentage of Total Sales
% of Total Sales = 
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(FactSales)),
    0
)
```

---

## 📊 Recommended Visualizations

### Page 1: Executive Dashboard

**KPI Cards (Top Row):**
- Total Sales: $34.5M
- Total Orders: 185.9K
- Avg Order Value: $185.49
- Total Items Sold: 209K

**Charts:**
1. **Line Chart:** Monthly Sales Trend
   - X-axis: DimDate[MonthName]
   - Y-axis: [Total Sales]
   - Legend: DimDate[Year]

2. **Bar Chart:** Top 10 Cities by Sales
   - Y-axis: DimGeography[City]
   - X-axis: [Total Sales]
   - Sort: Descending

3. **Donut Chart:** Sales by Product Category
   - Legend: DimProduct[ProductCategory]
   - Values: [Total Sales]

4. **Area Chart:** Sales by Hour
   - X-axis: DimTime[Hour]
   - Y-axis: [Total Sales]

### Page 2: Geographic Analysis

**Map Visual:**
- Location: DimGeography[State]
- Size: [Total Sales]
- Tooltips: City, Total Orders, Avg Order Value

**Table:**
- Columns: City, State, Total Sales, Total Orders, Avg Order Value
- Sort by: Total Sales (Descending)

**Clustered Bar Chart:** Sales by State
- Y-axis: DimGeography[State]
- X-axis: [Total Sales]

### Page 3: Product Analysis

**Matrix:**
- Rows: DimProduct[ProductCategory], DimProduct[ProductName]
- Values: [Total Sales], [Total Orders], [Total Quantity]

**Treemap:** Product Sales Distribution
- Group: DimProduct[ProductCategory]
- Details: DimProduct[ProductName]
- Values: [Total Sales]

**Scatter Chart:** Price vs Quantity
- X-axis: DimProduct[StandardPrice]
- Y-axis: [Total Quantity]
- Details: DimProduct[ProductName]
- Size: [Total Sales]

### Page 4: Time Analysis

**Line and Stacked Column Chart:**
- X-axis: DimDate[MonthName]
- Column Y-axis: [Total Orders]
- Line Y-axis: [Average Order Value]

**Heatmap (Matrix):**
- Rows: DimDate[DayOfWeek]
- Columns: DimTime[Hour]
- Values: [Total Sales]
- Conditional formatting: Color scale

**Waterfall Chart:** Monthly Sales Breakdown
- Category: DimDate[MonthName]
- Y-axis: [Total Sales]

---

## 🎨 Dashboard Design Tips

### Color Scheme
Use the project's color palette:
- Primary: #0892a5 (Teal)
- Secondary: #2e9b9b, #50a290, #6fa985
- Accent: #8dad7f, #a9b17e, #c4b383, #dbb68f

### Layout Best Practices
1. **Top Row:** KPIs (4 cards)
2. **Second Row:** Main trend chart (full width)
3. **Third Row:** 2-3 supporting charts
4. **Filters:** Left sidebar or top

### Interactivity
- Enable cross-filtering between visuals
- Add slicers for:
  - Date range
  - Product category
  - State/City
  - Time period

---

## 🔍 Sample Analysis Questions

Your Power BI dashboard can answer:

### Sales Performance
- What is our total revenue and how is it trending?
- Which months had the highest sales?
- What is our average order value?

### Geographic Insights
- Which cities generate the most revenue?
- How does sales distribution look across states?
- Where should we focus marketing efforts?

### Product Analysis
- What are our best-selling products?
- Which product categories drive the most revenue?
- What is the price-quantity relationship?

### Time Patterns
- What are our peak sales hours?
- Which days of the week are busiest?
- How do sales vary throughout the day?

### Customer Behavior
- What is the typical order size?
- Which products are frequently bought together?
- What is the purchase pattern by time of day?

---

## 📈 Advanced Features

### Drill-Through Pages

Create a product detail page:
1. Add "Drill through" field: DimProduct[ProductName]
2. Add visuals showing:
   - Sales trend for that product
   - Top cities for that product
   - Peak hours for that product

### Bookmarks

Create bookmarks for:
- Top 10 Products view
- Geographic focus view
- Time analysis view
- Executive summary view

### Parameters

Create "What-If" parameters:
- Target sales goal
- Discount percentage
- Growth rate assumptions

---

## 🚀 Performance Optimization

### For Large Datasets

1. **Use Summary Tables:**
   - Use pre-aggregated tables for overview pages
   - Use FactSales only for detailed drill-downs

2. **Optimize Measures:**
   - Use SUMMARIZE instead of ADDCOLUMNS when possible
   - Avoid complex calculated columns

3. **Reduce Visual Count:**
   - Keep 6-8 visuals per page maximum
   - Use drill-through for details

4. **Enable Query Reduction:**
   - File → Options → Query reduction
   - Enable "Reduce number of queries sent"

---

## 📱 Publishing to Power BI Service

### Steps:
1. Save your .pbix file
2. Click "Publish" in Power BI Desktop
3. Select workspace
4. Configure scheduled refresh (if needed)

### Sharing:
- Create an app for end users
- Set up row-level security if needed
- Configure email subscriptions

---

## 🎓 Learning Resources

### Power BI Tutorials
- [Microsoft Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [Power BI Community](https://community.powerbi.com/)

### Sample Reports
Check the `powerbi_samples` folder (if available) for:
- Pre-built dashboard templates
- Sample .pbix files
- Custom visuals recommendations

---

## ✅ Checklist

Before finalizing your dashboard:

- [ ] All tables imported correctly
- [ ] Relationships created and active
- [ ] Key measures created
- [ ] Visuals are clear and labeled
- [ ] Filters and slicers work correctly
- [ ] Cross-filtering is enabled
- [ ] Color scheme is consistent
- [ ] Dashboard loads quickly
- [ ] Mobile layout configured (optional)
- [ ] Report tested with different filters

---

## 🆘 Troubleshooting

### Issue: Relationships not working
**Solution:** Check that data types match (Date to Date, Text to Text)

### Issue: Measures showing wrong values
**Solution:** Verify filter context and relationship directions

### Issue: Slow performance
**Solution:** Use summary tables, reduce visual count, optimize DAX

### Issue: Data not refreshing
**Solution:** Check file paths, ensure CSV files are accessible

---

## 📞 Support

For questions about:
- **Data preparation:** See `prepare_powerbi_data.py`
- **Data model:** See `powerbi_data/DATA_MODEL_README.md`
- **General project:** See `README.md`

---

## 🎉 You're Ready!

Your data is now optimized for Power BI analysis. Start building your dashboard and uncover insights!

**Happy analyzing!** 📊

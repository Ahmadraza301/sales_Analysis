# Power BI Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Prepare Data (1 minute)
```cmd
Double-click: prepare_for_powerbi.bat
```
✅ Creates 10 CSV files in `powerbi_data` folder

### Step 2: Import to Power BI (2 minutes)
1. Open **Power BI Desktop**
2. Click **Get Data** → **Text/CSV**
3. Navigate to `powerbi_data` folder
4. Select and import these files:
   - FactSales.csv
   - DimDate.csv
   - DimProduct.csv
   - DimGeography.csv
   - DimTime.csv

### Step 3: Create Relationships (1 minute)
Go to **Model** view and create:
- FactSales[OrderDate] → DimDate[Date]
- FactSales[Product] → DimProduct[ProductName]
- FactSales[City] → DimGeography[City]

### Step 4: Create Measures (1 minute)
In **Data** view, create new measures:
```dax
Total Sales = SUM(FactSales[SalesAmount])
Total Orders = COUNTROWS(FactSales)
Avg Order Value = DIVIDE([Total Sales], [Total Orders])
```

## 📊 Quick Dashboard

### Add These Visuals:

**1. KPI Cards (Top Row)**
- Total Sales: $34.5M
- Total Orders: 185.9K
- Avg Order Value: $185.49

**2. Line Chart - Monthly Trend**
- X-axis: DimDate[MonthName]
- Y-axis: [Total Sales]

**3. Bar Chart - Top Cities**
- Y-axis: DimGeography[City]
- X-axis: [Total Sales]

**4. Donut Chart - Product Categories**
- Legend: DimProduct[ProductCategory]
- Values: [Total Sales]

## 🎨 Quick Formatting

**Theme Colors:**
- #0892a5 (Primary)
- #2e9b9b (Secondary)
- #50a290 (Accent)

**Font:** Segoe UI

## 📁 Files Explained

| File | Use For |
|------|---------|
| FactSales.csv | Main transaction data |
| DimDate.csv | Time-based analysis |
| DimProduct.csv | Product details |
| DimGeography.csv | Location analysis |
| MonthlySummary.csv | Quick monthly charts |
| CitySummary.csv | Quick city charts |

## 🔥 Pro Tips

1. **Use Summary Tables** for overview dashboards (faster)
2. **Use FactSales** for detailed drill-downs
3. **Enable Cross-Filtering** between visuals
4. **Add Slicers** for Date, City, Product Category

## 📈 Key Insights to Show

- **Peak Month:** December ($4.6M)
- **Top City:** San Francisco ($8.3M)
- **Best Product:** Macbook Pro ($8M)
- **Rush Hours:** 11 AM - 8 PM

## 🆘 Quick Fixes

**Problem:** Relationships not working
**Fix:** Check data types match (Date to Date, Text to Text)

**Problem:** Wrong totals
**Fix:** Use SUM() not SUMX() for simple aggregations

**Problem:** Slow performance
**Fix:** Use summary tables instead of FactSales

## 📚 Full Guide

For detailed instructions, see: **POWERBI_GUIDE.md**

---

**You're ready to build your dashboard!** 🚀

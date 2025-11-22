# How to Run the E-commerce Sales Analysis Project

## Project Overview
This project analyzes 2019 sales data for "Bluemazon" - an e-commerce company selling electronic items. The analysis provides insights on sales trends, top-performing products, and recommendations for business strategy.

## Prerequisites

### 1. Install Python
- Download and install Python 3.7 or higher from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"

### 2. Install Required Libraries
Open Command Prompt (CMD) and run these commands:

```cmd
pip install pandas
pip install matplotlib
pip install seaborn
pip install jupyter
```

Or install all at once:
```cmd
pip install pandas matplotlib seaborn jupyter
```

## Running the Project

### Step 1: Navigate to Project Directory
Open Command Prompt and navigate to the project folder:
```cmd
cd path\to\your\project\folder
```

### Step 2: Start Jupyter Notebook
Run this command:
```cmd
jupyter notebook
```

This will:
- Start the Jupyter server
- Automatically open your default web browser
- Display the Jupyter file browser

### Step 3: Open the Notebook
- In the browser, click on `ecommerce_sales.ipynb`
- The notebook will open in a new tab

### Step 4: Run the Analysis
You have two options:

**Option A: Run All Cells at Once**
- Click on "Cell" in the menu bar
- Select "Run All"
- Wait for all cells to execute (you'll see numbers appear next to each cell)

**Option B: Run Cells One by One**
- Click on the first cell
- Press `Shift + Enter` to run it and move to the next cell
- Repeat for each cell

## What the Notebook Does

### 1. Data Import
- Loads 12 CSV files (one for each month of 2019)
- Combines them into a single dataset with 186,850+ orders

### 2. Data Cleaning
- Removes null values (545 rows)
- Fixes incorrect data types
- Filters data to only 2019 records

### 3. Feature Engineering
Creates new columns:
- Year, Month, Hour, Minute
- Sales (Quantity × Price)
- Cities (extracted from addresses)

### 4. Analysis Performed

**Descriptive Statistics:**
- Total Revenue: $34,483,365.68
- Total Orders: 185,916
- Total Items Sold: 209,038

**Univariate Analysis:**
- Orders by city (San Francisco and LA lead)
- Orders by month (December and October peak)
- Sales by hour (peak 9 AM - 9 PM)
- Top products (batteries, cables, headphones)

**Multivariate Analysis:**
- Product combinations frequently bought together
- Order probability by product type

### 5. Visualizations
The notebook generates 7 charts saved in the `images` folder:
- Distribution plots
- Bar charts for cities and months
- Time series for rush hours
- Product analysis charts

## Key Insights & Recommendations

### 1. Product Bundling Opportunities
Frequently bought together:
- Phone + Charging cable
- Phone + Headphones
- Charging cable + Headphones

**Recommendation:** Create product bundles to increase sales

### 2. Rush Hour Advertising
Peak sales occur between 9:00 AM - 9:00 PM

**Recommendation:** Schedule ads during these hours for maximum impact

### 3. Inventory Management
- iPhones have higher order probability than Google Phones
- Wired headphones outsell other headphone types
- Charging cables have consistent demand

**Recommendation:** Stock more high-probability items

### 4. Geographic Focus
Top cities:
1. San Francisco, CA (40,000+ orders)
2. Los Angeles, CA (30,000+ orders)

**Recommendation:** Focus marketing efforts on California

## Troubleshooting

### Issue: "jupyter: command not found"
**Solution:** Jupyter not installed or not in PATH
```cmd
pip install --upgrade jupyter
```

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution:** Install the missing library
```cmd
pip install pandas
```

### Issue: Notebook won't open
**Solution:** Try specifying the browser
```cmd
jupyter notebook --browser=chrome
```

### Issue: Cells won't run
**Solution:** Restart the kernel
- Click "Kernel" → "Restart & Clear Output"
- Then run cells again

## Project Structure

```
project/
│
├── dataset/                    # 12 monthly CSV files
│   ├── Sales_January_2019.csv
│   ├── Sales_February_2019.csv
│   └── ... (10 more files)
│
├── images/                     # Generated visualizations
│   ├── image1.png
│   ├── image2.png
│   └── ... (7 images total)
│
├── ecommerce_sales.ipynb      # Main analysis notebook
├── README.md                   # Project documentation
└── HOW_TO_RUN.md              # This file
```

## Additional Tips

1. **Save Your Work:** Jupyter auto-saves, but manually save with `Ctrl + S`

2. **Clear Output:** If notebook is slow, clear outputs:
   - "Cell" → "All Output" → "Clear"

3. **Export Results:** Export notebook as PDF or HTML:
   - "File" → "Download as" → Choose format

4. **Modify Analysis:** Feel free to add your own cells and analysis

5. **Dataset Source:** Original data from [Kaggle](https://www.kaggle.com/datasets/knightbearr/sales-product-data)

## Next Steps

After running the analysis, you can:
1. Modify visualizations to explore different aspects
2. Add new analysis sections
3. Test different product bundling strategies
4. Analyze specific time periods in detail
5. Compare performance across different cities

## Support

If you encounter issues:
1. Check that all libraries are installed correctly
2. Verify Python version (3.7+)
3. Ensure all CSV files are in the `dataset` folder
4. Try restarting Jupyter kernel

## Summary

This project provides a complete sales analysis pipeline from data loading to actionable insights. The notebook is ready to run without modifications and will generate all visualizations automatically.

**Estimated Runtime:** 2-3 minutes for complete execution

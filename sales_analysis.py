import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def load_sales_data(file_path):
      df=pd.read_csv(file_path)
      return df

df=load_sales_data("data/sales_messy.csv")

print('Sales data')
print(df)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)


df['Date'] = pd.to_datetime(
      df['Date'],
      format='mixed',
      dayfirst=True,
      errors='coerce'
      )

df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

print('\nData types after conversion:')
print(df.dtypes)

print('\nMissing values after conversion:')
print(df.isnull().sum())

df=df.drop_duplicates()

print('\nDuplicates after cleaning:')
print(df.duplicated().sum())

df['Product']=df['Product'].fillna('Unknown')

df['Category']=df['Category'].fillna('Unknown')

df['Quantity']=pd.to_numeric(df['Quantity'],errors='coerce')
df['Price']=pd.to_numeric(
      df['Price'].astype(str).str.replace(",",""),
      errors='coerce'
)
df['Sales']=pd.to_numeric(df['Sales'],errors='coerce')

df['Quantity']=df['Quantity'].fillna(df['Quantity'].median())

df['Price']=df['Price'].fillna(df['Price'].median())

df['Sales']=df['Sales'].fillna(df['Quantity']*df['Price'])

df['Date']=pd.to_datetime(
      df['Date'],
      format='mixed',
      dayfirst=True,
      errors='coerce'
)

df['Product']=df['Product'].str.strip().str.title()

df['Category']=df['Category'].str.strip().str.title()

df.loc[df['Quantity']<0,'Quantity']=df['Quantity'].median()

df.loc[df['Sales']<0,'Sales']=df['Quantity']*df['Price']

print('\nCleaned data:')
print(df)

print('\nMissing values after cleaning:')
print(df.isnull().sum())

print('\nData types after cleaning:')
print(df.dtypes)

df.to_csv('data/sales_cleaned.csv',index=False)

print('\nCleaned dataset saved successfully.')

# step 4

print("\n---Basic Analysis---")

category_sales=df.groupby("Category")["Sales"].sum()

print("\nTotal sales by category: ")
print(category_sales)

product_sales=df.groupby("Product")["Sales"].sum()

print("\nSales by product: ")
print(product_sales)

print("\nTop selling product: ")
print(product_sales.sort_values(ascending=False))

print("\nTop 3 selling products: ")
print(product_sales.sort_values(ascending=True).head(3))

print("\nTop selling categories: ")
print(category_sales.sort_values(ascending=False))

daily_sales=df.groupby("Date")["Sales"].sum()

print("\nSales trend over time: ")
print(daily_sales)

monthly_sales=df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()

print("\nMonthly sales:")
print(monthly_sales)

average_order_value=df["Sales"].sum()/len(df)

print("\nAverage order value:")
print(average_order_value)

print(f"\nAverage order value: ₹{average_order_value:.2f}")

peak_sales_date=daily_sales.idxmax()
peak_sales_amount=daily_sales.max()

print("\nPeak sales period: ")
print("Date: ",peak_sales_date)
print("Amount: ",peak_sales_amount)

peak_month=monthly_sales.idxmax()
peak_month_sales=monthly_sales.max()

print("\nPeak sales month: ")
print("Month: ",peak_month)
print("Sales: ",peak_month_sales)

# step 5

monthly_sales=df.groupby(
      df['Date'].dt.to_period('M')
)['Sales'].sum()

print("\nMonthly sales: ")
print(monthly_sales)

monthly_growth=monthly_sales.pct_change()*100
print("\nMonthly sales growth rate: ")
print(monthly_growth)

customer_sales=df.groupby('Customer_ID')["Sales"].sum()

print("\nTotal sales by customer: ")
print(customer_sales.sort_values(ascending=False))

customer_orders=df.groupby("Customer_ID").size()

print("\nNumber of orders by customer: ")
print(customer_orders.sort_values(ascending=False))

customer_average=df.groupby("Customer_ID")["Sales"].mean()

print("\nAverage spending per customer: ")
print(customer_average.sort_values(ascending=False))

customer_first_purchase=df.groupby("Customer_ID")["Date"].min()

print("\nCustomer first purchase: ")
print(customer_first_purchase)

df["Cohort_Month"]=df["Customer_ID"].map(
      customer_first_purchase
).dt.to_period("M")

print("\nCohort month: ")
print(df[["Customer_ID","Date","Cohort_Month"]])

average_purchase_value=df.groupby("Customer_ID")["Sales"].mean()

purchase_frequency=df.groupby("Customer_ID").size()

customer_lifetime_value=(
      average_purchase_value * purchase_frequency
)

print("\nCustomer lifetime value: ")
print(customer_lifetime_value.sort_values(ascending=False))

moving_average=monthly_sales.rolling(window=3).mean()
 
print("\n3-Month moving average: ")
print(moving_average)

forecast=monthly_sales.rolling(window=3).mean().iloc[-1]

print("\nForecast for next month: ")
print(f"₹{forecast:.2f}")

# step 6

# line chart

daily_sales=df.groupby("Date")["Sales"].sum()

plt.figure(figsize=(10,5))

plt.plot(daily_sales.index,daily_sales.values)

plt.title("Sales trend over time")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# pie chart

category_sales=df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(7,7))

plt.pie(
      category_sales,
      labels=category_sales.index,
      autopct="%1.1f%%"
)

plt.title("Sales distribution by category")

plt.show()

# bar chart

monthly_sales=df.groupby(
      df["Date"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.index=monthly_sales.index.astype(str)

plt.figure(figsize=(10,5))

plt.bar(
      monthly_sales.index,
      monthly_sales.values
)

plt.title("Monthly sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

if "Location" in df.columns:
      location_sales=df.groupby("Location")["Sales"].sum()
      
      plt.figure(figsize=(8,5))
      
      plt.bar(
            location_sales.index,
            location_sales.values
      )
      
      plt.title("Sales by location")
      plt.xlabel("Location")
      plt.ylabel("Sales")
      
      plt.xticks(rotation=45)
      plt.tight_layout()
      
      plt.show()
      
else:
      print("\nLocation column not available.")
      print("Geographical sales analysis skipped.")



# sales dashboard

fig, axes=plt.subplots(2, 2, figsize=(14,10))

# sales trend

axes[0,0].plot(
      daily_sales.index,
      daily_sales.values
)

axes[0,0].set_title("Sales trend")
axes[0,0].set_xlabel("Trend")
axes[0,0].set_ylabel("Sales")

axes[0,0].tick_params(axis="x",rotation=45)

# category sales

axes[0,1].pie(
      category_sales,
      labels=category_sales.index,
      autopct="%1.1f%%"
)

axes[0,1].set_title("Sales by category")

# monthly sales

axes[1,0].bar(
      monthly_sales.index,
      monthly_sales.values
)

axes[1,0].set_title("Monthly sales")
axes[1,0].set_title("Month")
axes[1,0].set_title("Sales")

axes[1,0].tick_params(axis="x",rotation=45)

# location sales

if "Location" in df.columns:
      
      location_sales=df.groupby("Location")["Sales"].sum()
      
      axes[1,1].bar(
            location_sales.index,
            location_sales.values
      )
      
      axes[1,1].set_title("Sales by location")
      axes[1,1].set_title("Location")
      axes[1,1].set_title("Sales")
      
      axes[1,1].tick_params(axis="x",rotation=45)
      
else:
      axes[1,1].text(
            0.5,
            0.5,
            "Location data not available",
            ha="center",
            va="center"
      )
      
      axes[1,1].set_title("Geographical sales")
      
plt.suptitle("Sales analysis dashboard")

plt.tight_layout()

plt.show()

# reporting

print("\n---Reporting---")

summary_statistics=df.describe()

print("\nSummary statistics: ")
print(summary_statistics)

summary_statistics.to_csv(
      "data/summary_statistics.csv"
)

print("\nSummary statistics saved.")

# executive summary

total_sales=df["Sales"].sum()

total_orders=len(df)

average_order_value=df["Sales"].mean()

top_product=(
      df.groupby("Product")["Sales"]
      .sum()
      .idxmax()
)

top_category=(
      df.groupby("Category")["Sales"]
      .sum()
      .idxmax()
)

peak_sales_date=(
      df.groupby("Date")["Sales"]
      .sum()
      .idxmax()
)

peak_sales_amount=(
      df.groupby("Date")["Sales"]
      .sum()
      .max()
)

print("\n---Executive Summary---")

print("Total sales: ",total_sales)
print("Total orders: ",total_orders)
print("Average order value: ",average_order_value)
print("Top selling product: ",top_product)
print("Top selling category: ",top_category)
print("Peak sales date: ",peak_sales_date)
print("Peak sales amount: ",peak_sales_amount)

# export category sales

category_sales=(
      df.groupby("Category")["Sales"]
      .sum()
      .reset_index() 
)

category_sales.to_csv(
      "data/category_sales.csv",
      index=False
)

# export product sales

product_sales=(
      df.groupby("Product")["Sales"]
      .sum()
      .reset_index()
)

product_sales.to_csv(
      "data.product_sales.csv"
)

# export to excel

with pd.ExcelWriter(
      "data/sales_analysis_report.xlsx"
) as writer:
      
      df.to_excel(
            writer,
            sheet_name="Cleaned data",
            index=False
      )
      
      summary_statistics.to_excel(
            writer,
            sheet_name="Summary statistics"
      )
      
      category_sales.to_excel(
            writer,
            sheet_name="Category sales",
            index=False
      )
      
      product_sales.to_excel(
            writer,
            sheet_name="Product sales",
            index=False
      )
      
print("\nExcel report created successfully.")

# sales trend

plt.figure(figsize=(10,5))

plt.plot(
      daily_sales.index,
      daily_sales.values
)

plt.title("Sales trend over time")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
      "data/sales_trend.png"
)

plt.show()

# category pie chart

plt.figure(figsize=(7,7))

plt.pie(
      category_sales["Sales"],
      labels=category_sales["Category"],
      autopct="%1.1f%%"
)

plt.title("Sales distribution by category")

plt.savefig(
      "data/category_sales.png"
)

# monthly sales

plt.figure(figsize=(10,5))

plt.bar(
      monthly_sales.index.astype(str),
      monthly_sales.values
)

plt.title("Monthly sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
      "data/monthly_sales.png"
)

plt.show()

# html report

html_report = f"""
<html>

<head>
<title>Sales Analysis Report</title>
</head>

<body>

<h1>Sales Analysis Report</h1>

<h2>Executive Summary</h2>

<p>Total sales: ₹{total_sales:.2f}</p>
<p>Total orders: {total_orders}</p>
<p>Average order value:  ₹{average_order_value:.2f}</p>
<p>Top selling product: {top_product}</p>
<p>Top selling category: {top_category}</p>
<p>Peak sales date: {peak_sales_date}</p>
<p>Peak sales amount: ₹{peak_sales_amount:.2f}</p>

<h2>Visualization</h2>

<img src="sales_trend.png" width="700">

<br><br>

<img src="category_sales.png" width="500">

<br><br>

<img src="monthly_sales.png" width="700">

</body>

</html>

"""

with open(
      "data/sales_report.html",
      "w",
      encoding="utf-8"
) as file :
      file.write(html_report)
      
print("\nHTML report created successfully.")

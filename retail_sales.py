import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import textwrap

# Load dataset

df = pd.read_excel('US Superstore data.xls')
print(df.head())
print(df.columns)
print(df.info())
print(df.isnull().sum())
print(df['Customer Name'].nunique())
print('All good')

# Unique values
print(df['Category'].unique())
print(df['Region'].unique())
print(df['City'].nunique())
print(df['State'].nunique())
print(df['Sales'].describe())


###Cleaning

df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.dropna().drop_duplicates()
df.to_csv('cleaned_superstore.csv', index=False)
print('Data Cleaned')


## Profit
# By Category:
profit_by_category = df.groupby('Category')['Profit'].sum().reset_index()
profit_by_category = profit_by_category.sort_values('Profit', ascending=False)
print('\nProfit by Category:')
print(profit_by_category)

# By Product:
print("\nUnique products:", df['Product Name']. nunique())
profit_by_product = df.groupby('Product Name')['Profit'].sum().reset_index()
profit_by_product = profit_by_product.sort_values('Profit', ascending=False)
print("\n Top 5 products by profit:")
print(profit_by_product.head(5))

## City/State Sales

#State
print("\nUnique states:", df['State'].nunique())
sales_by_state = df.groupby('State')['Sales'].sum().reset_index()
sales_by_state = sales_by_state.sort_values('Sales', ascending=False)
print('\nTop 5 states by sales:')
print(sales_by_state.head(5))


# City
print("\nUnique cities:", df['City'].nunique())
sales_by_city = df.groupby('City')['Sales'].sum().reset_index()
sales_by_city = sales_by_city.sort_values('Sales', ascending=False)
print("\n Top 5 cities by sales")
print(sales_by_city.head(5))

## Loyal customers
# Frequency
print("\n Unique customers:", df['Customer Name'].nunique())
orders_per_customer = df.groupby('Customer Name')['Order ID'].nunique().reset_index()
orders_per_customer.columns = ['Customer Name', 'Order Count']
#Longevity
df['Year'] = df['Order Date'].dt.year
years_per_customer = df.groupby('Customer Name')['Year'].nunique().reset_index()
years_per_customer.columns = ['Customer Name', 'Years Active']
#Loyalty
loyalty = orders_per_customer.merge(years_per_customer, on='Customer Name')
loyal_customers = loyalty[(loyalty['Years Active']>= 3) & (loyalty['Order Count']>= 10)]
loyal_customers = loyal_customers.sort_values('Order Count', ascending=False)
print("\nTop 5 loyal customers:")
print(loyal_customers.head(5))


## High discount
# By Category:
discount_by_category = df.groupby('Category')['Discount'].mean().reset_index()
discount_by_category = discount_by_category.sort_values('Discount', ascending=False)
print("\nAverage discount by Category:")
print(discount_by_category)
# By Product:
discount_by_product = df.groupby('Product Name')['Discount'].mean().reset_index()
discount_by_product = discount_by_product.sort_values('Discount', ascending=False)
print('\nTop 5 products by average discount:')
print(discount_by_product.head(5))

### Visualization
def wrap_labels(labels, width=25):
    return[textwrap.fill(label, width) for label in labels]
#Profit by Product
top_products= profit_by_product.head(5).copy()
top_products['Product Name Wrapped'] = wrap_labels(top_products['Product Name'], width=25)
plt.figure(figsize=(10,8))
palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
ax = sns.barplot(y='Product Name Wrapped', x='Profit', hue='Product Name Wrapped', data=top_products,
            palette= palette, legend=False)
for container in ax.containers:
    ax.bar_label(container, fmt=lambda x:f'{x/1000:,.2f}K', padding=-50, fontsize=9, fontweight='bold', color='white')
plt.title('Profit by Product', fontsize=12, fontweight='bold')
plt.xlabel('Total Profit ($)')
plt.ylabel('Products')
plt.tight_layout()
plt.savefig('profit_by_product_bar.png')
plt.show()
#Sales by City
top_cities = sales_by_city.head(5)
plt.figure(figsize=(10,6))
ax = sns.barplot(y='City',x='Sales', hue='City', data=top_cities, 
            palette= palette,legend=False)
for container in ax.containers:
    ax.bar_label(container, fmt=lambda x:f'{x/1000:,.2f}K', padding=-50, fontsize=9, fontweight='bold', color='white')
plt.title('Top 5 Cities by Sales')
plt.xlabel('Total Sales ($)')
plt.ylabel('City')
plt.savefig('sales_by_city_horizontal.png')
plt.show()
#Loyal Customers
top_loyal =loyal_customers.head(5)
plt.figure(figsize=(10,8))
ax=sns.barplot(x='Customer Name', y='Order Count', hue='Customer Name', data=top_loyal, palette=palette, legend=False)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold')
plt.title('Top 5 Loyal Customers(3+ Years Active)')
plt.xticks(rotation=45)
plt.xlabel('Customers')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.savefig('loyal_customers_bar.png')
plt.show()
#High discount rates by product
top_discount = discount_by_product.head(5).copy()
top_discount['Product Name Wrapped'] = wrap_labels(top_discount['Product Name'], width=25)
fig, ax = plt.subplots(figsize=(14,6))
for i, (discount, name) in enumerate(zip(top_discount['Discount'], top_discount['Product Name Wrapped'])):
    ax.hlines(y=name, xmin=0, xmax=discount, color='#1f77b4', linewidth=2)
    ax.scatter(discount, name, color='#ff7f0e', s=100)
    ax.text(x=discount+0.01, y=name, s=f'{discount:.0%}', ha='left', va='center', fontsize=9)
ax.set_title('Top 5 Products with Highes Average Discount', fontsize=12, fontweight='bold')
ax.set_xlabel('Average discount', fontsize=10)
ax.set_ylabel('Product Name', fontsize=10)
ax.tick_params(axis='y',labelsize=9)
ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0))
ax.grid(True, axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('discount_by_product_lollipop.png')
plt.show()
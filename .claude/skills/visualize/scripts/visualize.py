"""
Data visualization and KPI analysis script.

Reads parquet files from the latest migration folder and generates
KPIs and visualizations based on sales and returns data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def get_latest_data_folder(base_path: str) -> Path:
    """
    Get the latest folder from the migrate data directory based on datetime naming.

    Args:
        base_path: Path to the migrate data directory

    Returns:
        Path to the latest data folder

    Raises:
        FileNotFoundError: If no data folders are found
    """
    base = Path(base_path)
    folders = [d for d in base.iterdir() if d.is_dir()]

    if not folders:
        raise FileNotFoundError(f"No data folders found in {base_path}")

    return max(folders, key=lambda x: x.name)


# Setup
MIGRATE_BASE = Path("./.claude/skills/migrate/data")
DATA_DIR = get_latest_data_folder(str(MIGRATE_BASE))
OUTPUT_DIR = Path("./.claude/skills/visualize/visualization")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Data Visualization and KPI Analysis")
print("=" * 70)
print(f"\nData folder: {DATA_DIR.name}")
print(f"Output folder: {OUTPUT_DIR}\n")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
print("Loading data...")
fact_sales = pd.read_parquet(DATA_DIR / "fact_sales.parquet")
fact_returns = pd.read_parquet(DATA_DIR / "fact_returns.parquet")
dim_store = pd.read_parquet(DATA_DIR / "dim_store.parquet")
dim_product = pd.read_parquet(DATA_DIR / "dim_product.parquet")

print(f"Sales records: {len(fact_sales)}")
print(f"Returns records: {len(fact_returns)}\n")

# ===== CALCULATE KPIs =====
print("=" * 70)
print("CALCULATING KPIs")
print("=" * 70)

# 1. Total Sales
total_sales = fact_sales['net_amount'].sum()
print(f"\n1. Total Sales: ${total_sales:,.2f}")

# 2. Total Returns
total_returns = fact_returns['refund_amount'].sum()
print(f"2. Total Returns: ${total_returns:,.2f}")

# 3. Net Sales
net_sales = total_sales - total_returns
print(f"3. Net Sales: ${net_sales:,.2f}")

# 4. Average Sales Per Store
avg_sales_per_store = fact_sales.groupby('store_sk')['net_amount'].sum() / len(dim_store)
print(f"4. Average Sales Per Store: ${avg_sales_per_store.mean():,.2f}")

# 5. Average Sales Per Product
avg_sales_per_product = fact_sales.groupby('product_sk')['net_amount'].sum() / len(dim_product)
print(f"5. Average Sales Per Product: ${avg_sales_per_product.mean():,.2f}")

# ===== CREATE VISUALIZATIONS =====
print("\n" + "=" * 70)
print("GENERATING VISUALIZATIONS")
print("=" * 70 + "\n")

# 1. KPI Summary - Overview metrics
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Sales & Returns KPI Summary', fontsize=16, fontweight='bold')

kpi_data = [
    ('Total Sales', total_sales, '$'),
    ('Total Returns', total_returns, '$'),
    ('Net Sales', net_sales, '$'),
    ('Avg Sales/Store', avg_sales_per_store.mean(), '$'),
    ('Avg Sales/Product', avg_sales_per_product.mean(), '$'),
    ('Return Rate', (total_returns / total_sales) * 100, '%')
]

for idx, (label, value, unit) in enumerate(kpi_data):
    ax = axes[idx // 3, idx % 3]
    ax.text(0.5, 0.5, f'{value:,.0f}{unit}',
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(0.5, 0.1, label, ha='center', va='center', fontsize=12)
    ax.axis('off')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_kpi_summary.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 01_kpi_summary.png")
plt.close()

# 2. Sales by Store
fig, ax = plt.subplots(figsize=(12, 6))
sales_by_store = fact_sales.groupby('store_sk')['net_amount'].sum().reset_index()
sales_by_store['store_name'] = sales_by_store['store_sk'].map(
    dict(zip(dim_store['store_sk'], dim_store['store_name']))
)
sales_by_store = sales_by_store.sort_values('net_amount', ascending=False)
ax.bar(sales_by_store['store_name'], sales_by_store['net_amount'], color='steelblue')
ax.set_title('Total Sales by Store', fontsize=14, fontweight='bold')
ax.set_ylabel('Sales ($)')
ax.set_xlabel('Store')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_sales_by_store.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 02_sales_by_store.png")
plt.close()

# 3. Sales by Product (Top 10)
fig, ax = plt.subplots(figsize=(12, 6))
sales_by_product = fact_sales.groupby('product_sk')['net_amount'].sum().reset_index()
sales_by_product['product_name'] = sales_by_product['product_sk'].map(
    dict(zip(dim_product['product_sk'], dim_product['product_name']))
)
sales_by_product = sales_by_product.sort_values('net_amount', ascending=False).head(10)
ax.barh(sales_by_product['product_name'], sales_by_product['net_amount'], color='seagreen')
ax.set_title('Top 10 Products by Sales', fontsize=14, fontweight='bold')
ax.set_xlabel('Sales ($)')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_top_products.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 03_top_products.png")
plt.close()

# 4. Sales vs Returns Comparison
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['Sales', 'Returns', 'Net Sales']
values = [total_sales, total_returns, net_sales]
colors = ['#2ecc71', '#e74c3c', '#3498db']
bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_title('Sales, Returns & Net Sales Overview', fontsize=14, fontweight='bold')
ax.set_ylabel('Amount ($)')
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_sales_returns_comparison.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 04_sales_returns_comparison.png")
plt.close()

# 5. Return Reasons Distribution
fig, ax = plt.subplots(figsize=(10, 6))
return_reasons = fact_returns['return_reason'].value_counts()
ax.pie(return_reasons.values, labels=return_reasons.index, autopct='%1.1f%%',
       colors=sns.color_palette("husl", len(return_reasons)), startangle=90)
ax.set_title('Return Reasons Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_return_reasons.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 05_return_reasons.png")
plt.close()

# 6. Sales Quantity vs Value by Store
fig, ax = plt.subplots(figsize=(12, 6))
qty_by_store = fact_sales.groupby('store_sk').agg({
    'quantity': 'sum',
    'net_amount': 'sum'
}).reset_index()
qty_by_store['store_name'] = qty_by_store['store_sk'].map(
    dict(zip(dim_store['store_sk'], dim_store['store_name']))
)
qty_by_store = qty_by_store.sort_values('net_amount', ascending=False)

x = range(len(qty_by_store))
ax2 = ax.twinx()
bars = ax.bar(x, qty_by_store['quantity'], color='skyblue', alpha=0.7, label='Quantity')
line = ax2.plot(x, qty_by_store['net_amount'], color='red', marker='o', linewidth=2, label='Sales Value')
ax.set_xlabel('Store')
ax.set_ylabel('Quantity', color='skyblue')
ax2.set_ylabel('Sales Value ($)', color='red')
ax.set_title('Sales Quantity vs Value by Store', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(qty_by_store['store_name'], rotation=45, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "06_qty_vs_value_by_store.png", dpi=300, bbox_inches='tight')
print("[OK] Saved: 06_qty_vs_value_by_store.png")
plt.close()

print("\n" + "=" * 70)
print(f"[OK] All visualizations saved to: {OUTPUT_DIR}")
print("[OK] Visualization complete!")
print("=" * 70)
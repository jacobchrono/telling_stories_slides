import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('data/updated_customer_summary.csv')

# Define the category order
category_orders = ['short-term', 'medium-term', 'long-term']

# Calculate counts for each category in 'customer_term'
term_counts = df['customer_term'].value_counts().reindex(category_orders)

# Set up the plot style
plt.figure(figsize=(10, 6))
sns.set_style("darkgrid", {"axes.facecolor": "#000000", "grid.color": "gray"})
sns.set_context("talk")

# Create a bar plot with counts of each category
sns.barplot(
    x=term_counts.index,
    y=term_counts.values, 
    order=category_orders, 
    color="steelblue"
)

# Customize plot appearance
plt.title("Counts by Customer Term", loc='left', color='white')
plt.xlabel('')
plt.ylabel('Count', color='white')
plt.xticks(rotation=0, color='white')
plt.yticks(color='white')

sns.despine(top=True, right=True)

# Save plot
plt.savefig(f'graphs/customer_term_count.png', facecolor='#000000')
plt.close()

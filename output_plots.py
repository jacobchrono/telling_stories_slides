import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set up directory for saving graphs
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Load the data
data_path = 'data/20241029-customer-summary.csv'
data = pd.read_csv(data_path)

# Parse date columns and remove timezone information
data['first_order_date'] = pd.to_datetime(data['first_order_date'], errors='coerce').dt.tz_localize(None)
data['last_order_date'] = pd.to_datetime(data['last_order_date'], errors='coerce').dt.tz_localize(None)

# Calculate new variables
data['average_tip'] = data['total_tips'] / data['total_orders']
data['Average Tip Percentage'] = data['average_tip'] / data['average_order_value']

# Filter data for recent customers
recent_data = data[(data['last_order_date'] >= '2023-10-14') & (data['last_order_date'] <= '2024-10-14')]

# Define customer type based on total_orders
def categorize_customer(total_orders):
    if total_orders <= 1:
        return 'one-time'
    elif total_orders <= 10:
        return 'repeat'
    elif total_orders <= 100:
        return 'regular'
    else:
        return 'die-hard'

data['customer_type'] = data['total_orders'].apply(categorize_customer)

# Define customer term based on first_order_date for recent customers
def categorize_customer_term(first_order_date):
    if pd.Timestamp('2015-01-01') <= first_order_date <= pd.Timestamp('2017-12-31'):
        return 'long-term'
    elif pd.Timestamp('2018-01-01') <= first_order_date <= pd.Timestamp('2021-12-31'):
        return 'medium-term'
    elif pd.Timestamp('2022-01-01') <= first_order_date <= pd.Timestamp('2024-12-31'):
        return 'short-term'
    return np.nan

recent_data['customer_term'] = recent_data['first_order_date'].apply(categorize_customer_term)
data = pd.concat([data, recent_data[['customer_term']]], axis=1)

# Set category orders
category_orders = {
    'customer_term': ['short-term', 'medium-term', 'long-term'],
    'customer_type': ['one-time', 'repeat', 'regular', 'die-hard'],
}

# Function to generate and save bar plot
def save_barplot(categorical_var, dependent_var, title = None, file_name=None):
    # Filter data and set category order
    plot_data = data.dropna(subset=[categorical_var, dependent_var])
    order = category_orders.get(categorical_var, None)

    # Create plot with specific background color and white text
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"axes.facecolor": "#000000", "grid.color": "gray"})
    sns.set_context("talk")
    sns.barplot(x=categorical_var, y=dependent_var, data=plot_data, order=order, color="steelblue",errorbar=None)

    # Customize plot appearance
    plt.title(title, loc='left', color='white')
    plt.xlabel('', color='white')
    plt.ylabel(dependent_var.replace('_', ' ').title(), color='white')
    plt.xticks(rotation=0, color='white')

    # Set y-axis to display as percentages
    ticks = plt.yticks()[0]  # Get current y-ticks
    plt.yticks(ticks=ticks, labels=[f'{int(tick * 100)}%' for tick in ticks], color='white')

    sns.despine(top=True, right=True)

    # Save plot
    plt.savefig(f'graphs/{file_name}.png', facecolor='#000000')
    plt.close()

# Generate and save plots
save_barplot('customer_term', 'Average Tip Percentage', 
             title=None, file_name='Average tip by customer term')
save_barplot('customer_type', 'Average Tip Percentage', 
             title=None, file_name='Average tip by customer type')

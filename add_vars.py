import pandas as pd
import numpy as np

# Load the data
data_path = 'data/20241029-customer-summary.csv'
data = pd.read_csv(data_path)

# Parse date columns and remove timezone information
data['first_order_date'] = pd.to_datetime(data['first_order_date'], errors='coerce').dt.tz_localize(None)
data['last_order_date'] = pd.to_datetime(data['last_order_date'], errors='coerce').dt.tz_localize(None)

# Calculate new variables
data['average_tip'] = round(data['total_tips'] / data['total_orders'], 2)
data['avg_tip_percentage'] = round(data['average_tip'] / data['average_order_value'], 2)

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

# Define customer term based on first_order_date directly within the data DataFrame
def categorize_customer_term(first_order_date):
    if pd.Timestamp('2015-01-01') <= first_order_date <= pd.Timestamp('2017-12-31'):
        return 'long-term'
    elif pd.Timestamp('2018-01-01') <= first_order_date <= pd.Timestamp('2021-12-31'):
        return 'medium-term'
    elif pd.Timestamp('2022-01-01') <= first_order_date <= pd.Timestamp('2024-12-31'):
        return 'short-term'
    return np.nan

# Apply customer term only for recent customers directly
data['customer_term'] = data.apply(
    lambda row: categorize_customer_term(row['first_order_date']) 
    if '2023-10-14' <= str(row['last_order_date']) <= '2024-10-14' else np.nan, axis=1
)

# Create preferred_location by comparing front_total_spent and central_total_spent
data['preferred_location'] = np.where(data['front_total_spent'] > data['central_total_spent'], 'front', 'central')

# Define an alternative customer_term without limiting to recent customers
data['customer_term_full'] = data['first_order_date'].apply(categorize_customer_term)

# Calculate absolute spend ratios for favorite_category and favorite_item, rounded to 4 decimals
data['favorite_category_spend_ratio'] = round(data['favorite_category_spend_dollars'] / data['total_spent'], 4)
data['favorite_item_spend_ratio'] = round(data['favorite_item_spend_dollars'] / data['total_spent'], 4)

# Set category orders
category_orders = {
    'customer_term': ['short-term', 'medium-term', 'long-term'],
    'customer_type': ['one-time', 'repeat', 'regular', 'die-hard'],
}

# Save the updated data to a CSV file
output_path = 'data/updated_customer_summary.csv'
data.to_csv(output_path, index=False)

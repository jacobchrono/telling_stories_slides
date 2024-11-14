import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data_path = 'data/updated_customer_summary.csv'
data = pd.read_csv(data_path)

# Filter out rows with missing values in 'customer_term' and 'avg_tip_percentage'
data = data.dropna(subset=['customer_term', 'avg_tip_percentage'])

# Define the order of categories for consistent bar arrangement
category_order = ['new', 'medium-term', 'long-term']
# Define colors for each category without transparency, with lightest for 'new' and darkest for 'long-term'
colors = ['#82c4d5', '#41aff2', '#1d657c']  # Lightest to darkest

# Set up the figure for the bar plot
plt.figure(figsize=(8, 6))

# Apply the dark grid style and set the background color and grid color
sns.set_style("darkgrid", {"axes.facecolor": "#000000", "grid.color": "gray"})
sns.set_context("talk")

# Create a bar plot with custom color palette and category order
sns.barplot(
    x='customer_term', y='avg_tip_percentage', data=data,
    order=category_order, palette=colors, errorbar=None
)

# Customize the plot aesthetics
plt.ylabel('Average Tip Percentage', color='white')  # Set y-axis label color to white
plt.xticks(color='white')  # Set x-axis tick labels color to white
plt.yticks(color='white')  # Set y-axis tick labels color to white

# Set background color to black
plt.gca().set_facecolor("#000000")

# Add gridlines with zorder behind bars
#plt.grid(True, color='gray', zorder=0)

# Add horizontal gridlines only with zorder behind bars
#plt.grid(True, color='gray', axis='y', zorder=0)

# Convert y-axis labels to percentages
ticks = plt.yticks()[0]  # Get current y-ticks
plt.yticks(ticks=ticks, labels=[f'{int(tick * 100)}%' for tick in ticks], color='white')

# Remove the top and right spines for a cleaner look
sns.despine(top=True, right=True)

# Save the plot to a file
plt.savefig('graphs/Average_Tip_by_Customer_Term.png', facecolor='#000000')

# Display the plot
plt.show()

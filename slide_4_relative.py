import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('data/updated_customer_summary.csv')

# Step 1: Aggregate data by favorite item category and customer term, taking the average of the spend ratio
category_data = df.groupby(['favorite_item_category_name', 'customer_term'])['favorite_category_spend_ratio'].mean().reset_index()

# Step 2: Identify top 5 favorite item categories based on average spend ratio
top_categories = category_data.groupby('favorite_item_category_name')['favorite_category_spend_ratio'].mean().nlargest(10).index
top_category_data = category_data[category_data['favorite_item_category_name'].isin(top_categories)]

# Step 3: Set up the color scheme and plot style
category_order = ['new', 'medium-term', 'long-term']
color_palette = {'new': '#82c4d5', 'medium-term': '#41aff2', 'long-term': '#1d657c'}

# Step 4: Create the plot
plt.figure(figsize=(10, 10))  # Adjust size to fit in the window
sns.set_style("darkgrid", {"axes.facecolor": "#000000", "grid.color": "gray"})  # Dark grid style
sns.set_context("talk")  # Larger font for readability

# Step 5: Plot data with a horizontal barplot
sns.barplot(
    data=top_category_data,
    y='favorite_item_category_name',
    x='favorite_category_spend_ratio',
    hue='customer_term',
    order=top_categories,
    hue_order=category_order,
    palette=color_palette
)

# Step 6: Clean up plot for minimalistic look
sns.despine(top=True, right=True)  # Remove top and right borders for a cleaner appearance
plt.gca().set_facecolor("#000000")  # Set background color to black
# Remove the legend
plt.legend().remove()

# Aesthetics: Make x and y axis tick labels white for contrast
plt.xticks(color='white')
plt.yticks(color='white')
plt.ylabel('')
plt.xlabel('')
# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot with a black background to the specified folder
plt.savefig('graphs/slide_4_relative.png', facecolor='#000000')
print('Plot saved to the graphs folder.')

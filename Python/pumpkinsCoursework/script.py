import pandas as pd 
# read the pumpkins_14.csv file
df = pd.read_csv("pumpkins_14.csv")
#show first 5 rows
print(df.columns)
#show columns names
print(df.columns)
# STEP 2: Find the heaviest pumpkin

max_weight = df["weight_lbs"].max()
heaviest = df[df["weight_lbs"] == max_weight]

print("Heaviest pumpkin row:")
print(heaviest)

# Take the first row (in case there is more than one with same weight)
heaviest_row = heaviest.iloc[0]

heaviest_variety = heaviest_row["variety"]
heaviest_city = heaviest_row["city"]
heaviest_country = heaviest_row["country"]

print("Heaviest pumpkin details:")
print("  Weight (lbs):", max_weight)
print("  Variety:", heaviest_variety)
print("  Location:", heaviest_city, ",", heaviest_country)
# STEP 3: Add weight_kg column ----------------------------

df["weight_kg"] = df["weight_lbs"] * 0.453592

print(df[["weight_lbs", "weight_kg"]].head())
# STEP 4: Add weight_class column -------------------------

# convert the weight_kg column into a normal Python list
weight_kg_list = df["weight_kg"].tolist()

# create an empty list to store classes
weight_class_list = []

# classify each pumpkin based on weight
for kg in weight_kg_list:
    if kg < 200:
        weight_class_list.append("light")
    elif kg < 400:
        weight_class_list.append("medium")
    else:
        weight_class_list.append("heavy")

# add the new column to the dataframe
df["weight_class"] = weight_class_list

# show a few rows to check it worked
print(df[["weight_kg", "weight_class"]].head())

# STEP 5: Scatter plot - estimated vs actual weight

import matplotlib.pyplot as plt

# Separate data by class
df_light = df[df["weight_class"] == "light"]
df_medium = df[df["weight_class"] == "medium"]
df_heavy = df[df["weight_class"] == "heavy"]

plt.figure()

# Plot each class with a different colour
plt.scatter(df_light["est_weight"], df_light["weight_lbs"], color="blue", alpha=0.6, label="light")
plt.scatter(df_medium["est_weight"], df_medium["weight_lbs"], color="green", alpha=0.6, label="medium")
plt.scatter(df_heavy["est_weight"], df_heavy["weight_lbs"], color="red", alpha=0.6, label="heavy")

plt.xlabel("Estimated Weight (lbs)")
plt.ylabel("Actual Weight (lbs)")
plt.title("Estimated vs Actual Pumpkin Weight")
plt.legend()

# Save the plot as a file for your report
plt.savefig("plot_est_vs_actual.png")
plt.show()

# STEP 6: See which countries are in the data

print("Countries in the dataset:")
print(df["country"].value_counts())

# Filter for three selected countries

# CHANGE THESE to the three countries you choose from the list above
country1 = "Spain"
country2 = "Portugal"
country3 = "Poland"

# Keep only rows where country is one of the three
df_filtered = df[
    (df["country"] == country1) |
    (df["country"] == country2) |
    (df["country"] == country3)
]

print("Filtered countries (after applying filter):")
print(df_filtered["country"].value_counts())

# Save the filtered data to a new CSV file
df_filtered.to_csv("pumpkins_filtered.csv", index=False)
print("Saved pumpkins_filtered.csv")

# STEP 7: Summary of mean weight by country and variety -----

summary = df_filtered.groupby(["country", "variety"])["weight_kg"].mean()

print("Mean pumpkin weight (kg) by country and variety:")
print(summary)

# Optional: save to file for report or checking
summary.to_csv("pumpkins_summary.csv")
print("Saved pumpkins_summary.csv")

# STEP 8: Boxplot of weight (kg) by country

import matplotlib.pyplot as plt  
plt.figure()

# Boxplot using the filtered data (three countries only)
df_filtered.boxplot(column="weight_kg", by="country", grid=False)

plt.title("Pumpkin weight (kg) by country")
plt.suptitle("")  # removes the automatic 'weight_kg by country' title
plt.xlabel("Country")
plt.ylabel("Weight (kg)")

# Save the plot to a file for your report
plt.savefig("boxplot_weight_by_country.png")
plt.show()

# STEP 9: Faceted plot by variety

# Find top 3 varieties in filtered data
variety_counts = df_filtered["variety"].value_counts()
top_varieties = variety_counts.index[:3]

# Create a new figure with 3 subplots (1 row, 3 columns)
plt.figure(figsize=(15, 5))

# Loop through the top varieties
for i, variety in enumerate(top_varieties):
    plt.subplot(1, 3, i+1)  # 1 row, 3 columns, plot index

    df_var = df_filtered[df_filtered["variety"] == variety]
    plt.scatter(df_var["est_weight"], df_var["weight_kg"], alpha=0.6)

    plt.title(variety)
    plt.xlabel("Estimated Weight (lbs)")
    plt.ylabel("Actual Weight (kg)")

plt.tight_layout()
plt.savefig("faceted_plot_variety.png")
plt.show()
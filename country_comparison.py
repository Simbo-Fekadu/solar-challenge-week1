# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set seaborn style
sns.set_style("whitegrid")

# Load datasets
benin = pd.read_csv("./data/benin.csv", parse_dates=["Timestamp"])
sierra_leone = pd.read_csv("./data/sierraleone.csv", parse_dates=["Timestamp"])
togo = pd.read_csv("./data/togo.csv", parse_dates=["Timestamp"])

# Add country column
benin["Country"] = "Benin"
sierra_leone["Country"] = "Sierra Leone"
togo["Country"] = "Togo"

# Combine datasets
df = pd.concat([benin, sierra_leone, togo], ignore_index=True)

# Clip negative values
for col in ["GHI", "DNI", "DHI"]:
    df[col] = df[col].clip(lower=0)

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Boxplots: GHI, DNI, DHI, Tamb
plt.figure(figsize=(12, 8))
for i, col in enumerate(["GHI", "DNI", "DHI", "Tamb"], 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x="Country", y=col, data=df, palette="Set2")
    plt.title(f"{col} Distribution by Country")
    unit = " W/m²" if col in ["GHI", "DNI", "DHI"] else " °C"
    plt.ylabel(col + unit)
plt.tight_layout()
plt.savefig("outputs/country_boxplots.png")
plt.close()

# Overlaid Histograms: GHI, DNI, DHI
plt.figure(figsize=(15, 5))
for i, col in enumerate(["GHI", "DNI", "DHI"], 1):
    plt.subplot(1, 3, i)
    for country in ["Benin", "Sierra Leone", "Togo"]:
        subset = df[df["Country"] == country]
        plt.hist(subset[col], bins=30, alpha=0.4, label=country, density=True)
    plt.title(f"{col} Density")
    plt.xlabel(col + " W/m²")
    plt.ylabel("Density")
    plt.legend()
plt.tight_layout()
plt.savefig("outputs/country_histograms.png")
plt.close()

# Time Series: Monthly GHI Trends
df["Month"] = df["Timestamp"].dt.to_period("M")
monthly_ghi = df.groupby(["Month", "Country"])["GHI"].mean().unstack()
plt.figure(figsize=(12, 6))
for country in monthly_ghi.columns:
    plt.plot(monthly_ghi.index.astype(str), monthly_ghi[country], marker="o", label=country)
plt.title("Monthly Average GHI by Country")
plt.xlabel("Month")
plt.ylabel("GHI (W/m²)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/country_ghi_timeseries.png")
plt.close()

print("Plots saved to outputs/")

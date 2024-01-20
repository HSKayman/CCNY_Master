#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Import required libraries for data manipulation and visualization
import pandas as pd
from datetime import date
from datetime import datetime
import matplotlib.pylab as plt

# In[2]:

# Read trade data for SPY from CSV files for each day and store in a list of DataFrames
dataframes = []
for day in range(1, 6):
    df = pd.read_csv("Day{}_Trades_SPY.csv".format(day))
    dataframes.append(df)

# In[3]:

# Add a 'Day' column to each DataFrame to indicate the trading day
for day in range(5):
    dataframes[day]["Day"] = [day + 1] * len(dataframes[day])

# In[4]:

# Concatenate all DataFrames into a single DataFrame for combined analysis
for day in range(1, 5):
    dataframes[0] = pd.concat([dataframes[0], dataframes[day]])

# In[5]:

# Assign the combined DataFrame to 'df' for convenience
df = dataframes[0]

# In[6]:

# Convert 'Time' column to datetime format and eliminate nanoseconds precision
df['Time'] = pd.to_datetime(df['Time']).dt.floor('ns')

# In[7]:

# Convert 'PARTICIPANT_TIME' column to datetime format and eliminate nanoseconds precision
df['PARTICIPANT_TIME'] = pd.to_datetime(df['PARTICIPANT_TIME']).dt.floor('ns')

# In[8]:

# Check the data types of each column in the DataFrame
df.dtypes

# In[9]:

# Display the first five rows of the DataFrame to preview the data
df.head()

# In[10]:

# Reset the index of the DataFrame for a clean, sequential index
df = df.reset_index()
df

# In[73]:

# Set pandas option to display all rows when printing a DataFrame
pd.set_option('display.max_rows', None)

# Group data by 'Day' and provide descriptive statistics for the 'PRICE' column
df.groupby(['Day'])['PRICE'].describe()

# In[59]:

# Provide descriptive statistics for the 'SIZE' column, grouped by 'Day'
df.groupby(['Day'])['SIZE'].describe()

# In[13]:

# Extract hour and minute from 'Time' column and create new columns for them
times = pd.to_datetime(df.Time)
df['Hour'] = times.dt.hour
df['Minute'] = times.dt.minute

# In[16]:

# Create a unique identifier combining 'Day', 'Hour', and 'Minute' for each trade
df['TimeWithInfo'] = df['Day'] * 10000 + df['Hour'] * 100 + df['Minute']
df['TimeWithInfo'].head()

# In[20]:

# Initialize a dictionary to store open, low, high, close, volume, and count for each time period
OpenCloseTablePerHour = {}
Index = df.TimeWithInfo.unique()
OpenCloseTablePerHour["Open"] = []
OpenCloseTablePerHour["Low"] = []
OpenCloseTablePerHour["High"] = []
OpenCloseTablePerHour["Close"] = []
OpenCloseTablePerHour["Volume"] = []
OpenCloseTablePerHour["Count"] = []
IndexForPandas = []

# Populate the dictionary with values for each time period using the unique time identifier
for j in Index:
    Open = Low = High = Close = Volume = Count = 0

    try:
        Open = df[(df['TimeWithInfo'] == j)]['PRICE'].iloc[0]
    except IndexError:
        Open = 0
    OpenCloseTablePerHour["Open"].append(Open)

    try:
        Low = df[(df['TimeWithInfo'] == j)]['PRICE'].min()
    except ValueError:
        Low = 0
    OpenCloseTablePerHour["Low"].append(Low)

    try:
        High = df[(df['TimeWithInfo'] == j)]['PRICE'].max()
    except ValueError:
        High = 0
    OpenCloseTablePerHour["High"].append(High)

    try:
        Close = df[(df['TimeWithInfo'] == j)]['PRICE'].iloc[-1]
    except IndexError:
        Close = 0
    OpenCloseTablePerHour["Close"].append(Close)

    try:
        Volume = df[(df['TimeWithInfo'] == j)]['SIZE'].sum()
    except ValueError:
        Volume = 0
    OpenCloseTablePerHour["Volume"].append(Volume)

    try:
        Count = df[(df['TimeWithInfo'] == j)]['PRICE'].count()
    except ValueError:
        Count = 0
    OpenCloseTablePerHour["Count"].append(Count)
    IndexForPandas.append(j)

# In[75]:

# Convert the dictionary to a DataFrame for analysis and visualization
OpenCloseTablePerMinute = pd.DataFrame(OpenCloseTablePerHour, index=IndexForPandas)
OpenCloseTablePerMinute[(OpenCloseTablePerMinute.index > 40000) & (OpenCloseTablePerMinute.index < 50000)]

# In[88]:

# Check if the unique time identifiers are greater than 40000
a = OpenCloseTablePerMinute.index
a > 40000

# In[91]:

# Plot high and low prices for each currency and day using a filled area plot
fig, ax = plt.subplots(figsize=(20, 10))
for currency in range(1, 6):
    plotedFrame = OpenCloseTablePerMinute[(OpenCloseTablePerMinute.index > currency * 10000) & (OpenCloseTablePerMinute.index < (currency + 1) * 10000)]
    x = plotedFrame.index % 10000
    yDown = plotedFrame['Low']
    yUp = plotedFrame['High']
    ax.fill_between(x, yDown, yUp, alpha=.5, linewidth=0)
    ax.plot(x, (yDown + yUp) / 2, linewidth=2, label='Day ' + str(currency))
plt.legend()
plt.show()

# In[123]:

# Plot the 'PRICE' column for Day 5 trades over time
df[(df['Day'] == 5)].plot(x='TimeWithInfo', y='PRICE', figsize=(20, 10))

# In[124]:

# Plot the 'SIZE' column for Day 5 trades over time
df[(df['Day'] == 5)].plot(x='TimeWithInfo', y='SIZE', figsize=(20, 10))

# In[125]:

# Initialize a list to store heatmaps for trade count
HeatMaps1 = []
for k in range(1, 6):
    # Group the DataFrame by 'Hour' and 'Minute' and count the number of trades
    DensityMap = df[(df['Day'] == k)].groupby(["Hour", "Minute"]).count()['index']
    
    # Initialize lists to store unique hours and minutes
    IndexCol = []
    IndexRow = []
    
    # Populate the lists with unique hours and minutes
    for i in DensityMap.index:
        IndexCol.append(i[0])
        IndexRow.append(i[1])
    
    # Convert lists to sets to ensure uniqueness
    IndexCol = set(IndexCol)
    IndexRow = set(IndexRow)

    # Initialize a 2D list (matrix) to represent the heatmap
    HeatMap = [[0 for _ in range(len(IndexRow))] for _ in range(len(IndexCol))]
    
    # Populate the heatmap matrix with trade counts
    for index, i in enumerate(DensityMap.index):
        HeatMap[i[0] - min(IndexCol)][i[1] - min(IndexRow)] = DensityMap.iloc[index]
    
    # Append the heatmap matrix to the list of heatmaps
    HeatMaps1.append(HeatMap)

# Convert each heatmap matrix into a pandas DataFrame
for index, HeatMap in enumerate(HeatMaps1):
    HeatMaps1[index] = pd.DataFrame(HeatMap)

# Adjust the index of each DataFrame to reflect the actual trading hours
for index, HeatMap in enumerate(HeatMaps1):
    HeatMaps1[index].index = [i + 9 for i in HeatMap.index]

# Display the heatmap for Day 3 with a color gradient
HeatMaps1[2].T.style.background_gradient(cmap='coolwarm')

# Repeat the process for trade size heatmaps
HeatMaps2 = []
for k in range(1, 6):
    # Group the DataFrame by 'Hour' and 'Minute' and sum the trade sizes
    DensityMap = df[(df['Day'] == k)].groupby(["Hour", "Minute"])['SIZE'].sum()
    
    # Initialize lists to store unique hours and minutes
    IndexCol = []
    IndexRow = []
    
    # Populate the lists with unique hours and minutes
    for i in DensityMap.index:
        IndexCol.append(i[0])
        IndexRow.append(i[1])
    
    # Convert lists to sets to ensure uniqueness
    IndexCol = set(IndexCol)
    IndexRow = set(IndexRow)

    # Initialize a 2D list (matrix) to represent the heatmap
    HeatMap = [[0 for _ in range(len(IndexRow))] for _ in range(len(IndexCol))]
    
    # Populate the heatmap matrix with trade sizes
    for index, i in enumerate(DensityMap.index):
        HeatMap[i[0] - min(IndexCol)][i[1] - min(IndexRow)] = DensityMap.iloc[index]
    
    # Append the heatmap matrix to the list of heatmaps
    HeatMaps2.append(HeatMap)

# Convert each heatmap matrix into a pandas DataFrame
for index, HeatMap in enumerate(HeatMaps2):
    HeatMaps2[index] = pd.DataFrame(HeatMap)

# Adjust the index of each DataFrame to reflect the actual trading hours
for index, HeatMap in enumerate(HeatMaps2):
    HeatMaps2[index].index = [i + 9 for i in HeatMap.index]

# Display the heatmap for Day 3 with a color gradient
HeatMaps2[2].T.style.background_gradient(cmap='coolwarm')

# The last line seems to be incomplete or out of context
# new_x["Low"]

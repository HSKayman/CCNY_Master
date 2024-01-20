#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Requirment Library
import pandas as pd
from datetime import date
from datetime import datetime
import matplotlib.pylab as plt


# In[2]:


# Read CSV file into a DataFrame I selected this because it is hardest of them. :)
df = pd.read_csv("Day4_Trades_SPY.csv")
df


# In[3]:


# General checking: Describes numerical features
df.describe()


# In[4]:


# Data Type Checking: Convert 'Time' column to datetime format
df.dtypes


# In[5]:


# Eliminate nanoseconds and convert 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time']).dt.floor('ns')


# In[6]:


# Verify the column types after conversion
df.dtypes


# In[7]:


# Convert 'PARTICIPANT_TIME' column to datetime format
df['PARTICIPANT_TIME'] = pd.to_datetime(df['PARTICIPANT_TIME']).dt.floor('ns')


# In[8]:


# Verify the column types after conversion
df.dtypes


# In[9]:


df.head()


# In[10]:


# Reset the DataFrame index
df = df.reset_index()
df


# # 1

# # What happened to price over the course of the day?

# In[11]:


# Group by 'EXCHANGE' and describe the 'PRICE' column
df.groupby('EXCHANGE')['PRICE'].describe()


# # How much did it change overall, and in what direction? 

# In[12]:


# Calculate the difference between the first and last prices for each exchange
df_diff_Price=pd.merge(df.groupby('EXCHANGE')['PRICE'].first(), df.groupby('EXCHANGE')['PRICE'].last(), on='EXCHANGE')
df_diff_Price["difference"]=df_diff_Price["PRICE_y"]-df_diff_Price["PRICE_x"]
df_diff_Price["isUp"]= df_diff_Price["difference"] > 0
df_diff_Price


# In[13]:


# All Currencies increased except that "M"
#if difference is Negative, it means it decrased. if not, it means it increased


# # When was it changing fastest?

# In[14]:


times = pd.to_datetime(df.Time)
df['Hour']=times.dt.hour
df['Minute']=times.dt.minute


# In[15]:


# Create a DataFrame to store open, low, high, close, volume, and count for each exchange and hour
OpenCloseTablePerHour = {}
Index=df.Hour.unique()
OpenCloseTablePerHour["Currency"] = []
IndexForPandas=[]
OpenCloseTablePerHour["Open"] = []
OpenCloseTablePerHour["Low"] = []
OpenCloseTablePerHour["High"] = []
OpenCloseTablePerHour["Close"] = []
OpenCloseTablePerHour["Volume"] = []
OpenCloseTablePerHour["Count"] = []

# Populate the DataFrame with values for each exchange and hour
for i in df.EXCHANGE.unique():
    for j in Index:
        Open = 0
        Low = 0
        High = 0
        Close = 0
        Volume = 0
        Count = 0

        try:
            Open = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['PRICE'].iloc[0]
        except IndexError:
            Open = 0

        OpenCloseTablePerHour["Open"].append(Open)

        try:
            Low = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['PRICE'].min()
        except ValueError:
             Low = 0

        OpenCloseTablePerHour["Low"].append(Low)

        try:
            High = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['PRICE'].max()
        except ValueError:
            High = 0

        OpenCloseTablePerHour["High"].append(High)

        try:
            Close = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['PRICE'].iloc[-1]
        except IndexError:
            Close = 0

        OpenCloseTablePerHour["Close"].append(Close)

        try:
            Volume = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['SIZE'].sum()
        except ValueError:
            Volume = 0
        
        OpenCloseTablePerHour["Volume"].append(Volume)
        
        try:
            Count = df[(df['EXCHANGE'] == i) & (df['Hour'] == j)]['PRICE'].count()
        except ValueError:
            Count = 0

        OpenCloseTablePerHour["Count"].append(Count)
        
        OpenCloseTablePerHour["Currency"].append(i)
        IndexForPandas.append(j)
     


# In[16]:


OpenCloseTablePerHour = pd.DataFrame(OpenCloseTablePerHour,index=IndexForPandas)
OpenCloseTablePerHour


# In[17]:


OpenCloseTablePerHour=OpenCloseTablePerHour.dropna(axis=0)
OpenCloseTablePerHour


# In[18]:


for i in OpenCloseTablePerHour['Currency'].unique():
    OpenCloseTablePerHour[(OpenCloseTablePerHour['Currency'] == i)]


# In[19]:


# plot
fig, ax = plt.subplots(figsize=(20, 10))
for currency in OpenCloseTablePerHour['Currency'].unique():
    plotedFrame = OpenCloseTablePerHour[(OpenCloseTablePerHour['Currency'] == currency)]
    x=plotedFrame.index
    yDown=plotedFrame['Low']
    yUp=plotedFrame['High']
    ax.fill_between(x, yDown, yUp, alpha=.5, linewidth=0)
    ax.plot(x, (yDown + yUp)/2, linewidth=2, label=currency)
plt.legend()
plt.show()


# In[20]:


OpenCloseTablePerHour["Difference"]=abs(OpenCloseTablePerHour['Low']-OpenCloseTablePerHour['High'])


# In[21]:


OpenCloseTablePerHour.groupby(["Currency"])['Difference'].idxmax()


# In[22]:


OpenCloseTablePerHour.groupby(["Currency"])['Difference'].last()


# In[23]:


# So 15:00 - 15:59:59 is so hight changing.


# In[24]:


df.plot(x='Hour',y='PRICE')


# # When was holding mostly steady (if at all)?

# In[25]:


OpenCloseTablePerHour.groupby(["Currency"])['Difference'].idxmin()


# In[26]:


# Mostly 11:00-11:59:59


# In[27]:


OpenCloseTablePerHour.groupby(["Currency"])['Volume'].idxmin()


# # 2

# # What happened to sizes of individual trades over the course of the day?

# In[28]:


OpenCloseTablePerHour[["Currency",'Volume']]


# In[29]:


OpenCloseTablePerHour.groupby("Currency")['Volume'].describe()


# In[30]:


# plot
fig, ax = plt.subplots(figsize=(20, 10))
for currency in OpenCloseTablePerHour['Currency'].unique():
    plotedFrame = OpenCloseTablePerHour[(OpenCloseTablePerHour['Currency'] == currency)]
    x=plotedFrame.index
    y=plotedFrame["Volume"]
    ax.plot(x, y, linewidth=2, label=currency)
plt.legend()
plt.show()


# In[31]:


# "T" is so high and of course it has really big correlasion with price diff.


# In[32]:


corr = OpenCloseTablePerHour.corr()
corr.style.background_gradient(cmap='coolwarm')


# In[33]:


# probaly I am wrong


# # Does trade size seem correlated with time of day at all in your opinion?
# 

# In[34]:


# saying something is hard because definetly there is realition on 15:00 this hour has maximum difference and maximum volume :)


# In[35]:


OpenCloseTablePerHour.groupby("Currency")['Volume'].idxmax()


# In[36]:


# saying something is hard because definetly there is realition on 15:00 this hour has maximum difference and maximum volume :)


# # 3

# # What happened to the rate of trading throughout the day?

# In[37]:


OpenCloseTablePerHour.groupby(["Currency"])["Count"].idxmax()


# In[38]:


# of course if its volume is high, its count would be high too 


# # What was the greatest number of trades per minute?

# In[39]:


#df.groupby([pd.Grouper(key = 'Time', freq='1min'), 'EXCHANGE']).count()
(df.groupby([pd.Grouper(key = 'Time', freq='1min')]).count()['index'].idxmax(),df.groupby([pd.Grouper(key = 'Time', freq='1min')]).count()['index'].max())


# In[40]:


#Here We Go below time has maximum Number Of Trade :) 26,518 :)))


# # Per second?

# In[41]:


(df.groupby([pd.Grouper(key = 'Time', freq='1s')]).count()['index'].idxmax(),df.groupby([pd.Grouper(key = 'Time', freq='1s')]).count()['index'].max())


# # How did the density of trading activity vary throughout the day?

# In[42]:


DensityMap=df.groupby(["Hour","Minute"]).count()['index']
DensityMap


# In[43]:


IndexCol=[]
IndexRow=[]
for i in DensityMap.index:
    IndexCol.append(i[0])
    IndexRow.append(i[1])
IndexCol=set(IndexCol)
IndexRow=set(IndexRow)
HeatMap=[[0 for i in range(len(IndexRow))] for i in range(len(IndexCol))]
for index,i in enumerate(DensityMap.index):
    HeatMap[i[0]-min(IndexCol)][i[1]-min(IndexRow)]=DensityMap.iloc[index]


# In[44]:


HeatMap = pd.DataFrame(HeatMap)


# In[45]:


HeatMap.index=[i+9 for i in HeatMap.index]


# In[46]:


HeatMap.style.background_gradient(cmap='coolwarm')


# In[ ]:





# # 1.What happened to price over the course of the day? How much did it change overall, and in what direction? When was it changing fastest? When was holding mostly steady (if at all)? 
# 
# # 2. What happened to sizes of individual trades over the course of the day? Does trade size seem correlated with time of day at all in your opinion?
# 
# # 3. What happened to the rate of trading throughout the day? What was the greatest number of trades per minute? Per second? How did the density of trading activity vary throughout the day?

# In[47]:


#1


# In[48]:


#What happened to price over the course of the day?
df.groupby('EXCHANGE')['PRICE'].describe()


# In[49]:


#How much did it change overall, and in what direction?
df_diff_Price


# In[50]:


#When was it changing fastest? (Below Shows Hour)
OpenCloseTablePerHour.groupby(["Currency"])['Difference'].idxmax()


# In[51]:


#When was holding mostly steady (if at all)? (Below Shows Hour) 
OpenCloseTablePerHour.groupby(["Currency"])['Difference'].idxmin()


# In[52]:


#2


# In[53]:


#What happened to sizes of individual trades over the course of the day?
OpenCloseTablePerHour.groupby("Currency")['Volume'].sum()


# In[54]:


#Does trade size seem correlated with time of day at all in your opinion?
corr.style.background_gradient(cmap='coolwarm')


# In[55]:


#3


# In[56]:


#What happened to the rate of trading throughout the day?
OpenCloseTablePerHour.groupby(["Currency"])["Count"].idxmax()


# In[57]:


#What was the greatest number of trades per minute? 
(df.groupby([pd.Grouper(key = 'Time', freq='1min')]).count()['index'].idxmax(),df.groupby([pd.Grouper(key = 'Time', freq='1min')]).count()['index'].max())


# In[58]:


#Per second?
(df.groupby([pd.Grouper(key = 'Time', freq='1s')]).count()['index'].idxmax(),df.groupby([pd.Grouper(key = 'Time', freq='1s')]).count()['index'].max())


# In[59]:


#How did the density of trading activity vary throughout the day?
HeatMap.style.background_gradient(cmap='coolwarm')


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[22]:


#Import Requirment Library
import pandas as pd
from datetime import date
from datetime import datetime
import matplotlib.pylab as plt


# In[23]:


#Read All Data
dataframes=[]
for day in range(1, 6):
    df = pd.read_csv("Day{}_Trades_SPY.csv".format(day))
    dataframes.append(df)
    


# In[24]:


#Check Columns
dataframes[0].head()


# In[25]:


#Check Columns If there is a date
dataframes[1].head()


# In[26]:


#Add Date in as a new column
for day in range(0, 5):
    dataframes[day]["Day"]=day


# In[27]:


#Concat DataFrames Because Working on would be easier
for day in range(1,5):
    dataframes[0]=pd.concat([dataframes[0], dataframes[day]])


# In[28]:


#Change Variable Name So I dont have to use index :)
MyFrame=dataframes[0]
MyFrame


# In[29]:


#General Checking Describes Of Numerical Features
MyFrame.describe()


# In[30]:


#Data Type Checking Oh No Time is like string I need to convert it
MyFrame.dtypes


# In[31]:


#Here we go, Nano Second damaged Our Converting So I need to eleminate it then convert
MyFrame['Time'] = pd.to_datetime(df['Time']).dt.floor('S')


# In[32]:


#Yes, Types Of Columns are What I want
MyFrame.dtypes


# In[33]:


#Do I Have Index Problem
MyFrame.head()


# In[34]:


#I think so because I must have had about 3M but when I looked Last INdex it was just 231K 
MyFrame.tail()


# In[36]:


#Here We Go Reseting What A Freshing
MyFrame = MyFrame.reset_index()
MyFrame


# In[38]:


#Day By Day Checking
MyFrame.groupby('Day').describe()


# In[81]:


#According to my fellings, Size doesn't let me know which days close which days far away
MyFrame.groupby('Day')['SIZE'].describe()


# In[83]:


#Checking Volume Day By Day Maybe we will find good knowledge
VOLUME = MyFrame.groupby(['EXCHANGE', 'Day'])['SIZE'].describe()
VOLUME


# In[84]:


#Checking Volume is in Process
for i in MyFrame['EXCHANGE'].unique():
    print((20-len(i))*'-',' ',i,' ',(20-len(i))*'-')
    print(VOLUME.loc[i][:])
    print((40-len(i))*'-')


# In[88]:


#According to my fellings, Price is so changebla. it must be great idea to reilaze which days close which days far away
PRICES = MyFrame.groupby(['EXCHANGE', 'Day'])['PRICE'].describe()
PRICES


# In[89]:


#Checking Price is in Process
for i in MyFrame['EXCHANGE'].unique():
    print((20-len(i))*'-',' ',i,' ',(20-len(i))*'-')
    print(PRICES.loc[i][:])
    print((40-len(i))*'-')


# In[90]:


#We are only evaluating the modem days, we can delete another column so it will be easier for my laptop. 
#But Don't forget If these days includes day after day days, 
#it probaly before close price should be same that day open price or close
MyGraphFrame = MyFrame.drop(['PARTICIPANT_TIME','Time'], axis=1)


# In[91]:


#This Graphs is really helpfull to guess which day close which not
MyGraphFrame.boxplot(column=['PRICE'], by=['Day', 'EXCHANGE'])

plt.rcParams['figure.figsize'] = [50, 20]
plt.rcParams['figure.dpi'] = 100 
plt.show()


# In[92]:


#as I said, Size doesnt give an idea to guess
MyGraphFrame.boxplot(column=['SIZE'], by=['Day', 'EXCHANGE'])

plt.rcParams['figure.figsize'] = [50, 20]
plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower
plt.show()


# # Give some summary statistics describing each days’ worth of data ?

# In[93]:


MyFrame.groupby('Day').describe()


# # Q: Investigate whatever properties of the data you find interesting ?

# ### Answer:
# ### Price is striking

# # Q: Do any of these days seem “unusual” in any sense compared to the others? Do you think any of these might represent days that are close together in time? Do you think any of these might represent days that are very far apart in time? Explain your reasoning. 

# ### Answer:
# ### Yes, Day 4 is clearly a different day. This day's data should be separate from other days. also its range is pretty large.
# ### (Day 2 and Day 3) are reasonably close to each other.
# ### (Day 1 and Day 5) may be close days. Even though day 5 and day 1 are not as close as day 2 and day 3. 
# ### I relaized Thoose From below Boxplot

# In[97]:


MyGraphFrame.boxplot(column=['PRICE'], by=['Day', 'EXCHANGE'])

plt.rcParams['figure.figsize'] = [50, 20]
plt.rcParams['figure.dpi'] = 100 
plt.show()


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# # Import Libraries I will use

# In[1]:


import pandas as pd
import numpy as np


# # Read Cvs

# In[2]:


df = pd.read_csv("VolumeAndNVbySymbol_wRand.csv")


# # The average value of each numerical column
# But firstly we need to know datatypes of columns

# In[3]:


df.dtypes


# # 1) We need to find averages of NV_rand * VOLUME_rand

# In[4]:


df['VOLUME_rand * NV_rand']=df['NV_rand']*df['VOLUME_rand']


# In[5]:


WeightedAverage=(df['VOLUME_rand * NV_rand']).sum()/df['NV_rand'].sum()


# In[6]:


WeightedAverage


# # 2) We need to sort them so it will be easy to eliminate first %5, last %5

# In[7]:


Sorted_df=df.sort_values(by='VOLUME_rand', ascending=True)


# In[8]:


NumberOfRows=len(df)
NumberOfRows


# In[9]:


NumberOfElements = NumberOfRows - int(NumberOfRows*0.05)


# In[10]:


HighestAverage = Sorted_df.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df.tail(NumberOfElements)['NV_rand'].sum()
i=NumberOfRows
while i>= NumberOfElements:
    isHighestAverage = Sorted_df.tail(i)['VOLUME_rand * NV_rand'].sum()/Sorted_df.tail(i)['NV_rand'].sum()
    if isHighestAverage > HighestAverage:
        HighestAverage = isHighestAverage
    i-=1


# In[11]:


HighestAverage


# In[12]:


LowestAverage = Sorted_df.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df.head(NumberOfElements)['NV_rand'].sum()
i=NumberOfRows
while i>= NumberOfElements:
    isLowestAverage = Sorted_df.head(i)['VOLUME_rand * NV_rand'].sum()/Sorted_df.head(i)['NV_rand'].sum()
    if isLowestAverage < LowestAverage:
        LowestAverage = isLowestAverage
    i-=1


# In[13]:


LowestAverage


# In[14]:


forGraph = pd.DataFrame({'Highest Average':[HighestAverage],
                       'Normal Average':[WeightedAverage],
                     'Lowest Average':[LowestAverage]})
forGraph.plot.bar()


# # Distance of normal to lowest is high. Distance of highest to normal is low because this series in that point has dense.

# In[29]:


df['VOLUME_rand * NV_rand'].plot.box()


# # 3) We need to do someting complex 

# In[15]:


GroupedByDf=df.groupby(['SYMBOL_NAME']).sum()


# In[16]:


GroupedByDf['AveragePerSymbol']=GroupedByDf['VOLUME_rand * NV_rand']/GroupedByDf['NV_rand']


# In[17]:


GroupedByDf['Relaitive Weight']=GroupedByDf['AveragePerSymbol']*100/GroupedByDf['AveragePerSymbol'].sum()


# In[18]:


GroupedByDf.head()


# # I couldn't understand , "do you get the same result as 1? Discuss why or why not." But I am sure that usually averages are not same each other because all Symbol has different value If you mean that, i did sum of w*x is 1.

# # So Answers

# In[19]:


pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.set_option('display.float_format', lambda x: '%.10f' % x)


# In[20]:


print("1)The weighted average of VOLUME_rand over the whole dataset, using NV_rand as the weights :"+str(WeightedAverage))
print("2)The averages of values :")
print("\t Highest: \t"+str(HighestAverage))
print("\t Lowest: \t"+str(LowestAverage))
print("3)The weighted average of VOLUME_rand over the whole dataset, using NV_rand as the weights for each Symbol:\n\n\n", GroupedByDf[['AveragePerSymbol','Relaitive Weight']])
print("Sum of all Relaitive Weight always is 1 because its mechanism. Sum =",GroupedByDf['Relaitive Weight'].sum()/100)


# # The END

# In[ ]:





# In[ ]:





# # I taught it can be solved by greedy knapsnack algorithm because we want to make weight high, weight*xi low for smallest mean but it doesn't work, you can see my some test below. ahahahahha

# In[21]:


df1=df.copy()


# In[22]:


df1['x']=df1['VOLUME_rand']
Sorted_df1=df1.sort_values(by='x', ascending=True)
NumberOfElements1 = NumberOfRows - int(NumberOfRows*0.05)
HighestAverage1 = Sorted_df1.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.head(NumberOfElements)['NV_rand'].sum()
LowestAverage1 = Sorted_df1.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.tail(NumberOfElements)['NV_rand'].sum()
[LowestAverage1,HighestAverage1]


# In[23]:


df1['x']=df1['NV_rand']
Sorted_df1=df1.sort_values(by='x', ascending=True)
NumberOfElements1 = NumberOfRows - int(NumberOfRows*0.05)
HighestAverage1 = Sorted_df1.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.head(NumberOfElements)['NV_rand'].sum()
LowestAverage1 = Sorted_df1.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.tail(NumberOfElements)['NV_rand'].sum()
[LowestAverage1,HighestAverage1]


# In[24]:


df1['x']=df1['NV_rand']/df1['VOLUME_rand']
Sorted_df1=df1.sort_values(by='x', ascending=True)
NumberOfElements1 = NumberOfRows - int(NumberOfRows*0.05)
HighestAverage1 = Sorted_df1.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.head(NumberOfElements)['NV_rand'].sum()
LowestAverage1 = Sorted_df1.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.tail(NumberOfElements)['NV_rand'].sum()
[LowestAverage1,HighestAverage1]


# In[25]:


df1['x']=df1['VOLUME_rand']/df1['NV_rand']
Sorted_df1=df1.sort_values(by='x', ascending=True)
NumberOfElements1 = NumberOfRows - int(NumberOfRows*0.05)
HighestAverage1 = Sorted_df1.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.head(NumberOfElements)['NV_rand'].sum()
LowestAverage1 = Sorted_df1.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.tail(NumberOfElements)['NV_rand'].sum()
[LowestAverage1,HighestAverage1]


# In[26]:


df1['x']=df1['VOLUME_rand']/df1['NV_rand'].sum() #OH MY GOD, BLESSING NOW This is like same normal volume :)
Sorted_df1=df1.sort_values(by='x', ascending=True)
NumberOfElements1 = NumberOfRows - int(NumberOfRows*0.05)
HighestAverage1 = Sorted_df1.head(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.head(NumberOfElements)['NV_rand'].sum()
LowestAverage1 = Sorted_df1.tail(NumberOfElements)['VOLUME_rand * NV_rand'].sum()/Sorted_df1.tail(NumberOfElements)['NV_rand'].sum()
[LowestAverage1,HighestAverage1]


# In[27]:


print("\t Highest: \t"+str(HighestAverage))
print("\t Lowest: \t"+str(LowestAverage))


# In[ ]:





# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# # Import Libraries I will use

# In[5]:


import pandas as pd
import numpy as np


# # Read Cvs

# In[6]:


df = pd.read_csv("VolumeAndNVbySymbol_wRand.csv")


# # Find The number of rows in the sample data set

# In[13]:


NumberOfRows=len(df)
NumberOfRows


# # The average value of each numerical column
# But firstly we need to know datatypes of columns

# In[10]:


df.dtypes


# # We need to find averages of NV_rand and VOLUME_rand

# In[14]:


AveragesOfColumns=[df['NV_rand'].mean(),df['VOLUME_rand'].mean()]
AveragesOfColumns


# In[17]:


df.plot.box() # sounds like it includes some thresholds rows :)


# # The min and max values of a time-based column

# In[40]:


pd.options.display.max_rows = None
pd.options.display.max_columns = None


# In[42]:


MinMaxTable=df.groupby(['Time']).agg({'NV_rand' : ['count', 'min', 'max'], 'VOLUME_rand' : ['min', 'max']})
MinMaxTable


# # So Answers

# In[56]:


print("1)Number Of Rows :"+str(NumberOfRows))
print("2)The average value :")
print("\t NV_rand: \t"+str(AveragesOfColumns[0]))
print("\t VOLUME_rand: \t"+str(AveragesOfColumns[1]))
print("3)The min and max values of a time-based column:\n\n\n", MinMaxTable)


# In[ ]:





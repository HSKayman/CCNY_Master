# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:17:16 2023

@author: HSK
"""


import numpy as np
import pandas as pd
import time
from tensorflow import keras

def print_weights(weights):
    print('\n******* WEIGHTS OF ANN *******\n') 
    for i in range(int(len(weights)/2)):
        print('Weights W%d:\n' %(i), weights[i*2])
        print('Bias b%d:\n' %(i), weights[(i*2)+1])


historical_data_file="GOOG.csv"

# Load historical stock data 
df=pd.read_csv(historical_data_file)

# Retain only the closing prices 
df = df[["Close"]]
short_window = 5
long_window = 25

# Calculate the Simple Moving Average and add it to a new column in df
df['SMA'] = df.rolling(short_window).mean()

# Calculate the Exponential Moving Average and add it to a new column in df
df['EMA'] = df['Close'].ewm(span=long_window).mean()

# Calculate the Momentum and add it to a new column in df
df['Momentum'] = df['Close'] / df['Close'].shift(short_window)

# Calculate the standard deviation of SMA over a rolling window
df['STD'] = df['Close'].rolling(short_window).std(ddof=0)

# Calculate the Bollinger Band for each day
df['BB'] = (df['Close'] - df['SMA']) / (2 * df['STD'])

# Calculate William's %R for each day
increase = df['Close'] / df['Close'].shift(1)
df['Percent_Change'] = (increase / df['Close'].shift(1)) * 100

# Calculate the percent change of closing price for each day
df['Percent_Change'] = df['Percent_Change'].shift(-1)

# Start training ANN using the df file containing historical data and information
print('\n\n********* NOW START TRAINING ANN USING', historical_data_file,'*********')
time.sleep(3)

# Remove rows with invalid inputs (i.e., nan) and create input and output arrays for ANN
X = np.array(df[long_window:-1][['SMA', 'EMA', 'Momentum', 'STD', 'BB', 'Close']])
Y = np.array(df[long_window:-1]['Percent_Change'])

# Create a model for the ANN
model = keras.Sequential()

# Create ANN with 6 inputs + 2 hidden layers + 1 output layer
model.add(keras.layers.Dense(50, activation='relu', input_shape=(6,)))
model.add(keras.layers.Dense(50, activation='relu'))
model.add(keras.layers.Dense(50, activation='relu'))
model.add(keras.layers.Dense(1, activation='linear'))

# Set the optimization algorithm used for minimizing loss function
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the ANN model using 200 epochs
model.fit(X, Y, epochs=200)
weights=model.get_weights()
print_weights(weights)
print('\n\n********** ANN training complete **********\n\n')

# Insert the inputs for the latest trading day into an array
latest_SMA = df.iloc[-1]['SMA'] 
latest_EMA = df.iloc[-1]['EMA']
latest_Momentum = df.iloc[-1]['Momentum'] 
latest_BB = df.iloc[-1]['BB']
latest_STD = df.iloc[-1]['STD']

latest_inputs = np.array([[latest_SMA, latest_EMA, latest_Momentum, latest_STD, latest_BB, df.iloc[-1]['Close']]])

# Make predictions using the trained model
prediction = model.predict(latest_inputs)[0,0]

print('\n***************************************')
print('ANN Predicted Next Day Stock Movement: %+.2f%%' % (prediction))
print('***************************************')

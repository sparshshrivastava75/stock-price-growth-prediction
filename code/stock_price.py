# -*- coding: utf-8 -*-
"""stockprice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uq1y1JAZ79H6YGlOxDLcI9McjMxiZuPZ
"""

pip install pmdarima

import pandas as pd
import numpy as np
import math
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('/content/NYKAA.NS.csv',index_col='Date',parse_dates = True)
df = df.dropna()
print('Shape of data',df.shape)
df.head()

plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Year',fontsize=18)
plt.ylabel('Close Price INR',fontsize=18)
plt.show()

data = df.filter(['Close'])
dataset = data.values
training_data_len=math.ceil(len(dataset)*.8)

training_data_len

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data =  scaler.fit_transform(dataset)
scaled_data

train_data  =scaled_data[0:training_data_len,:]
x_train = []
y_train = []

for i in range(60,len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])
  if  i<=61:
    print(x_train)
    print(y_train)
    print()

x_train,y_train = np.array(x_train),np.array(y_train)

x_train = np.reshape(x_train,(x_train.shape[0], x_train.shape[1],1))
x_train.shape

model = Sequential()
model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences = False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mean_squared_error')

#train model
model.fit(x_train,y_train,batch_size=1,epochs=1)

test_data = scaled_data[training_data_len - 60:,:]
x_test=[]
y_test = dataset[training_data_len:,:]
for i in range(60,len(test_data)):
  x_test.append(test_data[i-60:i,0])

x_test  = np.array(x_test)

x_test= np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions']=predictions
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.legend(['Train','Original','Predictions'],loc='lower right')
plt.show()

rmse=np.sqrt(np.mean(predictions - y_test)**2)
rmse
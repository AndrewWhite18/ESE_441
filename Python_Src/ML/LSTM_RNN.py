import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.recurrent import LSTM
from keras.layers import Dropout
import matplotlib.ticker as mtick
import plotly as py
import plotly.graph_objs as go


# Import csv file
d = pd.read_csv('dow_ml_confusion_date.csv')
data_csv = d.drop(['date'], 1)


# Number of rows
total_data = len(data_csv)

# split training/test into 80/20
train_end = round(0.8 * total_data)

# most recent data is in the end
start = total_data - total_data

# data from csv
close = data_csv.iloc[start:total_data, 0]  # Close price
cp1 = data_csv.iloc[start:total_data, 1]  # close -1
cp2 = data_csv.iloc[start:total_data, 2]  # close -2
cp3 = data_csv.iloc[start:total_data, 3]  # close -3
f1 = data_csv.iloc[start:total_data, 4]  # mood state 1
f2 = data_csv.iloc[start:total_data, 5]  # mood state 2
f3 = data_csv.iloc[start:total_data, 6]  # mood state 3


# demo sample of close price to console
print("close head (first five) :")
print(close.head())

#current close is label. Past 3 days of stock data/moods data are features
data = pd.concat([close, cp1, cp2, cp3, f1, f2, f3], axis=1)
#data = pd.concat([close, cp1, cp2, cp3], axis=1)

data.columns = ['close', 'close-1', 'close-2', 'close-3', 'mood-1', 'mood-2', 'mood-3']
#data.columns = ['close', 'close-1', 'close-2', 'close-3']

#get rid of any N/A values
data = data.dropna()
#print to console
print(data)

# Label (target) - close price
y = data['close']
# features - past 3 days of close price, past 3 days of mood
features = ['close-1', 'close-2', 'close-3', 'mood-1', 'mood-2', 'mood-3']
#features = ['close-1', 'close-2', 'close-3']

x = data[features]

#scale x
scaler_x = preprocessing.MinMaxScaler(feature_range=(-1, 1))
x = np.array(x).reshape((len(x), len(features)))
x = scaler_x.fit_transform(x)

#scale y
scaler_y = preprocessing.MinMaxScaler(feature_range=(-1, 1))
y = np.array(y).reshape((len(y), 1))
y = scaler_y.fit_transform(y)

#split into training and test
x_train = x[0: train_end, ]
x_test = x[train_end + 1:len(x), ]
y_train = y[0: train_end]
y_test = y[train_end + 1:len(y)]
x_train = x_train.reshape(x_train.shape + (1,))
x_test = x_test.reshape(x_test.shape + (1,))

# Build the LSTM RNN model
seed = 2016
np.random.seed(seed)
fit1 = Sequential()
fit1.add(LSTM(150, activation='tanh', inner_activation='hard_sigmoid', input_shape=(len(features), 1), return_sequences=True))
fit1.add(Dropout(0.2))
fit1.add(LSTM(75, activation='tanh', inner_activation='hard_sigmoid', input_shape=(len(features), 1), return_sequences=False))
fit1.add(Dropout(0.2))
fit1.add(Dense(35, init='uniform', activation='linear'))
fit1.add(Dense(1, init='uniform', activation='linear'))
"""
fit1.add(LSTM(100, activation='tanh', inner_activation='hard_sigmoid', input_shape=(len(cols), 1)))
fit1.add(Dropout(0.2))
fit1.add(Dense(output_dim=1, activation='linear'))
"""
fit1.compile(loss="mean_squared_error", optimizer="adam")
fit1.fit(x_train, y_train, batch_size=8, nb_epoch=20, shuffle=False)
# Print RNN summary
print(fit1.summary())

score_train = fit1.evaluate(x_train, y_train, batch_size=1)
score_test = fit1.evaluate(x_test, y_test, batch_size=1)
print(" in train MSE = ", round(score_train, 4))
print(" in test MSE = ", score_test)

pred1 = fit1.predict(x_test)
pred1 = scaler_y.inverse_transform(np.array(pred1).reshape((len(pred1), 1)))

#prediction_data = pred1[-1]

fit1.summary()
print("Inputs: {}".format(fit1.input_shape))
print("Outputs: {}".format(fit1.output_shape))
print("Actual input: {}".format(x_test.shape))
print("Actual output: {}".format(y_test.shape))

# summary of prediction
#print("prediction data:")
#print(pred1)
# summary of actual
print("Test data")
x_test = scaler_x.inverse_transform(np.array(x_test).reshape((len(x_test), len(features))))
print("X Test", x_test)
y_test = scaler_y.inverse_transform(np.array(y_test).reshape((len(y_test), 1)))
print("Y Test", y_test)
print("Prediction data:")
print("Predictions:", pred1)

# Find direction accuracy
correct = 0
direction_accuracy = 0

for i in range(1, len(pred1)):
    if ((y_test[i] > y_test[i - 1] and pred1[i] > pred1[i - 1]) or (
            y_test[i] < y_test[i - 1] and pred1[i] < pred1[i - 1])):
        correct += 1

direction_accuracy = 100 * (correct / (len(pred1) - 1))
direction_accuracy = round(direction_accuracy, 2)
mse_accuracy = 100 * score_test
mse_accuracy = round(mse_accuracy, 2)

# plot (plotly and matplotlib)
mood_used = 'Confusion'
plt.suptitle('Actual vs Predictions using ' + mood_used, fontsize=10)
plt.title("MSE: " + str(mse_accuracy) + "%\nDirection: " + str(direction_accuracy) + "%", fontsize=8)
plt.plot(pred1, label="predictions")
plt.plot([row[0] for row in y_test], label="actual")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
           fancybox=True, shadow=True, ncol=2)

fmt = '$%.0f'
tick = mtick.FormatStrFormatter(fmt)

ax = plt.axes()
ax.yaxis.set_major_formatter(tick)


a = [row[0] for row in y_test.tolist()]
p = [row[0] for row in pred1.tolist()]
dates = d['date']
dates = dates[train_end + 1:len(y)]

dff = pd.DataFrame(
    {'actual': a,
     'predictions': p,
     'date': dates
    })

preds = go.Scatter(
                x=dff['date'],
                y=dff['predictions'],
                name = 'Prediction',
                line = dict(color = '#ffff1a'),
                opacity = 0.8)

acts = go.Scatter(
                x=dff['date'],
                y=dff['actual'],
                name = 'Actual',
                line = dict(color = '#006600'),
                opacity = 0.8)


layout = dict(
    title = 'Actual vs Predictions using ' + mood_used + "<br>MSE: " + str(mse_accuracy) + "%<br>Direcion: " + str(direction_accuracy) + "%",
    annotations=[
            dict(
                x=.5,
                y=1,
                xref='paper',
                yref='paper',
                text='***Subtitle****',
                showarrow=False,
                align='center',
                font=dict(
                size=8,
                color='#ffffff'
            ),
            )
        ]
)

data = [preds, acts]

fig = dict(data=data, layout=layout)
py.offline.plot(fig, filename = mood_used + "_Predictions")

plt.show()

"""
anger #ff1a1a
depression #ff9933
confusion #ffff1a
anxiety #33ff33
happy #3333ff
calm #cc66ff
polarity #7300e6
"""
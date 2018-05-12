import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout
from sklearn.preprocessing import MinMaxScaler


import pandas as pd

df = pd.read_csv("plot_moods.csv")
df2 = df.drop(['date'], 1)

mood = 'polarity'
mood_title = 'Polarity'

# Scale data
scaler = MinMaxScaler()
#df2[df2.columns] = scaler.fit_transform(df2[df2.columns])
df2[[mood, 'dow_close']] = scaler.fit_transform(df2[[mood, 'dow_close']])

anger = go.Scatter(
                x=df['date'],
                y=df2['anger'],
                name = "Anger",
                line = dict(color = '#ff1a1a'),
                opacity = 0.8)


depression = go.Scatter(
                x=df['date'],
                y=df2['depression'],
                name = "Depression",
                line = dict(color = '#ff9933'),
                opacity = 0.8)

confusion = go.Scatter(
                x=df['date'],
                y=df2['confusion'],
                name = "Confusion",
                line = dict(color = '#ffff1a'),
                opacity = 0.8)

anxiety = go.Scatter(
                x=df['date'],
                y=df['anxiety'],
                name = "Anxiety",
                line = dict(color = '#33ff33'),
                opacity = 0.8)

happy = go.Scatter(
                x=df['date'],
                y=df2['happy'],
                name = "Happy",
                line = dict(color = '#3333ff'),
                opacity = 0.8)

calm = go.Scatter(
                x=df['date'],
                y=df2['calm'],
                name = "Calm",
                line = dict(color = '#cc66ff'),
                opacity = 0.8)

polarity = go.Scatter(
                x=df['date'],
                y=df2['polarity'],
                name = "Polarity",
                line = dict(color = '#7300e6'),
                opacity = 0.8)

dow_close = go.Scatter(
                x=df['date'],
                y=df2['dow_close'],
                name = "DIJA",
                line = dict(color = '#006600'),
                opacity = 0.8)

#data = [anger, depression, confusion, anxiety, happy, calm, polarity]
data = [polarity, dow_close]


layout = dict(title = mood_title + " vs DIJA")
fig = dict(data=data, layout=layout)
py.offline.plot(fig, filename = mood + "_DIJA")


"""
df = pd.read_csv("plot_moods.csv")

py.offline.plot({
"data": [
go.Scatter(x=df['date'], y=df['delta'])

],
"layout": Layout(
    title="Dow Delta Time Series"
)
})

anger #ff1a1a
depression #ff9933
confusion #ffff1a
anxiety #33ff33
happy #3333ff
calm #cc66ff
polarity #7300e6
total_tweets
"""
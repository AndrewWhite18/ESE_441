import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout

import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import grangercausalitytests

df = pd.read_csv("../scaled_no_interpolate2.csv", parse_dates=["tweet_date"])
df.set_index('tweet_date', inplace=True)

list_lag = ['1', '2', '3', '4', '5', '6', '7']
list_anger = []
list_depression = []
list_confusion = []
list_anxiety = []
list_calm = []
list_happy = []
list_polarity = []

#dictionary of lists
mood_dict_p = {'anger': list_anger, 'depression': list_depression, 'confusion': list_confusion, 'anxiety': list_anxiety, 'happy': list_happy, 'calm': list_calm, 'polarity': list_polarity}

columns = ['anger', 'depression', 'confusion', 'anxiety', 'happy', 'calm', 'polarity']

#for every mood state, find the granger causality p values
for key, value in enumerate(mood_dict_p.keys()):
    mood = value
    data = np.asarray(df[['delta', mood]])
    granger = grangercausalitytests(data, maxlag=7, verbose=True)
#for every lag, record the p value in the dict list
    for i in granger.keys():
        pF = granger[i][0]['ssr_ftest'][1]
        pChi = granger[i][0]['ssr_chi2test'][1]
        mood_dict_p[mood].append(pF)


new_df = pd.DataFrame(mood_dict_p)

new_df.to_csv('testing_granger_F.csv')









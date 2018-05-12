import psycopg2

#for connecting to the postgresql database
connection_string = "dbname=twitter user=foo_bar123 host=postgres.cb4bwthwzbqq.us-east-2.rds.amazonaws.com password=seniordesign123"
conn = psycopg2.connect(connection_string)
cursor1 = conn.cursor()
cursor2 = conn.cursor()

observed = 0

#this is a list of all observed dates in moody_tweets
dates = ['4/7/2009',
'4/18/2009',
'4/19/2009',
'4/20/2009',
'4/21/2009',
'5/2/2009',
'5/3/2009',
'5/4/2009',
'5/10/2009',
'5/11/2009',
'5/12/2009',
'5/14/2009',
'5/17/2009',
'5/18/2009',
'5/22/2009',
'5/24/2009',
'5/25/2009',
'5/27/2009',
'5/29/2009',
'5/30/2009',
'5/31/2009',
'6/1/2009',
'6/2/2009',
'6/3/2009',
'6/4/2009',
'6/5/2009',
'6/6/2009',
'6/7/2009',
'6/8/2009',
'6/14/2009',
'6/15/2009',
'6/16/2009',
'6/17/2009',
'6/18/2009',
'6/19/2009',
'6/20/2009',
'6/21/2009',
'6/22/2009',
'6/23/2009',
'6/24/2009',
'6/25/2009']


#look at every date in the data
for date in dates:
    anger = 0
    depression = 0
    confusion = 0
    happy = 0
    anxiety = 0
    calm = 0
    polarity = 0
    select_statement = 'select * from moody_tweets2 where date(timestamp) = ' + """'""" + date + """'"""
    cursor1.execute(select_statement)
    matches = cursor1.fetchall()
    #for every tweet on the given date, sum the mood sates found to get the day's sum of mood states
    if matches:
        num_tweets = len(matches)
        for match in matches:
            if match[4] is not None:
                anger += match[4]
            if match[5] is not None:
                depression += match[5]
            if match[6] is not None:
                confusion += match[6]
            if match[7] is not None:
                happy += match[7]
            if match[8] is not None:
                anxiety += match[8]
            if match[9] is not None:
                calm += match[9]
            if match[10] is not None:
                polarity += match[10]
        #commit the sums to the database
        update_statement = 'update time_series2 set anger= ' + str(anger) + ', depression=' + str(depression) + ', happy=' + str(happy) +  ', confusion= ' + str(confusion) + ', anxiety= ' + str(anxiety) + ', calm= ' + str(calm) + ', polarity= ' + str(polarity) + ', total_tweets=' + str(num_tweets) +' where tweet_date= ' + """'""" + date + """'"""
        cursor2.execute(update_statement)
        conn.commit()
        print('updated moods for date: ' + str(date))







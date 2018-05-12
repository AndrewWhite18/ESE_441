#this script is for sentiment alaysis using a custom lexicon

import psycopg2
from psycopg2 import sql
from textblob import TextBlob

#for connecting to the postgresql database
connection_string = "dbname=twitter user=foo_bar123 host=postgres.cb4bwthwzbqq.us-east-2.rds.amazonaws.com password=seniordesign123"
conn = psycopg2.connect(connection_string)
cursor1 = conn.cursor()
cursor2 = conn.cursor()

observed = 0
mood_dict = {'anxiety': 0, 'depression': 0, 'anger': 0, 'confusion': 0, 'calm': 0, 'happy': 0}

cursor1.execute("select * from moody_tweets2")


cursor1.execute("select * from moody_tweets offset 1200")
#all rows in the table
records = cursor1.fetchall()

#look at each row
for record in records:
    id = record[0]
    tweet = record[3]
    #tweet = "OMG! I wish! :) :X :( LMAO! haha!! LOL!"
    tweet = tweet.lower()
    observed += 1
    print(observed)
    #tokenize the tweet
    tokens = TextBlob(tweet)
    words = tokens.words
    if ':)' in tokens.raw:
        words.append(':)')
    if 'XD' in tokens.raw:
        words.append('XD')
    if ':(' in tokens.raw:
        words.append(':(')
    if ':D' in tokens.raw:
        words.append(':D')
    if ';)' in tokens.raw:
        words.append(';)')
    nouns = tokens.noun_phrases
    polarity = tokens.polarity
    #generate select
    word_str = 'select * from lexicon2 where keyword = '
    word_str += """'""" + words[0] + """'"""
    for word in words:
        if word not in nouns:
            word_str += ' OR keyword = ' + """'""" + word + """'"""
    #check the tweet's tokens for a lexicon keyword match
    cursor2.execute(word_str)
    #cursor2.execute('SELECT * from lexicon where keyword = %(statement)s', {'statement': word_str})
    matches = cursor2.fetchall()
    #set all the matching moods to 1 for the current tweet
    #update_statement = 'update moody_tweets set '
    if matches:
        for match in matches:
            #match index 0 is the column corresponding to the mood state
            mood = match[0]
            mood_dict[mood] += 1
            print('matched a keyword for the mood: ' + mood)
            #if mood not in update_statement:
               # update_statement += mood + ' = 1, '
                #print('matched a keyword for the mood: ' + mood)

        update_statement = 'update moody_tweets2 set depression = ' + str(mood_dict['depression']) + ', anxiety = ' + str(mood_dict['anxiety']) \
                           + ', calm = ' + str(mood_dict['calm']) + ', happy = ' + str(mood_dict['happy']) + ', anger = ' + str(mood_dict['anger']) + ', confusion = ' + str(mood_dict['confusion'])

        update_statement = update_statement + ' where id = ' + str(id)
        cursor2.execute(update_statement)
        #cursor2.execute(sql.SQL("UPDATE moody_tweets SET {} = %s WHERE id=%s").format(sql.Identifier(mood)),(1, id))
        conn.commit()
        for key, value in enumerate(mood_dict.keys()):
            mood_dict[value] = 0
    #update the polarity
    cursor2.execute("UPDATE moody_tweets2 SET polarity=%s WHERE id=%s", (polarity, id))
    conn.commit()






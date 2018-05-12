import psycopg2
from datamuse import datamuse


#for connecting to the postgresql database
connection_string = "dbname=twitter user=foo_bar123 host=postgres.cb4bwthwzbqq.us-east-2.rds.amazonaws.com password=seniordesign123"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

dm_api = datamuse.Datamuse()

#Custom Poms Adjectives (adapted from Poms)
list_anxiety = ['Tense', 'Shaky', 'Panicky', 'Uneasy', 'Restless', 'Nervous', 'Anxious']
list_depression=['Unhappy', 'Sorry', 'Sad', 'Blue', 'Hopeless', 'Unworthy', 'Discouraged', 'Lonely', 'Miserable', 'Gloomy', 'Desperate', 'Helpless',
                 'Worthless', 'Terrified', 'Guilty']
list_anger=['Anger', 'Peeved', 'Grouchy', 'Spiteful', 'Annoyed', 'Resentful', 'Bitter', 'Rebellious', 'Deceived', 'Furious']
list_confusion=['Confused', 'Muddled', 'Bewildered', 'Forgetful', 'Uncertain']
list_calm=['Cool', 'Harmonious', 'Placid', 'Serene', 'Smooth', 'Soothing', 'Tranquil', 'Peaceful', 'Undisturbed', 'Quiet']
list_happy=['Lively', 'Active', 'Energetic', 'Cheerful', 'Alert', 'Peppy', 'Carefree', 'Vigorous']


#dictionary of lists
mood_dict = {'anxiety': list_anxiety, 'depression': list_depression, 'anger': list_anger, 'confusion': list_confusion, 'calm': list_calm, 'happy': list_happy}

#first insert all lists into database
for key, value in mood_dict.items():
    for item in value:
        item = item.lower()
        word = item
        cursor.execute(""" INSERT INTO lexicon2 (mood_state, keyword)
        VALUES (%s, %s);
        """,
        (key, word))
        conn.commit()


#fill in missing words by finding synonyms of every POMS term
for key, value in mood_dict.items():
    for item in value:
        synonyms = dm_api.words(rel_syn=item, max=50)
        for syn in synonyms:
            word = syn.get('word')
            cursor.execute(""" INSERT INTO lexicon2 (mood_state, keyword)
            VALUES (%s, %s);
            """,
            (key, word))
            conn.commit()

"""
#find all statistically related words
for key, value in mood_dict.items():
    #for each item in the list
    for item in value:
        #find statistically related words
        related_words = dm_api.words(rel_trg=item, max=20)
        for rw in related_words:
            word = rw.get('word')
            cursor.execute( INSERT INTO lexicon (mood_state, keyword)
            VALUES (%s, %s);
            ,
            (key, word))
            conn.commit()
"""




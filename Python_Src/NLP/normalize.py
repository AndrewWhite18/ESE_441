import psycopg2
import decimal

#for connecting to the postgresql database
connection_string = "dbname=twitter user=foo_bar123 host=postgres.cb4bwthwzbqq.us-east-2.rds.amazonaws.com password=seniordesign123"
conn = psycopg2.connect(connection_string)
cursor1 = conn.cursor()
cursor2 = conn.cursor()


#795 keywords

#70 anxiety
#227 depression
#86 anger
#75 confusion
#190 calm
#147 happy

#scale all occurences to the respective keyword having 100% share of lexicon
# (1 / (mood_keywords / total_keywords)) is the amount to multiply each occurence by to scale the data such that the ratio of kaywords to total words doesn't skew results

dict = {'anxiety' : decimal.Decimal((.1/.088)), 'depression' : decimal.Decimal((.1/.286)), 'anger' : decimal.Decimal((.1/.108)), 'confusion' : decimal.Decimal((.1/.094)), 'calm' : decimal.Decimal((.1/.239)), 'happy' : decimal.Decimal((.1/.185))}

select_statement = 'select * from time_series2'
cursor1.execute(select_statement)
rows = cursor1.fetchall()

for row in rows:
    #collect the non-normalized values
    date = row[1]
    anger = row[2]
    depression = row[3]
    confusion = row[4]
    happy = row[5]
    anxiety = row[6]
    calm = row[7]
    polarity = row[8]
    total = row[9]
    #scale the values
    test = dict.get('anger')
    anger = round(((anger * dict.get('anger'))/total), 3)
    depression = round(((depression * dict.get('depression'))/total), 3)
    confusion = round(((confusion * dict.get('confusion'))/total), 3)
    happy = round(((happy * dict.get('happy'))/total), 3)
    anxiety = round(((anxiety * dict.get('anxiety'))/total), 3)
    calm = round(((calm * dict.get('calm'))/total), 3)
    polarity = round((polarity / total), 3)
    #insert the scaled values into the scaled table
    cursor1.execute(""" INSERT INTO scaled_time_series2 (tweet_date, anger, depression, confusion, happy, anxiety, calm, polarity, total_tweets)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """,
    (date, anger, depression, confusion, happy, anxiety, calm, polarity, total))
    conn.commit()
    print('processed')


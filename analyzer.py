from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(user,df):


    if user != "Overall":
        df = df[df['user']==user]
    
    
    #number of message
    num_mes = df.shape[0]

    #number of words
    words = []
    for mess in df['message']:
        words.extend(mess.split())

    # No of media
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # no of links

    links = []
    extractor = URLExtract()
    for msg in df['message']:
        links.extend(extractor.find_urls(msg))

    return num_mes, len(words), media,  len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    each_counts = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name', 'count':'percent'})
    each_counts=each_counts[each_counts['name']!='group_notification']
    return x, each_counts


def create_wordcloud(user, df):
    
    df_wc_ = df[df['user'] != 'group_notification']
    df_wc_ = df_wc_[df_wc_['message'] != '<Media omitted>\n']
    
    if user != "Overall":
        df_wc_ = df[df['user']==user]
    
    
    wc = WordCloud(width = 500, height = 500, min_font_size=10, background_color='white')
    
    df_wc_ = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc_

def word_counter(user, df):

    words=[]
    if user != "Overall":
        df = df[df['user']==user]


    temp = df[df['user']!='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open("HinglishStopWordFile/stop_hinglish.txt", 'r')
    stopWords = f.read()
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stopWords:
                words.append(word)
        
    

    return pd.DataFrame(Counter(words).most_common(20))

def findEmoji(user, df):
    emojis=[]
    if user != "Overall":
        df = df[df['user']==user]
    
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA.keys()])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def timeline_analysis(user, df):


    if user != "Overall":
        df = df[df['user']==user]

    
    timeline = df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(user, df):
    if user != "Overall":
        df = df[df['user']==user]

    dailyTimeLine = df.groupby(['datemap']).count()['message'].reset_index()

    return dailyTimeLine

def week_activity_map(user,df):
    if user != "Overall":
        df = df[df['user']==user]
    return df['day_name'].value_counts()

def month_activity_map(user,df):
    if user != "Overall":
        df = df[df['user']==user]
    return df['month'].value_counts()

def activity_heatmap(user, df):
    if user != "Overall":
        df = df[df['user']==user]
    
    user_heatmap = df.pivot_table(index='day_name',
                                   columns='period', 
                                   values='message',
                                    aggfunc='count').fillna(0)

    return user_heatmap

import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)?\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [s.replace('\u202F', ' ')for s in dates] # we had to run this as '/s' in pattern caught non-breaking element "\u202f" need to be replace by space " "
    df = pd.DataFrame({'user_message' : message, 'message_date': dates})
    df['message_date']= pd.to_datetime(df['message_date'], format = '%m/%d/%y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'}, inplace = 1)
    users= []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']= messages
    df.drop(columns=['user_message'],inplace=True)
    df['year']= df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['datemap']= df['date'].dt.date
    df['day']=df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    temp = df[df['user']!='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']



    return temp

def fetchUsers(df):
    user_list = df['user'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    return user_list
import re
import pandas as pd

def preprocess(data):
    # Define the regex pattern to match the date and time format in the chat export
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'
    
    # Split the data into messages based on the pattern
    messages = re.split(pattern, data)[1:]
    
    # Find all date matches based on the pattern
    dates = re.findall(pattern, data)
    
    # Create a DataFrame with the messages and corresponding dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Clean the 'message_date' column to remove the trailing ' -' and strip any extra whitespace
    df['message_date'] = df['message_date'].str.replace(' -', '').str.strip()
    
    # Convert 'message_date' to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')
    
    # Rename the column
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Initialize lists to store users and messages separately
    users = []
    messages = []
    
    # Loop through each message and split it into user and message parts
    for message in df['user_message']:
        entry = re.split(r'([\w\s]+?):\s', message, maxsplit=1)
        if len(entry) > 1:  # If a username and message are found
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:  # If the message does not contain a username (e.g., group notification)
            users.append('group_notification')
            messages.append(entry[0].strip())
    
    # Add the extracted users and messages to the DataFrame
    df['user'] = users
    df['message'] = messages
    
    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract additional date and time components
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 11:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    return df


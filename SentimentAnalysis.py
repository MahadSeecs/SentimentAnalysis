# Importing libraries
import tweepy
from tkinter import *
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

# Authentication Variables
access_token = ""
access_secret = ""
api_consumer_key = ""
api_consumer_secret = ""

# Authenticates
auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Makes input window
window = Tk()

entryvar1 = StringVar()
entryvar2 = IntVar()


def clicked():
    x = entryvar1.get()
    y = entryvar2.get()
    return x, y


lab = Label(window, text="Enter Twitter @:").pack()
entry = Entry(
    window,
    textvariable=entryvar1,
).pack()
lab = Label(window, text="Enter number of recent tweets:").pack()
entry = Entry(window, textvariable=entryvar2).pack()
btn = Button(window, text="Submit", command=clicked)
btn.pack()
window.mainloop()

name, num = clicked()


# Extract tweets
posts = api.user_timeline(screen_name=name, count=num, tweet_mode="extended")

# Store tweets in a dataframe
df = pd.DataFrame([tweet.full_text for tweet in posts], columns=["Tweets"])
df.head()

# ldf = pd.DataFrame([tweet.favorite_count for tweet in posts],columns = ['Likes'])
# ldf.head()

# rdf = pd.DataFrame([tweet.retweet_count for tweet in posts],columns = ['Retweets'])
# rdf.head()


# Cleaning tweets
def cleanTxt(posts):
    posts = re.sub(r"@[A-Za-z0-9]+", "", posts)
    posts = re.sub(r"#", "", posts)
    posts = re.sub(r"RT[\s]+", "", posts)
    posts = re.sub(r"https?:\/\/\S+", "", posts)

    return posts


# Applying cleaning function
df["Tweets"] = df["Tweets"].apply(cleanTxt)
# print(df)


# Subjectivity function
def Subjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Polarity function
def Polarity(text):
    return TextBlob(text).sentiment.polarity


# Apply polarity and subjectivity functions to dataframe and add to that dataframe
df["Subjectivity"] = df["Tweets"].apply(Subjectivity)
df["Polarity"] = df["Tweets"].apply(Polarity)
# print(df)

# Visuaise data with WordCloud Library
allWords = " ".join([twts for twts in df["Tweets"]])
wordCloud = WordCloud(
    width=500, height=300, random_state=21, max_font_size=119
).generate(allWords)
plt.imshow(wordCloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# Whether negative, neutral or positive
def Analysis(score):
    if score < 0:
        return "Negative"
    elif score > 0:
        return "Positive"
    else:
        return "Neutral"


df["Analysis"] = df["Polarity"].apply(Analysis)
# print(df)

# # Generate all positive tweets
# pos = 0
# posdf = df.sort_values(by = ['Polarity'])
# for i in range(0,posdf.shape[0]):
#   if(posdf['Analysis'][i] == 'Positive'):
#     print(str(i+1)+')',posdf['Tweets'][i])
#     print()
#     pos = pos + 1
# print(pos)

# # Generate all negative tweets
# neg = 0
# negdf = df.sort_values(by = ['Polarity'])
# for i in range(0,negdf.shape[0]):
#   if(negdf['Analysis'][i] == 'Negative'):
#     print(str(i+1)+')',posdf['Tweets'][i])
#     print()
#     neg = neg + 1
# print(neg)

# # Generate all neutral tweets
# neu = 0
# neudf = df.sort_values(by = ['Polarity'])
# for i in range(0,neudf.shape[0]):
#   if(posdf['Analysis'][i] == 'Neutral'):
#     print(str(i+1)+')',neudf['Tweets'][i])
#     print()
#     neu = neu + 1
# print(neu)

# Plot the polarity against subjectivity
plt.figure(figsize=(8, 6))
for i in range(0, df.shape[0]):
    plt.scatter(df["Polarity"][i],  df["Subjectivity"][i], color="Black")

plt.title("Sentiment Analysis")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity")
plt.show()

# Percentage positive tweets
ptweets = df[df.Analysis == "Positive"]
ptweets = ptweets["Tweets"]

round((ptweets.shape[0] / df.shape[0]) * 100, 1)

# Percentage negative tweets
ntweets = df[df.Analysis == "Negative"]
ntweets = ntweets["Tweets"]

round((ntweets.shape[0] / df.shape[0]) * 100, 1)

# Percentage neutral tweets
nutweets = df[df.Analysis == "Neutral"]
nutweets = nutweets["Tweets"]

round((nutweets.shape[0] / df.shape[0]) * 100, 1)

df["Analysis"].value_counts()

# Plot and visualise the counts
plt.title("Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Counts")
df["Analysis"].value_counts().plot(kind="bar")

plt.show()

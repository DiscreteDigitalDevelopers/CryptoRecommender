import pandas as pd
import requests 
import json 
import csv
import time
import datetime
search_ps4_after_date = "https://api.pushshift.io/reddit/search/submission/?q=screenshot&after=1514764800&before=1517443200&subreddit=PS4"
search_science = "https://api.pushshift.io/reddit/search/submission/?q=science"

def getPushshiftData(query, after, before, sub):
    #Build URL
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    #Print URL to show user
    print(url)
    #Request URL
    r = requests.get(url)
    #Load JSON data from webpage into data variable
    data = json.loads(r.text)
    #return the data element which contains all the submissions data
    return data['data']

"""# Extract key information from Submissions

We want key data for further analysis including: 
* Submission Title
* URL 
* Flair
* Author
* Submission post ID
* Score
* Upload Time
* No. of Comments 
* Permalink.

"""
def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    # url = subm['url']
    #flairs are not always present so we wrap in try/except
    # try:
    #     flair = subm['link_flair_text']
    # except KeyError:
    #     flair = "NaN"    
    author = subm['author']
    sub_id = subm['id']
    # score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    subData.append((sub_id,title,author,created,numComms,permalink))
    subStats[sub_id] = subData

# after = "1609477200"
# before = "1623816000"
# query = "Bitcoin"
# sub = "Cryptocurrency"
after = input("Enter your starting date (unix time): ")
before = input("Enter your end date (unix time): ")
query = input("Enter query: ")
sub = input("Enter which subreddit: ")
subCount = 0
subStats = {}

data = getPushshiftData(query, after, before, sub)
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        subCount+=1
    print(len(data))
    print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(query, after, before, sub)
    
print(len(data))
print(str(len(subStats)) + " submissions have added to list")
print("1st entry is:")
print(list(subStats.values())[0][0][1] + " created: " + str(list(subStats.values())[0][0][5]))
print("Last entry is:")
print(list(subStats.values())[-1][0][1] + " created: " + str(list(subStats.values())[-1][0][5]))

def updateSubs_file():
    upload_count = 0
    print("input filename of submission file, please add .csv")
    filename = input()
    file = filename
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
            
        print(str(upload_count) + " submissions have been uploaded")
updateSubs_file()


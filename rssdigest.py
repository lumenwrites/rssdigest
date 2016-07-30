import listparser as lp
import feedparser
import time
from markdown import Markdown



opml = lp.parse('https://dl.dropbox.com/s/m0vxh64kv18vxde/feedly4.opml')
feeds = opml.feeds

# feed = feedparser.parse(feeds[0].url)
# print(feed.feed.title)

# localtime = time.localtime()
# publishedtime = feed.entries[0].published_parsed
# age = (time.mktime(localtime) - time.mktime(publishedtime)) / 60 / 60 / 24 # in days
# print(age)



md = Markdown()
filename = "/home/ray/rssdigest/rssdigest.html"
with open(filename, "w") as text_file:
    text_file.write(md.convert("# Daily RSS Digest \n----"))


digeststring = "# Daily RSS Digest \n----\n\n"

number_of_feeds = len(feeds)
for index, feed in enumerate(feeds):
    feed = feedparser.parse(feed.url)
    feedstring = ""
    addfeed = False

    print("[" + str(index) + "/" + str(number_of_feeds) + "]")

    if 'title' in feed.feed:
        feedstring += "## " + feed.feed.title + "\n"
    
    for entry in feed.entries:
        localtime = time.localtime()
        try:
            publishedtime = entry.published_parsed
            # age in days
            age = (time.mktime(localtime) - time.mktime(publishedtime)) / 60 / 60 / 24
            if age < 1:
                feedstring += "## ["+entry.title+"]("+entry.link+")\n\n"
                if 'description' in entry:
                    if len(entry.description) < 500:
                        feedstring += entry.description + "\n\n"
                addfeed = True
        except:
            pass

    if not addfeed:
        print(feedstring + "No new posts\n")

    feedstring += "----\n"

    if addfeed:
        print(feedstring)
        # Append to string
        digeststring += feedstring
        # Append to file
        with open(filename, "a") as text_file:
            feedhtml = md.convert(feedstring)
            text_file.write(feedhtml)

digesthtml = md.convert(digeststring)    


# Sending email
import os

import sendgrid
import os
from sendgrid.helpers.mail import *

SENDGRID_APIKEY = os.environ["SENDGRID_APIKEY"]
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_APIKEY)
from_email = Email("raymestalez@gmail.com")
to_email = Email("raymestalez@gmail.com")
subject = "Daily RSS Digest"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
content = Content("text/html", digesthtml)
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)
print("Email sent!!")

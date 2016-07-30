import sys

# For feeds
import listparser as lp
import feedparser
import time
from markdown import Markdown

# For email
import os
import sendgrid
from sendgrid.helpers.mail import *


print(sys.argv[1])


def get_feeds(feeds_file, max_age, max_feeds):
    opml = lp.parse(feeds_file)
    feeds = opml.feeds

    feeds = feeds[:max_feeds]
    
    md = Markdown()
    filename = "rssdigest.html"
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
                if age < max_age:
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

    # print("Final: " + digesthtml)

    return digesthtml



def send_email(subject, message, from_email, to_email, apikey):
    sg = sendgrid.SendGridAPIClient(apikey=apikey)
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject
    # content = Content("text/plain", "and easy to do anywhere, even with Python")
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
    print("Email sent!!")


    

max_age = 100
max_feeds = 5
email = sys.argv[1]
feeds_file = sys.argv[2]
SENDGRID_APIKEY = os.environ["SENDGRID_APIKEY"]


digesthtml = get_feeds(feeds_file, max_age, max_feeds)
send_email("Daily RSS Digest", digesthtml, email, email, SENDGRID_APIKEY)

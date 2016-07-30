# RSS Digest

This script sends you a daily email digest of your rss feeds.


## Installing the requirements

```shell
sudo pip3.4 install sendgrid-python listparser feedparser
```

## Adding the list of feeds

This script requires an OPML file that contains a list of your rss feeds.

To export your RSS feeds from feedly you can click Organize, and then click on the link called "As OPML". Save this file into the rssdigest directory with the name "feeds.opml".


## Using sendgrid to send an email

Create a sendgrid account, create an api key, and before running the script run the command:

```shell
export SENDGRID_APIKEY=sendgrid_api_key_here
```

## Running the script

```shell
python3.4 rssdigest.py youremail@gmail.com
```

## Using cron to run the script daily

Run the command:

```shell
crontab -e
```

And at the end of the file add the lines:

```
SENDGRID_APIKEY=sendgrid_api_key_here
30 10 * * * python3.4 /path/to/the/script/rssdigest.py youremail@gmail.com
```

(it will run the script every day at 10:30)

    # -*- coding: utf-8 -*-
import tweepy
import json
import re
import os
import string
from PIL import Image
import gc

from secrets import *
import imagesearch

auth = tweepy.OAuthHandler(68ZcCgrQUAr12xhKn6OxMRGW2 ,mtqOk68fdr6OprGf9Oq4bRbQgf32F5uziI1TFFA2y2JFaYn7d7)
auth.set_access_token(999337147206422528-yDsDWT8LDOZuWRs5g2NuNWRtbSyMEzZ,RIFLLvzgCRrQ4QT5vS1irDxCZpqV57P7k7lRaDUrkY7j5)
api = tweepy.API(auth)

stream_rule = " "
account_screen_name = "botdonpa "
account_user_id = "botdonpa "

def Oimage(image):
    background = Image.open("img/"+image)
    foreground = Image.open("img/donppaaa.png")
    bw = background.size[0]
    bh = background.size[1]
    fw = foreground.size[0]
    fh = foreground.size[1]
    if bw < fw:
        resize = (int(bw*fw/bw),int(bh*fw/bw))
        background = background.resize(resize,Image.ANTIALIAS)
        bw = background.size[0]
        bh = background.size[1]
    if bh < fh:
        resize =  (int(bw*fh/bh),int(bh*fh/bh))
        background = background.resize(resize,Image.ANTIALIAS)
        bw = background.size[0]
        bh = background.size[1]
    background.paste(foreground, (bw-fw,bh-fh), foreground)
    background.save("output.png") 
    os.remove("img/"+image)
    background.close()
    foreground.close()  

def archive(text):
    file_txt = open('archives.txt','a')
    file_txt.write("\n"+text)
    file_txt.close()


def create_tweet(txt):
    txt = re.sub("donpa rapeando a ",'',txt)
    txt = re.sub("donpa rapeando a ",'',txt)
    txt = re.sub("donpa rapeando a ",'',txt)
    txt = re.sub("donpa rapeando a ",'',txt)
    txt = re.sub("donpa rapeando a ",'',txt)
    txt = re.sub("donpa rapeandole a ",'',txt)
    txt = re.sub("donpa rapeandole a ",'',txt)
    txt = re.sub("donpa rapeandole a ",'',txt)
    img = imagesearch.image_search(txt)
    if img != False:
        try:
            Oimage(img)
        except OSError:
            img = False
        archive(txt)
    image_size = os.path.getsize("output.png")
    print(image_size)
    if image_size >= 3072000:
        print('File too big! Returning false')
        img = False

    return (txt,img)


class ReplyToTweet(tweepy.StreamListener):

    def on_data(self, data):
        print('Tweet received!')
        tweet = json.loads(data.strip())
        retweeted = tweet.get('retweeted')
        faved = tweet.get('favorited')
        if retweeted is not None and not retweeted and tweet.get('user',{}).get('id_str','') != account_user_id and 'retweeted_status' not in tweet:
            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            
            tweetText = tweet.get('text').encode('utf-8')

            tweetText = tweetText.decode('ascii',errors='ignore')
            tweetText = re.sub('@botdonpa','',tweetText)
            tweetText = re.sub('@botdonpa','',tweetText)
            tweetText = re.sub('@botdonpa','',tweetText)
            tweetText = re.sub('@botdonpa','',tweetText)
            tweetText = re.sub('#','',tweetText)

            full_reply = create_tweet(tweetText)
            if full_reply[1] == False:
                replyText = '@' + screenName + ' ' + "No he podido encontrar " + full_reply[0] + " AHHHHH JOPUTA "
                api.update_status(status=replyText, in_reply_to_status_id=tweetId)
                gc.collect()
            else:
                replyText = '@' + screenName + ' ' + "donpa rapeando a " + full_reply[0]
                api.update_with_media("output.png",status=replyText, in_reply_to_status_id=tweetId)
                gc.collect()


    def on_error(self, status):
        print("ERROR #"+str(status))


if __name__ == "__main__":
    streamListener = ReplyToTweet()
    twitterStream = tweepy.Stream(auth, streamListener)
    twitterStream.userstream(_with='user')

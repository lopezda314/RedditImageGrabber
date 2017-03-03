#!/usr/bin/env python
#####################################################################################
#####################################################################################
##    One of the first "useful" things I ever coded.                               ##
##    Takes in subreddit and crawls thumbnails using Reddit's REST API.            ##
##    TODO - add pagination                                                        ##
##    Main Features - RedditCrawl Class (does all the hardwork)                    ##
##   - process_images does all the image processing for users that want image stuff## 
#####################################################################################
#####################################################################################

#importing all the modules
import requests
import json
import getpass
import time
import numpy
from skimage import io
from PIL import Image
import argparse

#searches JSON for specified key/value pairs and stores result in pics
def get_all(myjson, key, pics):
	if type(myjson) == str:
		myjson = json.loads(myjson)
	if type(myjson) is dict:
		for jsonkey in myjson:
			if type(myjson[jsonkey]) in (list, dict):
				get_all(myjson[jsonkey], key, pics)
			elif jsonkey == key:
				pics.append(myjson[jsonkey])
	elif type(myjson) is list:
		for item in myjson:
			if type(item) in (list, dict):
				get_all(item, key, pics)
	return pics

def get_avg(img):
	average_color_per_row = numpy.average(img,axis=0)
	average_color = numpy.average(average_color_per_row, axis=0)
	average_color = numpy.uint8(average_color)
	return average_color

def process_images(data, colors):
    for index, link in enumerate(data):
        if link[0:4] == 'http':
            image_file = io.imread(link)
            colors[index][0] = get_avg(image_file[:][:][0])
            colors[index][1] = get_avg(image_file[:][:][1])
            colors[index][2] = get_avg(image_file[:][:][2])
            print (avg_subreddit[index])
            time.sleep(1.5)

    average_color = numpy.average(colors, axis=0)
    average_color_image = numpy.array([[average_color]*100] * 100, numpy.uint8)

    Image.fromarray(average_color_image).save("output.jpg")
    return

class RedditCrawler():
    def __init__(self, subreddit, user_dict, content_pull):
        self.subreddit = subreddit
        self.user_dict = user_dict
        self.content_pull = content_pull
        self.data = None
        return


    def crawl(self, headers={'user-agent':'image-grabber',}):
        client = requests.session()
        client.headers = headers

        r = client.post(r'http://ww.reddit.com/r/' + self.subreddit + '/.json', data=self.user_dict)

        #use tempStorage for get_all method. all the content actually ends up in self.data though
        tempStorage = []
        self.data = get_all(r.text, self.content_pull, tempStorage)
        return self.data



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Use this program to crawl Reddit for useful info like thumbnails or comments of your favorite Subreddit!")
    parser.add_argument("-u", help="Your Reddit Username", required=True)
    parser.add_argument("-p", help="Your Reddit Password", required=True)
    parser.add_argument("-s", "--subreddit", help="Subreddit you want to crawl", required=True)
    args = vars(parser.parse_args())
    if len(args) != 3:
        quit()

    #set username and password values
    username = args['u']
    password = args['p']
    subreddit = args['subreddit']
    #create dict with username and password
    user_pass_dict = {'user': username,
                     'passwd': password,
                    'api_type': 'json',}

    redditcrawl = RedditCrawler(subreddit, user_pass_dict, 'thumbnail')
    pics = redditcrawl.crawl()
    avg_subreddit = numpy.zeros((len(pics), 3))
    process_images(pics, avg_subreddit)

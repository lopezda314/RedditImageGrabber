#importing all the modules
import requests
import json
import getpass
import time
import numpy
from skimage import io
from PIL import Image
import argparse

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

#set username and password values
username = input("Give Me Your Username!:")
password = getpass.getpass()

subreddit = str(input('Place the subreddit you want to know about here:'))
#create dict with username and password
user_pass_dict = {'user': username,
				  'passwd': password,
				  'api_type': 'json',}

#set the header for all the following requests
headers = {'user-agent': 'image-grabber', }

#create a requests.session that'll handle our cookies for us
client = requests.session()
client.headers=headers

#make a login request, passing in the user and pass as data
r = client.post(r'http://www.reddit.com/r/' + subreddit + '/.json', data=user_pass_dict)
pics = []
iteration = get_all(r.text, 'thumbnail', pics)
size = len(iteration)
avg_subreddit = numpy.zeros((size, 3))

for index, link in enumerate(iteration):
	if link[0:4] == 'http':
		image_file = io.imread(link)
		avg_subreddit[index][0] = get_avg(image_file[:][:][0])
		avg_subreddit[index][1] = get_avg(image_file[:][:][1])
		avg_subreddit[index][2] = get_avg(image_file[:][:][2])
		print (avg_subreddit[index])
		time.sleep(1.5)

average_color = numpy.average(avg_subreddit, axis=0)
average_color_image = numpy.array([[average_color]*100] * 100, numpy.uint8)

Image.fromarray(average_color_image).save("output.jpg")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("square", help="display a square of a given number",
                        type=int)
    args = parser.parse_args()
    print(args.square**2)


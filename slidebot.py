import praw
import config
import time
import os
import urllib
import os.path
from urllib.request import urlretrieve
import json
from imgurpython import ImgurClient
from pystreamable import StreamableApi
import slideshow
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
						

streamApi = StreamableApi(config.streamusername,config.streampass)
subList = [ 
	'Pictures',
	'pics',
	'PhotoshopBattles',
	'Ireland',
	'Europe',
	'Melbourne',
	'france',
	'denmark',
	'italy',
	'norge',
	'polska',
	'de',
	'suomi',
	'romania',
	'belgium',
	'canada',
	'thenetherlands',
	'toronto',
	'vancouver',
	'MURICA',
	'floridaman',
	'nyc',
	'chicago',
	'seattle',
	'portland',
	'boston',
	'atlanta',
	'washingtondc',
	'denver',
	'philadelphia',
	'mexico',
	'australia',
	'newzealand',
	'Philippines',
	'india',
	'kpop',
	'pyongyang',
	'singapore',
	'japan',
	'japanpics',
	'brasil',
	'argentina',
	'Politics',
	'worldpolitics',
	'Libertarian',
	'anarchism',
	'socialism',
	'conservative',
	'politicalhumor',
	'neutralpolitics',
	'politicaldiscussion',
	'ukpolitics',
	'latestagecapitalism',
	'geopolitics',
	'wholesomememes',
	'prequelmemes',
	'SequelMemes',
	'terriblefacebookmemes',
	'Demotivational',
	'TrollXChromosomes',
	'CrappyDesign',
	'web_design',
	'graphic_design',
	'design',
	'designporn',
	'InteriorDesign',
	'ATBGE',
	'dontdeadopeninside',
	'assholedesign',
	'keming',
	'MilitaryPorn',
	'military',
	'food',
	'FoodPorn',
	'foodhacks',
	'shittyfoodporn',
	'earthporn',
	'hardcoreaww',
	'hitmanimals',
	'natureisfuckinglit',
	'heavyseas',
	'funny',
	#'movies',#No bots
	'aww',
	'television',
	'sports',
	'Documentaries',
	'TwoXChromosomes',
	#'DIY', Banned
	#'Test',
	'OldSchoolCool',
	'Pictures',
	'pics',
	'PhotoshopBattles',
	'perfecttiming',
	'itookapicture',
	'Pareidolia',
	'ExpectationVSReality',
	'dogpictures',
	'misleadingthumbnails',
	'FifthWorldPics',
	'TheWayWeWere',
	'pic',
	'nocontextpics',
	'cosplay',
	'woodworking',
	'somethingimade',
	'architecture',
	'CoolGuides',
	#'WorldBuilding', copyright claim
	'aquariums',
	'ifyoulikeblank',
	'DiWHY',
	'knitting',
	'sewing',
	'modelmakers',
	'crochet',
	'ProtectAndServe',
	'RTLSDR',
	'digitalnomad',
	'FastWorkers',
	'accounting',
	'preppers',
	'cars',
	'motorcycles',
	'carporn',
	'justrolledintotheshop',
	'Shitty_Car_Mods',
	'autos',
	'AutoDetailing',
	'photography',
	'itookapicture',
	'Filmmakers',
	'astrophotography',
	'analog',
	'photocritique',
	'mildlyinteresting',
	'interestingasfuck',
	'damnthatsinteresting',
	'gentlemanboners',
	'prettygirls',
	'Art',
	#'redditgetsdrawn', Ban, reason not stated
	'heavymind',
	'drawing',
	'graffiti',
	'retrofuturism',
	'sketchdaily',
	'ArtPorn',
	'pixelart',
	#'artfundamentals',
	'learnart',
	'Space',
	'SpacePorn',
	'astronomy',
	'astrophotography',
	'spacex',
	'nasa',
	'Space',
	'HistoryPorn',
	'PropagandaPosters',
	'TheWayWeWere',
	'technology',
	'internetisbeautiful',
	'futurology',
	'pcmasterrace',
	'buildapc',
	'gamedev',
	'design',
	'hacking',
	'infographics',
	#'3Dprinting',
	'EngineeringPorn',
	'cableporn',
	'unixporn',
	'Demotivational',
	'lolcats',
	'supershibe',
	'copypasta',
	'emojipasta',
	'AdviceAnimals',
	'memes',
	'MapPorn',
	'polandball',
	'vexillology'
	 ]
	 
	 
slideReply = "I am SlideshowBot, I have made your Imgur Album into a looping Slideshow [here]"
slideReply2nd = "\n \n *** \n I am a bot, please upvote if you find me useful.  "
slideReply2 = "I foramtiing [here](http://reddit.com/r/redditdev) \n \n *** \n Iam bot "

def bot_login():
	logging.info ("Loggin in...")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Makros")
	logging.info ("Logged in!")

	return r

def getImgurData(url):
	path = urllib.parse.urlparse(url).path
	path = str(path.split('/')[-1])
	logging.info(path)
	try:
		client = ImgurClient(config.imgur_client_id, config.imgur_client_secret)
		items = client.get_album(path)
	except:
		logging.info("Bad Link Error")
		return 0,0,0
	#logging.info(items.title)
	#logging.info(items.images_count)
	#logging.info(items.images)
	return items.images_count, items.images, path

def sendVideotoStreamable(videofilepath):
	videoURL = streamApi.upload_video(videofilepath)
	return videoURL
	

def saveFilesandStartSlide(imgurImageData, path):
	newpath = path 
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		imageList = []
		descriptionList = []
		for idx, image in  enumerate(imgurImageData):
			#save each image to folder
			#logging.info(image['description'])
			
			logging.info("Saving image")
			filename = urllib.parse.urlparse(image["link"]).path
			filename = str(filename.split('/')[-1])
			urlretrieve(image["link"], path+"/"+filename)
			logging.info("image saved!")
			imageList.append(path+"/"+filename)
			descriptionList.append(image['description'])
	else:
		#Gallery was attempted and for some reason never uploaded best leave it
		imageList = 0
		descriptionList = 0
	
	return imageList, descriptionList
	
def run_bot(r, posts_replied_to):
	
	#Loop through each subreddit
	for idx, val in enumerate(subList):
		logging.info("Checking sub r/"+str(val))
		logging.info ("Obtaining 150 comments...")
		for post in r.subreddit(val).hot(limit=150):
			#logging.info("Number of comments in post"+str(post.num_comments))
			if (post.url.find("imgur") > 1) and ((post.url.find("/gallery") > 1) or (post.url.find("/a/") > 1)) and(post.url not in saved_gallerys) and(post.id not in posts_replied_to) and(post.num_comments > 2) :
				
				#retreive Images 
				imageAmounts, imgurImageData, path = getImgurData(post.url)
				if imageAmounts > 1:
					logging.info ("Imgur Gallery!")
					logging.info("Post Title:"+str(post.title))
					logging.info("Post url:"+str(post.url))
					logging.info("Post author:"+str(post.author.name))
					logging.info("Post id:"+str(post.id))
	
					imageList, descriptionList = saveFilesandStartSlide(imgurImageData, path)
					#Start Slideshow
					if(imageList != 0):
						#write path to saved files gallery
						saved_gallerys.append(post.url)
						with open ("saved_gallerys.txt", "a") as f:
							f.write(post.url + "\n")
						#write path to saved comments
						posts_replied_to.append(post.id)
						with open ("posts_replied_to.txt", "a") as f:
							f.write(post.id + "\n")
						#Start creating AVI
						videofilepath = slideshow.buildSlideShow(imageList, descriptionList,path, str(post.title)+" | u/"+str(post.author.name))
						if(videofilepath):
							#Start upload unto Streamable
							logging.info("Starting Upload")
							videoURL = sendVideotoStreamable(videofilepath)
							logging.info("Uploaded")
							logging.info("videoUrl: "+str(videoURL))
							#Attempt reply wait 20 seconds each
							
							for attempt in range(25):
								try:
									logging.info("Starting comment post attempt ")
									post.reply(slideReply2)		
									logging.info("Comment posted")
								except:
									logging.info("Exception with comment waiting 30 seconds")
									time.sleep(30)
								else:
									logging.info("Posted Response")
									break
							
					else:
						logging.info("SlideShow already saved ignoring")
				else:
					logging.info("Only 1 picture in Gallery ignoring")
	logging.info("Finished checkinging - waiting 1 minute")
	time.sleep(60)

def get_saved_comments():
	if not os.path.isfile("posts_replied_to.txt"):
		posts_replied_to = []
	else:
		with open("posts_replied_to.txt", "r") as f:
			posts_replied_to = f.read()
			posts_replied_to = posts_replied_to.split("\n")
			posts_replied_to = list(filter(None, posts_replied_to))

	return posts_replied_to
	
def get_saved_gallerys():
	if not os.path.isfile("saved_gallerys.txt"):
		saved_gallerys = []
	else:
		with open("saved_gallerys.txt", "r") as f:
			saved_gallerys = f.read()
			saved_gallerys = saved_gallerys.split("\n")
			saved_gallerys = list(filter(None, saved_gallerys))

	return saved_gallerys

r = bot_login()
posts_replied_to = get_saved_comments()
saved_gallerys = get_saved_gallerys()
logging.info ("posts_replied_to: "+str(posts_replied_to))
logging.info ("saved_gallerys: "+str(saved_gallerys))

while True:
	#for i in range(100):
	#	for attempt in range(10):
	#		try:
	#			logging.info("Starting attempt "+str(i))
	#			run_bot(r, posts_replied_to)
	#		except:
	#			logging.info("Exception waiting 1 minutes")
	#			time.sleep(5)
	#		else:
	#			break
	#	else:
	#		logging.info("100 Exceptions reached")
	run_bot(r, posts_replied_to)
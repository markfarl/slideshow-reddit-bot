import slideshow
import logging


logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+",
					format="%(asctime)-15s %(levelname)-8s %(message)s")
logging.info ("Loggin in...")

descriptionList = [ 
     'Touch me gowl',
     #'Ye dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good enough for ye',
     'TEST/image6.jpg e dirty yold ye good enough for yeYe dirty yold ye good enough for yeYe dirty yold ye good e',
     'IOEIDPOED PDOC PC DCPopjrfoh fidh cvidh ciuh dciuh dicu hdicuhdi uchiduhcidu icuhi  ewhfiuweh fiueh wfiuhe wifuh ewifuh iweufh iweufh iweuhfiweufh iweufh iweufh iwefu ',
     'none',
     'none',
	 ]
imageList = [ 
	#u'TEST/image4.jpg',
	#u'TEST/image6.jpg',
	# u'TEST/small.png',
    # u'TEST/image4.jpg',
    # u'TEST/image5.jpg',
    # u'TEST/image6.jpg',
	 ]

titleText = "A night in this place was n this place was n this place was n this place was n this place was n this place was n this place was n this place was n this place was n this place was n this place was n this place was great | u/iHaveFun"
path = "TEST"
	 
slideshow.buildSlideShow(imageList, descriptionList,path,titleText)
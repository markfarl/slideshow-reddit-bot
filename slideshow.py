from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ExifTags
import cv2
import numpy as np
import pytweening
import math
from image_utils import ImageText
import logging

#pip install pillow #for PIL
#pip install opencv-python #for cv2 and numpy

imageList22 = [ 
     u'image22.jpg',
     u'image4.jpg',
     u'image5.jpg',
     u'image2.jpg',
	 ]
	 
	
def image_rotate(im1):
	for orientation in ExifTags.TAGS.keys() : 
		if ExifTags.TAGS[orientation]=='Orientation' : break 
	try:
		exif=dict(im1._getexif().items())
		if   exif[orientation] == 3 :
			logging.info("Image rotate 3")
			im1=im1.rotate(180, expand=True)
		elif exif[orientation] == 6 :
			logging.info("Image rotate 6")
			im1=im1.rotate(270, expand=True)
		elif exif[orientation] == 8 :
			logging.info("Image rotate 8")		
			im1=im1.rotate(90, expand=True)
	except:
		logging.info ("There is no EXIF")
	
	
	return im1

	
def getOffset(t, d):
	b = 0
	c = float(d)
	t = float(t)
	t = t/d
	if ((t) < (1/float(2.75))):
		return c*(float(7.5625)*t*t) + b
	elif (t < (2/float(2.75))):
		t = t -(float(1.5))
		return c*(float(7.5625)*(t/float(2.75))*t + float(.75)) + b
	elif (t < (2.5/2.75)):
		t = t -(float(2.25))
		return c*(float(7.5625)*(t/float(2.75))*t + float(.9375)) + b
	else:
		t = t-(float(2.625))
		return c*(float(7.5625)*(t/float(2.75))*t + float(.984375)) + b

def resize_image(image, h, w):
	width2, height1  = image.size
	if (width2 > w or height1 > h):
		logging.info("image resize small")
		image.thumbnail([w, h], Image.ANTIALIAS)
	elif (width2 < w and height1 < h):
		logging.info("image resize enalrge!")
		wratio = w/width2
		hration = h/height1
		if(wratio <= hration):
			logging.info("increase by wratio")
			image = image.resize((int(width2 * wratio), int(height1 * wratio)))
		else:	
			logging.info("increase by hratio")
			image = image.resize((int(width2 * hration) , int(height1 * hration)))
	return image
	
def limitTopRes(w,h):
	if(w > 1920 or h > 1080):
		logging.info("Higher than 720p shrink")
		wratio = w/1920
		hratio = h/1080
		logging.info("wratio:" + str(wratio) + " hratio:"+ str(hratio))
		if(wratio >= hratio):
			logging.info("increase by wratio")
			w = int(w / wratio)
			h = int(h / wratio)
		else:	
			logging.info("increase by hratio")
			w = int(w / hratio)
			h = int(h / hratio)
	return w,h
	
def getZoomScaleInt(height,width,zoomPosition):
	zoomScaleH = height+((height/20)*pytweening.easeOutQuad(zoomPosition)) #divide by height
	zoomScaleW = width+((width/20)*pytweening.easeOutQuad(zoomPosition)) #divide by height
	return int(zoomScaleH), int(zoomScaleW)

def textBoxBuilder(text,height,width,bufferOffsetH,buffer,font,fontSize):
	imgTxt = ImageText(buffer, background=(255, 255, 255, 0))
	imgTxtShadow = ImageText(buffer, background=(0, 0, 0, 0))
	imgTxtWhiteShadow = ImageText(buffer, background=(80, 80,80, 0))
	
	color = (255, 255, 255)
	textHeight = imgTxt.write_text_box((0,0), text, int(width - (width/10)), font_filename=font,font_size=fontSize, color=color, place='center')
	imgTxtShadow.write_text_box((0,0), text, int(width - (width/10)), font_filename=font,font_size=fontSize, color=(0,0,50), place='center')
	imgTxtWhiteShadow.write_text_box((0,0), text, int(width - (width/10)), font_filename=font,font_size=fontSize, color=(80,80,80), place='center')
	textHeight = height - ((textHeight[1]) + bufferOffsetH)
	if textHeight < 0:
		textHeight = bufferOffsetH
	#logging.info("textHeight"+str(textHeight))
	return textHeight,imgTxt, imgTxtShadow, imgTxtWhiteShadow
		
def getFontSize(text,height,width):
	if text != None:
		text = text
	else:
		text = ""
	logging.info("len"+str(len(text)))
	if height > width:
		smallestAspect = width
	else:
		smallestAspect = height
		
	if len(text) > 150:
		logging.info((1000 - len(text))/ 850)
		fontSize = int(((smallestAspect / 1080) * 70)*((1500 - len(text))/ 1350))
	else:
		fontSize = int((smallestAspect / 1080) * 70)
	
	if fontSize > 70:
		fontSize = 70
	elif fontSize < 20:
		fontSize = 20
	return fontSize, text
	
def buildSlideShow(imageList, descriptionList, path, titleText):
	FPS = 60 # Sets the FPS of the entire video
	currentFrame = 0 # The animation hasn't moved yet, so we're going to leave it as zero
	blendingFrames = 60 # Sets the amount of time that each transition should last for
	framesbetweenImages =  120             # Zoom Frames
	staticFrames = 120 #frames at the start are static text comes in here	TO
	textFrames = 30 #Frames for text should be < static frames
	titleTextDuration = 280
	
	
	im1 = Image.open(imageList[0])# Load the image in
	im1 = image_rotate(im1) # Roate image if nessessacry
	im2 = im1 # Define a second image to force a global variable to be created
	width, height = im1.size # Get some stats on the image file to create the video with
	## Limit W & H by 720p maintain aspect 
	logging.info("h:" + str(height) + " W;"+ str(width) )
	width, height = limitTopRes(width,height)

	logging.info("new res: h:" + str(height) + " W;"+ str(width) )
	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	video = cv2.VideoWriter(path+"/"+path+".avi",fourcc,FPS,(width,height),True)
	#write gallery objects
	imageListFile = open(path+"/imageList-"+path+".txt","w+")
	imageListFile.write(str(imageList))
	descriptionListFile = open(path+"/descriptionList-"+path+".txt","w+")
	descriptionListFile.write(str(descriptionList))
	
	#Font Type
	font = 'MaxImpact.ttf'
	tileFontSize = getFontSize(titleText,height,width)
	
	for idx, val in enumerate(imageList):
		logging.info("start image: "+str(idx))
		im1 = Image.open(val)
		fontSize, text = getFontSize(descriptionList[idx],height,width)
		
		#logging.info("fontSize: "+str(fontSize))
		
		##Get Staticframe lenght
		staticFrames = 80 + (len(text)*4)
		if staticFrames > 660:
			staticFrames = 660
		##logging.info("staticFrames "+str(staticFrames))
		
		buffer = (int(width - (width/10)), int(height - (height/10)))
		bufferOffset = (int(width/20), int(height/20))
		bufferOffsetW = int(width/20)
		bufferOffsetH = int(height/9)
		
		imgTxt = ImageText(buffer, background=(255, 255, 255, 0))
		imgTxtShadow = ImageText(buffer, background=(0, 0, 0, 0))
		imgTxtWhiteShadow = ImageText(buffer, background=(80, 80,80, 0))
		
		textHeight,imgTxt, imgTxtShadow, imgTxtWhiteShadow = textBoxBuilder(text,height,width,bufferOffsetH,buffer,font,fontSize)
		textTitleHeight,imgTitleTxt, imgTitleTxtShadow, imgTitleTxtWhiteShadow = textBoxBuilder(titleText,height,width,bufferOffsetH,buffer,font,fontSize)

	
		#Open next image
		if idx == (len(imageList) - 1):
			logging.info("Last Image")
			im2 = Image.open(imageList[0])
		else:
			logging.info(str(idx) + " len"+ str(len(imageList)))
			im2 = Image.open(imageList[idx+1])
			
			
		outputimage = Image.new('RGBA', (width, height), (50, 50, 50, 255)) # Image all others will paste onto
		outputimageZoom = Image.new('RGBA', (width, height), (50, 50, 50, 255)) # Image zoomed others will paste onto
		im1 = image_rotate(im1)
		im1 = resize_image(im1, height, width)
		img_w, img_h = im1.size
		offset = ((width - img_w) // 2, (height - img_h) // 2)
		outputimage.paste(im1, offset)
		outputimageZoom.paste(im1, offset)
		
		#Output Blend Frames
		outputimageBlend = Image.new('RGBA', (width, height), (50, 50, 50, 255)) # Image all others will paste onto
		
		im2 = image_rotate(im2)
		im2 = resize_image(im2, height, width)
		img_wBlend, img_hBlend = im2.size
		offsetBlend = ((width - img_wBlend) // 2, (height - img_hBlend) // 2)
		outputimageBlend.paste(im2, offsetBlend)
		
		
		if(idx == 0):
			#first Image, show titleText on open
			fbi = ((currentFrame) + (framesbetweenImages + blendingFrames + staticFrames + titleTextDuration + textFrames))
			while (currentFrame) < (fbi - blendingFrames - framesbetweenImages):
				#draw = ImageDraw.Draw(outputimage)
				#draw.text((100, 100), text, font=font, fill="blue")
				
				#FIrst will always start 0 frame
				currentTitleTextFrame  = currentFrame
				
				if currentFrame <= textFrames:
					#Do animation for text title axis
					currentTextFrame = currentFrame / textFrames
					
					newTextHeight = int((bufferOffsetW+textTitleHeight)*pytweening.easeOutQuad(currentTextFrame))-bufferOffsetW-textTitleHeight
					outputimage.paste(outputimageZoom, (0,0))
					outputimage.paste(imgTitleTxtShadow.image, (bufferOffsetW - 2, newTextHeight + 2), imgTitleTxtShadow.image)
					outputimage.paste(imgTitleTxtShadow.image, (bufferOffsetW - 1, newTextHeight + 1), imgTitleTxtShadow.image)
					outputimage.paste(imgTitleTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTitleTxtWhiteShadow.image)
					outputimage.paste(imgTitleTxt.image, (bufferOffsetW, newTextHeight), imgTitleTxt.image)
					#logging.info("textHeight N "+str(newTextHeight))
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
				elif currentFrame <= (titleTextDuration):
					#Static 
						   
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
				#STart Last Frames ANimation here
				elif currentFrame <= textFrames + titleTextDuration:
					currentTextFrame = (currentFrame - titleTextDuration)/ textFrames
					newTextHeight = int(height - ((height - textHeight)*pytweening.easeOutQuad(currentTextFrame)))
					newTextTitleHeight = int((bufferOffsetW+textTitleHeight)*pytweening.easeOutQuad(-(currentTextFrame - 1)))-bufferOffsetW-textTitleHeight
					
					
					outputimage.paste(outputimageZoom, (0,0))
					outputimage.paste(imgTitleTxtShadow.image, (bufferOffsetW - 2, newTextTitleHeight + 2), imgTitleTxtShadow.image)
					outputimage.paste(imgTitleTxtShadow.image, (bufferOffsetW - 1, newTextTitleHeight + 1), imgTitleTxtShadow.image)
					outputimage.paste(imgTitleTxtWhiteShadow.image, (bufferOffsetW + 1, newTextTitleHeight - 1), imgTitleTxtWhiteShadow.image)
					outputimage.paste(imgTitleTxt.image, (bufferOffsetW, newTextTitleHeight), imgTitleTxt.image)
					
					outputimage.paste(imgTxtShadow.image, (bufferOffsetW - 2, newTextHeight + 2), imgTxtShadow.image)
					outputimage.paste(imgTxtShadow.image, (bufferOffsetW - 1, newTextHeight + 1), imgTxtShadow.image)
					outputimage.paste(imgTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTxtShadow.image)
					outputimage.paste(imgTxt.image, (bufferOffsetW, newTextHeight), imgTxt.image)
					#logging.info("textHeight N "+str(newTextHeight))
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
				else:
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
		else:
			fbi = ((currentFrame) + (framesbetweenImages + blendingFrames + staticFrames))
			#Starts static frames text belnd will start here
			while (currentFrame) < (fbi - blendingFrames - framesbetweenImages):
				#logging.info("static frames"+str(currentFrame))
				#draw = ImageDraw.Draw(outputimage)
				#draw.text((100, 100), text, font=font, fill="blue")
				
				currentTextFrame  = textFrames - ((fbi - blendingFrames - framesbetweenImages - staticFrames) + textFrames - currentFrame);
				
				if currentTextFrame <= textFrames:
					#Do animation for text Y axis
					#Gets range between 0 and 1 
					#logging.info("currentTextFrame "+str(currentTextFrame))
					currentTextFrame = currentTextFrame / textFrames
					
					#logging.info("currentTextFrame -  "+str(currentTextFrame))

					newTextHeight = int(height - ((height - textHeight)*pytweening.easeOutQuad(currentTextFrame)))
					outputimage.paste(outputimageZoom, (0,0))
					outputimage.paste(imgTxtShadow.image, (bufferOffsetW - 2, newTextHeight + 2), imgTxtShadow.image)
					outputimage.paste(imgTxtShadow.image, (bufferOffsetW - 1, newTextHeight + 1), imgTxtShadow.image)
					outputimage.paste(imgTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTxtShadow.image)
					outputimage.paste(imgTxt.image, (bufferOffsetW, newTextHeight), imgTxt.image)
					#logging.info("textHeight N "+str(newTextHeight))
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
				else:
					#imgTxt.save('sample-imagetext.png')()
					#outputimage.paste(imgTxt.image, (bufferOffsetW, textHeight), imgTxt.image)
						   
					video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
					currentFrame += 1
		#Starts Zoom Frame
		while (currentFrame + 0) < (fbi - blendingFrames):
			#logging.info("zoom frames"+str(currentFrame))
			#find zoom based on frame position var is from 0 to 1 
			zoomPosition = -(((fbi - blendingFrames - currentFrame) / (framesbetweenImages))) + 1
			#Find dimensions based on zoom position 
			zoomScaleH, zoomScaleW = getZoomScaleInt(height,width,zoomPosition)
			#logging.info("next-W"+str(zoomScaleW))
			#logging.info("next-H"+str(zoomScaleH))
			
			#Check if zoom frames stay similar if not we can antialias frames via blend
			zoomFrameCheck = 1
			keepCheck = "true"
			if(zoomPosition < 1):
				while keepCheck == "true":
					if(zoomFrameCheck < (fbi - currentFrame - blendingFrames)):
						nextZoomPosition = -(((fbi - blendingFrames - (currentFrame + zoomFrameCheck)) / framesbetweenImages)) + 1
						nextZoomScaleH, nextZoomScaleW = getZoomScaleInt(height,width,nextZoomPosition)
						#If the frames zoom size are less than 2 pixel differences
						#then skip ahead this will determine how many inbwteen alias frames there
						#are with the var ##zoomFrameCheck##
						if((nextZoomScaleH - zoomScaleH  < 3 ) or (nextZoomScaleW - zoomScaleW <  3)):
							zoomFrameCheck += 1
						else:
							#logging.info("Size Changed after - " + str(zoomFrameCheck) + " frames")
							keepCheck = "false"
					else:
						#logging.info("Size Changed after and maxed - " + str(zoomFrameCheck) + " frames")
						keepCheck = "false"
			
			#If true this starts rendering inital frame and inbetween frames
			if(zoomFrameCheck>1):
				#get first frames
				outputimageZoomPaste = outputimageZoom.resize((zoomScaleW, zoomScaleH), Image.ANTIALIAS)
				newOutputimageZoomPaste = Image.new('RGBA', (width, height), (50, 50, 255, 255))

				offsetZ = (math.floor((width - zoomScaleW) // 2), math.floor((height - zoomScaleH) // 2))
				newOutputimageZoomPaste.paste(outputimageZoomPaste, offsetZ)
				#get next image size up for blend
			
				zoomPositionBlend = -(((fbi - blendingFrames - (currentFrame + zoomFrameCheck - 1)) / framesbetweenImages)) + 1

				zoomScaleHblend, zoomScaleWblend = getZoomScaleInt(height,width,zoomPositionBlend)
				#logging.info(fbi - blendingFrames - currentFrame + zoomFrameCheck - 1)
				#logging.info(zoomPositionBlend)
				outputimageZoomPasteBlend = outputimageZoom.resize((zoomScaleWblend, zoomScaleHblend), Image.ANTIALIAS)
				#Crop Image for blend
				newOutputimageZoomPasteBlend = Image.new('RGBA', (width, height), (50, 50, 50, 255))
		
				#logging.info("big-W"+str(zoomScaleWblend))
				#logging.info("big-H"+str(zoomScaleHblend))
				#logging.info(zoomScaleHblend)
				offsetZLarge = (math.floor((width - zoomScaleWblend) // 2), math.floor((height - zoomScaleHblend) // 2))
				
				newOutputimageZoomPasteBlend.paste(outputimageZoomPasteBlend, offsetZLarge)
				
			
				for x in range(1,zoomFrameCheck):
					blendPercent = ((x - 1)/(zoomFrameCheck - 1))
					
		
					outputimageZoomPasteBlendOutput = Image.blend(newOutputimageZoomPaste, newOutputimageZoomPasteBlend, blendPercent)
					
					#outputimage = Image.new('RGBA', (zoomScaleWblend, zoomScaleHblend), (50, 50, 255, 255))
					#outputimage.paste(outputimageZoomPasteBlendOutput, offsetZ)
					#draw = ImageDraw.Draw(outputimage)
					#draw.text((100, 100), str(blendPercent), font=font, fill="blue")
					outputimageZoomPasteBlendOutput.paste(imgTxtShadow.image, (bufferOffsetW-2, textHeight+2), imgTxtShadow.image)
					outputimageZoomPasteBlendOutput.paste(imgTxtShadow.image, (bufferOffsetW-1, textHeight+1), imgTxtShadow.image)
					outputimageZoomPasteBlendOutput.paste(imgTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTxtShadow.image)
					outputimageZoomPasteBlendOutput.paste(imgTxt.image, (bufferOffsetW, textHeight), imgTxt.image)
					video.write(cv2.cvtColor(np.array(outputimageZoomPasteBlendOutput), cv2.COLOR_RGB2BGR))
					#logging.info("Precent:"+str(blendPercent))
					currentFrame += 1
			
			#Or else just render single fream
			else:
				#logging.info(currentFrame)
				outputimageZoomPaste = outputimageZoom.resize((zoomScaleW, zoomScaleH), Image.ANTIALIAS)
				offsetZ = (math.floor((width - zoomScaleW) // 2), math.floor((height - zoomScaleH) // 2))
				outputimage.paste(outputimageZoomPaste, offsetZ)
				outputimage.paste(imgTxtShadow.image, (bufferOffsetW-2, textHeight+2), imgTxtShadow.image)
				outputimage.paste(imgTxtShadow.image, (bufferOffsetW-1, textHeight+1), imgTxtShadow.image)
				outputimage.paste(imgTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTxtShadow.image)
				outputimage.paste(imgTxt.image, (bufferOffsetW, textHeight), imgTxt.image)

				#draw = ImageDraw.Draw(outputimage)
				#draw.text((100, 100), 'Hello World!', font=font, fill="blue")
				video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
				#logging.info(currentFrame)
				currentFrame += 1
				
				
		logging.info("Blending frames image: "+str(idx)+ " curent Frame:"+ str(currentFrame))
		
		#Start Blending frame
		while (currentFrame < fbi):
			#Blending frames here
			framesLeft = (currentFrame - fbi) + blendingFrames + 1
			easePosition = -(((fbi - currentFrame - 1) / blendingFrames) - 1)
			offesetW = (width / blendingFrames) * framesLeft
			outputimage = Image.new('RGBA', (width, height), (50, 50, 50, 255))
			outputimage.paste(outputimageZoomPaste, offsetZ)
			outputimage.paste(imgTxtShadow.image, (bufferOffsetW-1, textHeight+1), imgTxtShadow.image)
			outputimage.paste(imgTxtShadow.image, (bufferOffsetW-2, textHeight+2), imgTxtShadow.image)
			outputimage.paste(imgTxtWhiteShadow.image, (bufferOffsetW + 1, newTextHeight - 1), imgTxtShadow.image)
			outputimage.paste(imgTxt.image, (bufferOffsetW, textHeight), imgTxt.image)
			if idx % 2 == 0:
				outputimage.paste(outputimageBlend, (-width + int(pytweening.easeInOutQuad(easePosition) * width),0))
			else:
				outputimage.paste(outputimageBlend, (width - int(pytweening.easeInOutQuad(easePosition) * width),0))
			video.write(cv2.cvtColor(np.array(outputimage), cv2.COLOR_RGB2BGR))
			currentFrame += 1

	try:	
		logging.info("Video saving locally")
		video.release()
		logging.info("Video saved")
		return str(path+"/"+path+".avi")
	except:
		logging.info("Video failed on realese")
		return false
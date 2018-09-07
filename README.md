# Project Title

Slideshow Reddit Bot - To compile Imgur galleries into slideshows with text and upload onto Streamable

Slideshowbot will scan Top 25 posts of a given sub and check for any Imgur galleries.
Once scanned these will compile into and slideshow avi and upload onto streamable where half of everyone will hate the result.

The video dimensions are given from the first image of gallery, within a given range.

You can see my profile here

https://www.reddit.com/user/SlideshowBot

## Getting Started

You will need to open config.py and enter in these variables from Reddit, Imgur and Streamable

```
username = "Reddit"
password = "Reddit"
client_id = "Reddit"
client_secret = "Reddit"
imgur_client_id = "Imgur"
imgur_client_secret = "Imgur"
streamusername = "Streamable"
streampass = "Streamable"
```

### Installing

What things you need to install the software and how to install them

You will need along with python 3.6.x
```
urlretrieve
ImgurClient
StreamableApi
PIL
cv2
pytweening
np
ImageText
```


### Running

To run on your command simply run 


```
py slidebot.py
```


Logging is inside log file.


There is a test script to see if the videos are rendering you can use without any login details

```
py slideTest.py
```

You will need to edit the file slideTest.py to point to any test images you wish to use. Enjoy!

## Authors

* **Mark Farrell** - *2017* - [markfarl](https://github.com/markfarl)


## License

This project is licensed under the MIT License 


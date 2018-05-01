"""
Script: SeptaNext5
Version: 2.0
Created: 4/1/2018
Created By: Paul R. Sesink Clee
Updated: 5/1/2018
Updated By: Paul R. Sesink Clee
Summary: Uses Septa's open train hackathon data to parse the status of trains
         for specific route or routes on the Regional Rail. Data is used to
         draw a time board with the next 5 trains on that route/direction that
         mimics the look of Septa's status boards. This script can be
         scheduled so that a machine always has a current board image for
         display or messaging.
"""

# region import libraries
import requests
from datetime import datetime
import time
from time import mktime
from PIL import ImageFont, Image, ImageDraw
import sys
import os
from configparser import ConfigParser
# endregion

# region setup
startTime = datetime.now()

# config parser
try:
    scriptDirectory = os.path.dirname(__file__)
    config = ConfigParser()
    config.read(os.path.join(scriptDirectory, 'SeptaNext5config.cfg'))
except:
    print('Could not read config file')
    sys.exit(1)

# declaring variables from config file
try:
    print('Parsing config file and setting up parameters...')
    departureStation = config['TrainRouteInformation']['departureStation']
    boundDirection = config['TrainRouteInformation']['boundDirection']
    trainDestination = config['TrainRouteInformation']['trainDestination']
    trainLineName = config['TrainRouteInformation']['trainLineName']
    ttf = config['TrueTypeFontFile']['TTF']
except:
    print('Config file cannot be read.')
    sys.exit(1)

# print train line text for top of board
try:
    font = ImageFont.truetype(ttf, 25)
    print('Font file accepted.')
except:
    print('Font file incompatible.')
    sys.exit(1)
# endregion

# region creating board and headers
# creating empty board image
print('Creating empty board image...')
img = Image.new(mode='RGBA', size=(600, 393), color=(0, 0, 0))                # solid black background box
draw = ImageDraw.Draw(im=img)
draw.rectangle(xy=(0, 0, 600, 65), fill=(0, 0, 102), outline=None)            # blue fill for header
draw.rectangle(xy=(0, 66, 600, 68), fill=(255, 255, 255), outline=None)       # white lines to separate rows
draw.rectangle(xy=(0, 131, 600, 133), fill=(255, 255, 255), outline=None)
draw.rectangle(xy=(0, 196, 600, 198), fill=(255, 255, 255), outline=None)
draw.rectangle(xy=(0, 261, 600, 263), fill=(255, 255, 255), outline=None)
draw.rectangle(xy=(0, 326, 600, 328), fill=(255, 255, 255), outline=None)
draw.rectangle(xy=(0, 391, 600, 393), fill=(255, 255, 255), outline=None)
draw = ImageDraw.Draw(img)

# print header train line name
w, h = draw.textsize(text=trainLineName, font=font)
leftX = ((600 - w) / 2)     # calculating text starting 'x' based on string length to center in the image
draw.text(xy=(leftX, 4), text=trainLineName, fill=(255, 255, 255), font=font)

# print status column header
statusString = 'Status'
w, h = draw.textsize(text=statusString, font=font)
statusW = w
statusX = 25
draw.text(xy=(statusX, 34), text=statusString, fill=(255, 255, 255), font=font)

# print destination column header
destinationX = 150
draw.text(xy=(destinationX, 34), text='Destination', fill=(255, 255, 255), font=font)

# print track column header
trackString = 'Track'
w, h = draw.textsize(text=trackString, font=font)
trackW = w
trackX = 430
draw.text(xy=(trackX, 34), text=trackString, fill=(255, 255, 255), font=font)

# print train column header
trainString = 'Train'
w, h = draw.textsize(text=trackString, font=font)
trainW = w
trainX = 520
draw.text(xy=(trainX, 34), text=trainString, fill=(255, 255, 255), font=font)
# endregion


# region pulling train information
print('Pulling train data...')
apiURLbase= 'http://www3.septa.org/hackathon/Arrivals/{0}/'.format(departureStation)

# trying different URLs because some do not always appear to work
try:
    apiURL = apiURLbase + 'ALL'
    r = requests.post(apiURL)
    for k, v in r.json().items():
        key = k
except:
    try:
        apiURL = apiURLbase + '80'
        r = requests.post(apiURL)
        for k, v in r.json().items():
            key = k
    except:
        try:
            apiURL = apiURLbase + '60'
            r = requests.post(apiURL)
            for k, v in r.json().items():
                key = k
        except:
            try:
                apiURL = apiURLbase + '50'
                r = requests.post(apiURL)
                for k, v in r.json().items():
                    key = k
            except:
                print('API is down.  Script terminated.')
                sys.exit('API is down.  Script terminated.')

trainRoute = r.json()[key][0][boundDirection]
# endregion

# region parsing train data and printing on board image
trainCounter = 0        # used to only pull data for 5 trains
lineY = 70              # used to calculate position for each new row
font = ImageFont.truetype(ttf, 23)

for train in trainRoute:
    if trainCounter < 5:
        if train['destination'] in trainDestination:
            strTime = time.strptime(train['depart_time'], "%Y-%m-%d %H:%M:%S.%f")
            stampTime = datetime.fromtimestamp(mktime(strTime))
            boardTime = stampTime.strftime("%I:%M")

            # print time (white)
            timeW, timeH = draw.textsize(text=boardTime, font=font)
            timeX = (statusX + (statusW / 2)) - (timeW / 2)     # centering string under 'time' header
            draw.text(xy=(timeX, lineY), text=boardTime, fill=(255, 255, 255), font=font)

            # print destination (white)
            draw.text(xy=(destinationX, lineY), text=train['destination'], fill=(255, 255, 255), font=font)

            # print status (green if on time, yellow if < 5min late, red if > 5min late)
            if train['status'] == 'On Time':
                fill = (0, 255, 0)
                statusText = 'ON TIME'
            else:
                lateMin = str(train['status'])
                lateSplit = lateMin.split(' ')
                statusText = lateSplit[0] + ' LATE'
                if int(lateSplit[0]) < 5:
                    fill = (255, 255, 0)
                else:
                    fill = (255, 0, 0)

            statusTextW, statusTextH = draw.textsize(text=statusText, font=font)
            statusTextX = (statusX + (statusW / 2)) - (statusTextW / 2)     # centering string under 'status' header
            draw.text(xy=(statusTextX, lineY + 30), text=statusText, fill=fill, font=font)

            # print service type (blue if local, yellow if express)
            if train['service_type'] == 'LOCAL':
                fill = (0, 255, 255)
            else:
                fill = (255, 255, 0)

            draw.text(xy=(destinationX, lineY + 30), text=train['service_type'], fill=fill, font=font)

            # print track information (white)
            trackNum = train['track'] + train['platform']
            trackNumW, trackNumH = draw.textsize(text=trackNum, font=font)
            trackNumX = (trackX + (trackW / 2)) - (trackNumW / 2)     # centering string under 'track' header
            draw.text(xy=(trackNumX, lineY + 15), text=trackNum, fill=(255, 255, 255), font=font)

            # print train number (blue)
            trainNum = train['train_id']
            trainNumW, trainNumH = draw.textsize(text=trainNum, font=font)
            trainNumX = (trainX + (trainW / 2)) - (trainNumW / 2)     # centering string under 'train' header
            draw.text(xy=(trainNumX, lineY + 15), text=trainNum, fill=fill, font=font)

            # updating counters
            trainCounter += 1
            lineY += 65        # increasing starting y coordinate for next line

print('Saving board image...')
draw = ImageDraw.Draw(img)
img.save('C:/Users/paul.sesinkclee/Documents/Python_Scripts/Miscellaneous/septanext5.png')

# endregion

print('Total runtime: {0}'.format(datetime.now() - startTime))

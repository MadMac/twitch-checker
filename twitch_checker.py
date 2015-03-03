#!/usr/bin/python
# -*- coding: utf-8 -*-
from twitch import *
import unicodedata
import logging
import subprocess
import thread
import time
import datetime
import sys
from colorama import init, Fore, Back, Style

import Tkinter

root = Tkinter.Tk()

filename = 'settings.txt'
following = []
file = open(filename)

TWITCHTV = TwitchTV(logging)

online = None
offline = None

# Initialize colorama

init()

# Read settings data
# Username

line = file.readline().split(' = ')
if line[0] == 'username':
    settings_data = {'username': line[1].replace('\n', '')}

# Video quality

line = file.readline().split(' = ')
if line[0] == 'default_quality':
    settings_data['default_quality'] = line[1].replace('\n', '')

# Livestreamer's path

line = file.readline().split(' = ')
if line[0] == 'livestreamer_path':
    settings_data['livestreamer_path'] = line[1].replace('\n', '')


def checkChannels():
    print settings_data

 # Get all the followed channels from profile

    following = \
        TWITCHTV.getFollowingStreams(settings_data.get('username'))
    online = following.get('live')
    offline = following.get('others')

 # Remove online channels from offline dictionary

    for i in range(0, len(online)):
        for j in range(0, len(offline)):
            if j < len(offline):
                if online[i].get('channel').get('name') \
                    == offline[j].get('name'):
                    offline.pop(j)

 # Print all the offline channels

    print Style.RESET_ALL + Fore.GREEN + Back.RED + 'Offline channels:'
    print Back.RESET + Fore.MAGENTA
    for i in range(0, len(offline)):
        print offline[i].get('display_name')

 # Print all the online channels

    print Fore.CYAN + Back.BLUE + Style.BRIGHT + 'Online channels:'
    print Back.RESET + Fore.YELLOW
    for i in range(0, len(online)):
        print Fore.YELLOW + online[i].get('channel').get('display_name')
        if online[i].get('channel').get('status') is not None:
            print Fore.CYAN + online[i].get('channel').get('status'
                    ).encode('ascii', 'ignore')
            print Fore.BLUE + 'Playing: ' + online[i].get('channel'
                    ).get('game')


def help():
    print Fore.YELLOW
    print '## HELP ##'
    print 'quit, Quit - Close'
    print 'show - Shows status of all the channels'
    print 'play channel_name (quality) - Starts livestreamer'


def startStream(channel, quality):
    print 'Starting livestreamer'
    subprocess.Popen(settings_data.get('livestreamer_path')
                    + ' twitch.tv/' + channel + ' ' + quality)


def getInput(iArray):
    raw_input()
    iArray.append(None)


def check_channel(channel_name):
    try:
        channel = TWITCHTV.getLiveStream(channel_name, 0)
        print Fore.BLUE + 'Online'
    except:
        print Fore.RED + 'Offline'


def keepUpdating(updateTime):
    iArray = []
    thread.start_new_thread(getInput, (iArray, ))
    timesLooped = 0
    while 1:
        if iArray:
            break
        time.sleep(1)
        timesLooped += 1
        if timesLooped >= updateTime * 60:
            checkChannels()
            print 'Updated at: ',
            print datetime.datetime.strftime(datetime.datetime.now(),
                    '%H:%M:%S')
            timesLooped = 0


def updateFunc(updateButton, OnlineBox, OfflineBox, selected, updateTime):

    updateText = Tkinter.Label(root, text='Updating...')
    updateText.pack()
    updateButton.config(state="disabled")
    selected[0] = None
    global online
    global offline

    root.update_idletasks()

    print settings_data
    following = \
        TWITCHTV.getFollowingStreams(settings_data.get('username'))
    online = following.get('live')
    offline = following.get('others')

 # Delete all from listbox

    OnlineBox.delete(0, int(OnlineBox.size()) - 1)

 # Remove online channels from offline dictionary

    for i in range(0, len(online)):
        for j in range(0, len(offline)):
            if j < len(offline):
                if online[i].get('channel').get('name') \
                    == offline[j].get('name'):
                    offline.pop(j)

    for i in range(0, len(online)):
        if online[i].get('channel').get('status') is not None:
            OnlineBox.insert(i+1, online[i].get('channel'
                             ).get('display_name'))

    for i in range(0, len(offline)):
        OfflineBox.insert(i, offline[i].get('display_name'))

    updateTimeString = 'Updated at: ' + datetime.datetime.strftime(datetime.datetime.now(),'%H:%M:%S')
    updateTime.config(text=updateTimeString)

    updateText.pack_forget()
    updateButton.config(state="normal")

def checkIfChannelSelected(OnlineBox, selected, watchButton, titleText):
    if OnlineBox.size() > 0:
        selected[0] = OnlineBox.index("active")
    #print selected[0]
    if selected[0] != None:
        watchButton.config(state="normal")
        titleText.config(text=online[selected[0]].get('channel').get('name') + '\n\n' + online[selected[0]].get('channel').get('status' \
                ).encode('ascii', 'ignore') + '\n' + 'Playing: ' + online[selected[0]].get('channel'
                        ).get('game'))
    else:
        watchButton.config(state="disabled")


    root.after(100, lambda: checkIfChannelSelected(OnlineBox, selected, watchButton, titleText))


if __name__ == '__main__':

    if len(sys.argv) == 2:
        if str(sys.argv[1]) == 'text':
            root.withdraw()
            checkChannels()
            input = ''
            help()
            while (input != 'quit' and input != 'Quit'):
              print Fore.RESET + Back.RESET
              input = raw_input('>> ')
              print input

              if input == 'help' or input == 'Help':
                help()
              elif input == 'show':
                checkChannels()
              elif input.split(' ')[0] == 'play':
                if len(input.split(' ')) == 2:
                  startStream(
                      input.split(' ')[1], settings_data.get('default_quality'))
                else:
                  startStream(input.split(' ')[1], input.split(' ')[2])
              elif input.split(' ')[0] == 'update':
                if len(input.split(' ')) == 2:
                  keepUpdating(float(input.split(' ')[1]))
                else:
                  print "Not enough parameters! update (time between updates in minutes)"
              elif input.split(' ')[0] == 'check':
                if len(input.split(' ')) == 2:
                  check_channel(input.split(' ')[1])
                else:
                  print "Not enough parameters! check (name of the channel)"
    else:
        selectedChannel = [None]

        root.title('Twitch')
        root.minsize(300, 500)
        root.maxsize(300, 500)
        root.geometry('%dx%d+%d+%d' % (300, 500, 200, 200))

        OnlineText = Tkinter.Label(root, text='Online')
        OnlineText.pack()
        OnlineText.place(x=10, y=10)

        OnlineBox = Tkinter.Listbox(root,font="default 9", width=20)
        OnlineBox.pack()
        OnlineBox.place(x=10, y=30)

        OfflineText = Tkinter.Label(root, text='Offline')
        OfflineText.pack()
        OfflineText.place(x=10, y=200)

        OfflineBox = Tkinter.Listbox(root ,font="default 9", width=20)
        OfflineBox.pack()
        OfflineBox.place(x=10, y=220)

        updateButton = Tkinter.Button(root, text='Update', command=lambda : \
                                      updateFunc(updateButton, OnlineBox, OfflineBox, selectedChannel, updateTime))
        updateButton.config(font="default 12", width=7)
        updateButton.pack()
        updateButton.place(x=190, y=30)

        channelButton = Tkinter.Button(root, text='Channel')
        channelButton.config(font="default 12", width=7)
        channelButton.pack()
        channelButton.place(x=190, y=80)

        watchButton = Tkinter.Button(root, text='Watch', command=lambda: startStream(online[selectedChannel[0]].get('channel').get('name'), "source"))
        watchButton.config(font="default 12", width=7)
        watchButton.pack()
        watchButton.place(x=190, y=130)

        titleText = Tkinter.Label(root, text='', anchor='w', justify='left', wraplength=250)
        titleText.pack()
        titleText.place(x=10, y=400)

        updateTime = Tkinter.Label(root, text='', wraplength=80)
        updateTime.pack()
        updateTime.place(x=190, y=180)

        root.after(100, lambda: checkIfChannelSelected(OnlineBox, selectedChannel, watchButton, titleText))
        root.mainloop()

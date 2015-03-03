#!/usr/bin/python
# -*- coding: utf-8 -*-
from twitch import *
import unicodedata
import logging
import subprocess
import thread
import time
import datetime
from colorama import init, Fore, Back, Style

import Tkinter

root = Tkinter.Tk()

filename = 'settings.txt'
following = []
file = open(filename)

TWITCHTV = TwitchTV(logging)

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


def updateFunc(updateButton, OnlineBox, OfflineBox, selected):

    updateText = Tkinter.Label(root, text='Updating...')
    updateText.pack()
    updateButton.config(state="disabled")
    selected = None
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
            OnlineBox.insert(i, online[i].get('channel'
                             ).get('display_name'))

    for i in range(0, len(offline)):
        OfflineBox.insert(i, offline[i].get('display_name'))

    updateText.pack_forget()
    updateButton.config(state="normal")

    return

def checkIfChannelSelected(OnlineBox, selected, watchButton):
    if OnlineBox.size() > 0:
        selected = OnlineBox.index("active")

    if selected != None:
        watchButton.config(state="normal")
    else:
        watchButton.config(state="disabled")


    root.after(100, lambda: checkIfChannelSelected(OnlineBox, selected, watchButton))


if __name__ == '__main__':

    selectedChannel = None

    root.title('Twitch')
    root.minsize(300, 500)
    root.maxsize(300, 500)
    root.geometry('%dx%d+%d+%d' % (300, 500, 200, 200))

    OnlineText = Tkinter.Label(root, text='Online')
    OnlineText.pack()
    OnlineText.place(x=10, y=10)

    OnlineBox = Tkinter.Listbox(root)
    OnlineBox.pack()
    OnlineBox.place(x=10, y=30)

    OfflineText = Tkinter.Label(root, text='Offline')
    OfflineText.pack()
    OfflineText.place(x=10, y=200)

    OfflineBox = Tkinter.Listbox(root)
    OfflineBox.insert(1, 'Dansgaming')
    OfflineBox.pack()
    OfflineBox.place(x=10, y=220)

    updateButton = Tkinter.Button(root, text='Update', command=lambda : \
                                  updateFunc(updateButton, OnlineBox, OfflineBox, selectedChannel))
    updateButton.pack()
    updateButton.place(x=200, y=10)

    channelButton = Tkinter.Button(root, text='Channel')
    channelButton.pack()
    channelButton.place(x=200, y=40)

    watchButton = Tkinter.Button(root, text='Watch', command=lambda: startStream("Sevadus", "source"))
    watchButton.pack()
    watchButton.place(x=200, y=70)

    root.after(100, lambda: checkIfChannelSelected(OnlineBox, selectedChannel, watchButton))
    root.mainloop()

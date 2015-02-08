from twitch import *
import unicodedata, logging
import subprocess
from colorama import init, Fore, Back, Style

filename = "settings.txt"
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
    following = TWITCHTV.getFollowingStreams(settings_data.get('username'))
    online = following.get('live')
    offline = following.get('others')

    # Remove online channels from offline dictionary
    for i in range(0, len(online)):
        for j in range(0, len(offline)):
            if j < len(offline):
                if online[i].get('channel').get('name') == offline[j].get('name'):
                    offline.pop(j)

    # Print all the offline channels
    print Style.RESET_ALL + Fore.GREEN + Back.RED  + "Offline channels:"
    print Back.RESET + Fore.MAGENTA
    for i in range(0, len(offline)):
        print offline[i].get('display_name')

    # Print all the online channels
    print Fore.CYAN + Back.BLUE + Style.BRIGHT + "Online channels:"
    print Back.RESET + Fore.YELLOW
    for i in range(0, len(online)):
        print Fore.YELLOW + online[i].get('channel').get('display_name')
        if online[i].get('channel').get('status') is not None:
            print Fore.CYAN + online[i].get('channel').get('status').encode('ascii', 'ignore')
            print Fore.BLUE + "Playing: " + online[i].get('channel').get('game')

def help():
    print Fore.YELLOW
    print "## HELP ##"
    print "quit, Quit - Close"
    print "show - Shows status of all the channels"
    print "play channel_name (quality) - Starts livestreamer"

def startStream(channel, quality):
    print "Starting livestreamer"
    subprocess.call(settings_data.get('livestreamer_path') + " twitch.tv/" + channel + " " + quality)

if __name__ == "__main__":
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
                startStream(input.split(' ')[1], settings_data.get('default_quality'))
            else:
                startStream(input.split(' ')[1], input.split(' ')[2])

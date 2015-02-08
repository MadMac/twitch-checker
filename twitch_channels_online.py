from twitch import *
import unicodedata, logging
from colorama import init, Fore, Back, Style

filename = "settings.txt"
following = []
file = open(filename)

TWITCHTV = TwitchTV(logging)

# Initialize colorama
init()

# Read settings data
line = file.readline().split(' = ')
settings_data = {'username': line[1].replace('\n', '')}
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
print Fore.GREEN + Back.RED + "Offline channels:"
print Back.RESET + Fore.MAGENTA
for i in range(0, len(offline)):
    print offline[i].get('display_name')

# Print all the online channels
print Fore.CYAN + Back.BLUE + Style.BRIGHT + "Online channels:"
print Back.RESET + Fore.YELLOW
for i in range(0, len(online)):
    print Fore.YELLOW + online[i].get('channel').get('display_name')
    print Fore.CYAN + online[i].get('channel').get('status').encode('ascii', 'ignore')
    print Fore.BLUE + "Playing: " + online[i].get('channel').get('game')

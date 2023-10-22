import discord
import time

def makePingable(user) -> str:
    ID = user.id
    return f"<@{ID}>"

def makeClickableChannel(channel) -> str:
    channelID = channel.id
    return f"<#{channelID}>"

def isValidChannel(channel) -> bool:
    return channel[0] == "<" and channel[1] == "#" and channel[len(channel) - 1] == ">"

def isValidUsername(channel) -> bool:
    return channel[0] == "<" and channel[1] == "@" and channel[len(channel) - 1] == ">"

def combineToString(arr) -> str:
    s = ""
    for i in arr:
        s += i + " "
    s = s[:len(s) - 1]
    return s

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
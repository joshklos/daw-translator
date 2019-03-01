import math
from sys import exit

# this function will take the time in hh:min:sec:frame(or something) and convert it to seconds
def timeToSeconds(time):
    split_time = time.split(":")
    minutes = 0
    hours = 0
    seconds = float(split_time[-1])
    if len(split_time) > 1:
        minutes = int(split_time[-2])
    if len(split_time) > 2:
        hours = int(split_time[-3])

    minutes = minutes + (hours*60)
    seconds = seconds + (minutes*60)
    return seconds

def secondsToMinutes(time):
    hours = 0
    minutes = 0

    if time > 3600:
        hours = int(time/3600)
    if time > 60:
        if hours > 0:
            adjustedTime = time - hours*3600
        else:
            adjustedTime = time
        minutes = int(adjustedTime/60)
    if minutes > 0:
        seconds = adjustedTime-minutes*60
        seconds = int(seconds*1000)
        seconds = float(seconds/1000)
    else:
        seconds = time

    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)

    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    if hours == 0:
        return minutes + ":" + seconds
    else:
        return str(hours) + ":" + minutes + ":" + seconds



# this function helps you view an object at any time
def displayObject(obj, indent=''):
    for (key, value) in obj.__dict__.items():
        if type(value) is str:
            print(indent + key + ":\t" + value)
        elif type(value) is int or type(value) is float:
            print(indent + key + ":\t" + str(value))
        elif type(value) is bool:
            print(indent + key + ":\t" + str(value))
        elif type(value) is list or type(value) is dict:
            print(indent + key + ":")
            for item in value:
                displayObject(item, indent + "\t")
        else:
            print(indent + key +":")
            displayObject(value, indent + "\t")

# These functions help to convert DB measurements

def powerToDb(num):
    return math.log10(num)*10

def dbToPower(num):
    temp = math.pow(10, num)
    return math.pow(temp, .1)

def powerToAmplitude(num):
    return math.sqrt(num)

def amplitudeToPower(num):
    return num*num

def dbToAmplitude(num):
    return powerToAmplitude(dbToPower(num))

def amplitudeToDb(num):
    return powerToDb(amplitudeToPower(num))


# This function shows an issue an allows the user to abort if necessary
def missingFeature(message):
    print(message)
    answerReceived = False
    while answerReceived == False:
        myAnswer = input("\nWould you like to continue? [y/N]")
        if myAnswer.lower() == 'n' or myAnswer.lower() == 'y':
            answerReceived = True
        if myAnswer.lower() == 'n':
            exit()

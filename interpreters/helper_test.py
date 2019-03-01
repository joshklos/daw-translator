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

print(secondsToMinutes(650.3))
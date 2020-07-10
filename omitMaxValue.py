# omitMaxValue.py
# Make sure the servo will not pass the maximum allowed values

def MaxValue(currentPos, stepsToTake, minPos, maxPos):
    if currentPos + stepsToTake > maxPos:
        stepsToTake = maxPos-currentPos
    if currentPos + stepsToTake < minPos:
        stepsToTake = minPos-currentPos

    return stepsToTake

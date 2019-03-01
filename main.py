from sys import argv, exit
import os
from interpreters.helpers import displayObject
from interpreter_index import interpreters

debug = False


def getFileExt(myFile):
    mySplit = myFile.split('.')
    for i in mySplit:
        pass
    return i

if len(argv) == 3:
    script, myFile, myOutput = argv
    if os.path.exists(myFile) is False:
        print("ERROR: File does not exist, please double-check the file path")
        exit()
    myType = getFileExt(myFile)
    if debug:
        print("Extension: " + myType)
    reader = ''
    for item in interpreters:
        for extension in item[0]:
            if extension == myType.lower():
                reader = item[2]()
                break
    if reader == '':
        print("ERROR: Could not find an interpreter compatible with " + myType + " file extension")
        exit()

    writer = ''
    for item in interpreters:
        if item[1].lower() == myOutput.lower():
            writer = item[2]()
            destType = item[0][0]
            break
    if writer == '':
        print("ERROR: Could not find an interpreter for " + myOutput)
        exit()

    session = reader.read(myFile, debug)
    if debug:
        displayObject(session)

    destinationFile = myFile.replace(myType, destType)
    # Add a function to check if the file already exists, and if it does
    # if the user wants to overwrite the file, or cancel the conversion
    if os.path.exists(destinationFile):
        answerReceived = False
        while answerReceived == False:
            myAnswer = input("File " + destinationFile + " already exists, would you like to overwrite it? [y/N]")
            if myAnswer.lower() == 'n' or myAnswer.lower() == 'y':
                answerReceived = True
        if myAnswer.lower() == 'n':
            print('Conversion stopped')
            exit()
    output = writer.write(session, debug)
    myOutputFile = open(destinationFile, mode='w')
    myOutputFile.write(output)
    myOutputFile.close()
    print("Conversion complete")
else:
    print("ERROR: Wrong number of arguments")



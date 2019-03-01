from xml.dom import minidom
from interpreters.object_classes import *
from interpreters.helpers import timeToSeconds, missingFeature, secondsToMinutes


class HindenburgInt(object):

    def __init__(self, version="Hindenburg Journalist 1.26.1936", version_num="1.26.1936"):
        self.version = version
        self.version_num = version_num

    def get_session_name(self):
        for i in self.projectFile.split("/"):
            name = i

        name = name.split(".")
        return name[0]

    def read(self, project_file, debug=False):
        self.projectFile = project_file
        projectXML = minidom.parse(self.projectFile)
        projectObj = Session(self.get_session_name())
        projectXML = projectXML.getElementsByTagName("Session")
        project = projectXML[0]
        projectObj.samplerate = project.getAttribute('Samplerate')
        fileSourceInfo = project.getElementsByTagName("AudioPool")[0]
        fileSourcePath = fileSourceInfo.getAttribute("Location") + "/" + fileSourceInfo.getAttribute("Path")
        projectObj.audio_folder = fileSourceInfo.getAttribute('Path')
        projectObj.folder_path = fileSourceInfo.getAttribute('Location')

        audioFiles = project.getElementsByTagName("File")
        for file in audioFiles:
            projectObj.addFile(fileSourcePath + "/" + file.getAttribute("Name"), int(file.getAttribute('Id')))

        markers = project.getElementsByTagName("Marker")
        for marker in markers:
            projectObj.addMarker(marker.getAttribute('Id'), marker.getAttribute('Name'), float(marker.getAttribute('Time')))

        tracks = project.getElementsByTagName("Track")
        for track in tracks:
            current_track = projectObj.addTrack(track.getAttribute('Name'))

            try:
                current_track.pan = self.interpretPan(track.getAttribute('Pan'))
            except:
                current_track.pan = 0

            try:
                current_track.volume = track.getAttribute('Volume')
            except:
                current_track.volume = 0

            try:
                if track.getAttribute('Solo') == "1":
                    current_track.solo = True
            except:
                current_track.solo = False

            try:
                if track.getAttribute('Mute') == "1":
                    current_track.mute = False
            except:
                current_track.mute = False

            try:
                if track.getAttribute('Rec') == "1":
                    current_track.rec = True
            except:
                current_track.rec = False


            trackItems = track.getElementsByTagName("Region")
            for item in trackItems:
                new_item = current_track.addItem(projectObj.getFileByID(int(item.getAttribute('Ref'))))
                try:
                    start = float(item.getAttribute('Start'))
                except:
                    start = 0
                new_item.startTime = start

                try:
                    startAt = float(item.getAttribute('Offset'))
                except:
                    startAt = 0
                new_item.startAt = startAt

                length = timeToSeconds(item.getAttribute('Length'))
                new_item.length = length

                try:
                    gain = float(item.getAttribute('Gain'))
                except:
                    gain = 0
                new_item.gain = gain

                new_item.name = item.getAttribute('Name')

                fades = item.getElementsByTagName('Fade')
                if fades:
                    autoEnv = current_track.getEnvelope('Volume')
                    if autoEnv == "Envelope Not Found":
                        autoEnv = current_track.addEnvelope('Volume')

                    firstFade = True

                    for fade in fades:
                        startTime = new_item.startTime + float(fade.getAttribute('Start'))
                        if firstFade:
                            startValue = new_item.gain
                        else:
                            startValue = autoEnv.points[-1].value
                            firstFade = False
                        endTime = startTime + float(fade.getAttribute('Length'))
                        try:
                            endValue = float(fade.getAttribute('Gain'))
                        except:
                            endValue = 0

                        autoEnv.addPoint(startTime, startValue)
                        autoEnv.addPoint(endTime, endValue)




            plugins = track.getElementsByTagName("Plugin")
            for plugin in plugins:
                if plugin.getAttribute('Name') == 'Compressor':
                    pluginType = "Native"
                else:
                    pluginType = "Plugin"
                new_plugin = current_track.addFX(plugin.getAttribute('Name'), pluginType, int(plugin.getAttribute('Id')))

                if pluginType == "Native":
                    if plugin.getAttribute('Name') == 'Compressor':
                        new_plugin.addProperty('UID', plugin.getAttribute('UID'))
                        new_plugin.addProperty('Comp', plugin.getAttribute('Comp'))

        return projectObj

    # Notes: Need to develop the section that reads the plugins...include support for external plugins, and the native EQ plugin

    def write(self, session, debug=False):
        if debug:
            print(destinationFile)
        self.featureCheck(session)
        myReturn = '<?xml version="1.0" encoding="utf-8"?>\n'
        myReturn = myReturn + '<Session Version="' + self.version + '" Samplerate="' + str(session.samplerate) + '">\n'
        # Need code for the audio pool here
        myReturn = myReturn + '  <Tracks>\n'
        for track in session.tracks:
            myReturn = myReturn + '    <Track Name="' + track.name + '"'
            if track.volume != 0:
                myReturn = myReturn + ' Volume="' + str(track.volume) + '"'
            if track.pan != 0:
                myReturn = myReturn + ' Pan="' + self.panBack(track.pan)
            if track.solo:
                myReturn += ' Solo="1"'
            if track.mute:
                myReturn += ' Mute="1"'
            if track.rec:
                myReturn += ' Rec="1"'
            myReturn += ">\n"
            for item in track.items:
                myReturn = myReturn + '      <Region Ref="' + str(item.source_file.itemID) + '" Name="' + item.name
                myReturn = myReturn + '" Start="' + secondsToMinutes(item.startTime) + '" Length="' + secondsToMinutes(item.length) + '"'
                if item.startTime > 0:
                    myReturn = myReturn + ' Offset="' + secondsToMinutes(item.startAt) + '"'
                myReturn = myReturn + ">\n"


        return myReturn


    def interpretPan(self, amount):
        num = -float(amount)
        num = num*90
        return num

    def panBack(self, amount):
        num = float(amount/90)
        return str(num)

    def gatherVolumeEnvelope(self, track, item):
        myVolumePoints = []
        myStartTime = item.startTime
        myEndTime = myStartTime + item.length
        if len(track.envelopes) > 0:
            for envelope in track.envelopes:
                if envelope.type == "Volume":
                    for point in envelope.points:
                        if myStartTime <= point.time <= myEndTime:
                            myVolumePoints.append(point)
        if len(myVolumePoints) > 0:
            # Order the points properly, then return them
            return False
        else:
            return False


    def featureCheck(self, session):
        for file in session.files:
            if file.fileType != "WAV":
                missingFeature('\nAll audio files for Hindenburg must be WAV files\nIf you continue you\'ll be missing some files')
        for track in session.tracks:
            for envelope in track.envelopes:
                if envelope.type == "Pan":
                    missingFeature('\nPan envelopes on tracks are not supported by Hindenburg')
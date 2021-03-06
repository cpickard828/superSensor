import sys
import subprocess
import os.path
import threading, time, random
import Queue
from sense_hat import SenseHat
import json
import io
import smbus
from vad import VoiceActivityDetector 
# PROGRAM VARIABLES
timeRun = 172800 # number of seconds to run program (86400 = 1 Day)
numRecordings = 5 # number of audio records
lengthRecording = 5 # length of each recording in seconds
frequencyTempReadings = 5 # seconds
stepTrackerSlider = 60 # The lower the number, the more precise the step/time intervals will be
sense = SenseHat()
sense.clear()
my_mutex = threading.Lock()
audioNum = 0
processNum = 0 
foNum = 0
timeStart = 0
timeEnd = 0
q = Queue.Queue()
goingFlag = True
soundName = "/home/pi/sound.json"
tempName = "/home/pi/temp.json"
lightName = "/home/pi/light.json"
movementName = "/home/pi/movement.json"
foundMean = False

# 2 digit display code from yaab-arduino.blogspot.com

OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9

# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
  abs_val = abs(val)
  tens = abs_val // 10
  units = abs_val % 10
  if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)


################################################################################
# MAIN

#sense = SenseHat()
#sense.clear()

#for i in range(0, 100):
#  show_number(i, 200, 0, 60)
#  time.sleep(0.2)

#sense.clear()
def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

class countSeconds(threading.Thread):
    def run(self):
        global timeStart
        global timeEnd
        for x in range(150):
            print "DOOF"
            time.sleep(1)
        timeEnd = time.time()

        timeElapsed = timeEnd - timeStart
        print `timeElapsed`

class createWAV(threading.Thread):
    def run(self):
        #global my_mutex
        global lengthRecording
        durLabel = "--duration=" + `lengthRecording`
        global numRecordings
        global audioNum
        global goingFlag
        totalTime = 0
        while foundMean == False:
            y=0
        #for x in range(numRecordings):
        while totalTime < timeRun:

            my_file = "/home/pi/talking" + `audioNum` + ".wav"   
            print my_file
            currTime = time.time()
            totalTime = currTime - timeStart
            totalTime = round(totalTime, 2)
            q.put(totalTime)
            #q.put(time.time() - timeStart)


            #print subprocess.check_output(['arecord',durLabel, '-vvvv', '-f', 'cd', '--file-type', 'wav', my_file])

            try:
                subprocess.check_output(['arecord',durLabel, my_file])
            except subprocess.CalledProcessError as e:
                print e.output

            audioNum = audioNum + 1
            #print subprocess.check_output(['ls'])
            #while os.path.exists(my_file) == False:
            #    print "Waiting..."

        goingFlag = False
class processWAV(threading.Thread):
    def run(self):
        #global my_mutex
        global numRecordings
        global audioNum
        global processNum
         
        megaArray = []
        #while processNum < numRecordings:
        while goingFlag == True or processNum < audioNum:
            while processNum >= audioNum:
               y=0
            #print processNum
            if processNum > 0:
                subprocess.check_output(['rm', wavFile])
            #jsonFile = "/home/pi/results" + `processNum` + ".json"
            wavFile = "/home/pi/talking" + `processNum` + ".wav"
            print "Processing " + wavFile
            foFile = "fo" + `processNum` + ".fo"
            pmFile = "pm" + `processNum` + ".pm"
            timeEnd = q.get()
            print timeEnd
            #print subprocess.check_output(['python', '/home/pi/detectVoiceInWav.py', wavFile, jsonFile, str(timeEnd)])
            v = VoiceActivityDetector(wavFile)
            raw_detection = v.detect_speech()
            speech_labels = v.convert_windows_to_readible_labels(raw_detection, str(timeEnd))
            megaArray.append(speech_labels)
            save_to_file(megaArray, soundName)
            #print subprocess.check_output(['./reaper/REAPER/build/reaper', '-i', wavFile, '-f', foFile, '-p', pmFile, '-a'])
            processNum = processNum + 1
            #if goingFlag == False and processNum >= audioNum:
             #   break

        #subprocess.check_output(['rm', wavFile])
        #megaArray = []
        #for i in range(processNum): 
        #    if i > 0:
        #        subprocess.check_output(['rm', fileName])
        #    fileName = "/home/pi/results" + `i` + ".json"
        #    with open(fileName) as json_data:
        #        d = json.load(json_data)
        #        megaArray.append(d)

        #subprocess.check_output(['rm', fileName])
        #save_to_file(megaArray, "/home/pi/results.json")
        #with open('results0.json') as json_data:
         #   d = json.load(json_data)
          #  print d
class foWAV(threading.Thread):
    def run(self):
        global numRecordings
        global audioNum
        global foNum
        while foNum >= audioNum:
            y = 0
        while foNum < numRecordings:    
            wavFile = "talking" + `processNum` + ".wav"
            foFile = "fo" + `processNum` + ".fo"
            pmFile = "pm" + `processNum` + ".pm"
            print subprocess.check_output(['./reaper/REAPER/build/reaper', '-i', wavFile, '-f', foFile, '-p', pmFile, '-a'])
            foNum = foNum + 1


class tempTaking(threading.Thread):
    def run(self):
        global frequencyTempReadings
        global goingFlag
        global timeStart
        global sense
        num = 0
        tempData = []
        while goingFlag:
            currTime = time.time()
            totalTime = currTime - timeStart
            totalTime = round(totalTime, 3)
            temp = sense.get_temperature()
            f = open("/sys/class/thermal/thermal_zone0/temp", "r")
            t = f.readline()
            t = float(int(t))/1000
            t = t * 1.8
            t = t + 32
            temp = temp *1.8
            temp = temp + 32
            tempCalibrated = temp-((t - temp)/5.466)
            tempCalibrated = round(tempCalibrated, 3)
            #tempData = []
            tempLabel = {}
            tempLabel["temperature(farenheit)"] = tempCalibrated
            tempLabel["time_taken(seconds)"] = totalTime
            tempData.append(tempLabel)
            #tempFile = "/home/pi/temp" + `num` + ".json"
            num = num + 1
            save_to_file(tempData, tempName)
            time.sleep(frequencyTempReadings)
        
        #print subprocess.check_output(['rm', 'temp0.json'])
        #print "Num" + str(num)
        #for x in range(num):
        #    print "HERE!!"
        #    tempFile = "/home/pi/temp" + `x` + ".json"
        #    print subprocess.check_output(['rm', tempFile])
        #save_to_file(tempData, "/home/pi/temp.json")


class movementDetector(threading.Thread):
    def run(self):
        global goingFlag
        global timeStart
        global stepTrackerSlider
        global foundMean
        xList = []
        yList = []
        zList = []

        movData = []
        movLabel = {}
        finalStable = False
        gap = False
        numMisses = 0
        
        print "Calibrating..."
        #sense.clear((255, 0, 0))
        while goingFlag:
            currTime = time.time()
            totalTime = currTime - timeStart
            totalTime = round(totalTime, 3)
            acceleration = sense.get_accelerometer_raw()
            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']

            x = round(x, 3)
            y = round(y, 3)
            z = round(z,3)

            stable = True
            for xCom in xList:
                if x < xCom -0.015 or x > xCom + 0.015:
                    stable = False
            #for yCom in yList:
            #    if y < yCom - 0.015 or y > yCom + 0.015:
            #        stable = False

            if stable:
                if len(xList) < 191:
                    xList.append(x)
                    yList.append(y)
                    if foundMean == False:
                        lenList = (len(xList) - 1) / 3
                        xx = lenList % 8
                        yy = lenList / 8
                        sense.set_pixel(xx, yy, [255,0,0])
            else:
                xList = []
                yList = []
                finalStable = False
                if foundMean == False:
                    sense.clear()

            if len(xList) > 190 and finalStable == False:
                print "----------Calibrated!------------"
                
                finalStable = True
                if foundMean == False:
                    sense.clear((0,255,0))
                    sense.show_letter("-", text_colour=[255,0,0])# back_colour=[0,255,0])
                    #sense.show_message("Calibrated", text_colour=(255,255,0),back_colour=(0,255,0))
                foundMean = True
                meanX = float(sum(xList))/len(xList)
                meanX = round(meanX, 3)
                meanY = float(sum(yList))/len(yList)
                meanY = round(meanY, 3)

                print "X: " + str(meanX)
                print "Y: " + str(meanY)
            if foundMean:
                if x >= meanX + 0.003 or x <= meanX -0.003: #or y>= meanY + 0.009 or y <= meanY - 0.009:
                    if gap == False:
                        movLabel = {}
                        print "^^^^^^^^^^^^^^^^^^^^^^^"
                        movLabel["beg"] = totalTime

                        sense.show_letter("-", text_colour=[0,255,0]) # back_colour=[0,255,0])
                    gap = True
                    numMisses = 0
                    #movData.append(totalTime)
                    print "Movement detected: " + "x={0}, y={1}, z={2}".format(x,y,z)

                    #sense.show_letter("!", text_colour=[0,255,0]) # back_colour=[0,255,0])
                else:
                    #gap = False
                    #sense.show_letter("-", text_colour=[0,255,0])
                    numMisses = numMisses + 1
                    if gap and numMisses >= stepTrackerSlider:

                        sense.show_letter("-", text_colour=[255,0,0])
                        gap = False
                        numMisses = 0
                        movLabel["end"] = totalTime
                        movData.append(movLabel)
                        save_to_file(movData, movementName)
        sense.clear()
        #save_to_file(movData, "/home/pi/movementData.json")

class lightSensor(threading.Thread):
    def run(self):
        global goingFlag
        global timeStart

        try:
            bus = smbus.SMBus(1)
            lightData = []
            while goingFlag:
                bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
                bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
                time.sleep(0.5)
                currTime = time.time()
                totalTime = currTime - timeStart
                totalTime = round(totalTime, 2)
                data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
                data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

                # Convert the Data
                ch0 = data[1] * 256 + data[0]
                ch1 = data1[1] * 256 + data1[0]

                lightLabel = {}

                lightLabel["time_taken"] = totalTime
                lightLabel["Inf_Val"] = ch1
                lightLabel["Vis_Val"] = ch0 - ch1
                lightData.append(lightLabel)
                save_to_file(lightData, lightName)
                print "Visible Value :%d lux" %(ch0 - ch1)
                time.sleep(4.5)
        except:
            print "\nWAT\n"
            sense.clear()

            sense.show_letter("X", text_colour=[255,0,0])# back_colour=[0,255,0])
            sys.exit(1)
#sense.show_message("Prepare for instruction...", text_colour=(255, 0, 0), back_colour=(0,0,0))

try:

    cat = smbus.SMBus(1)
    
    cat.write_byte_data(0x39, 0x00 | 0x80, 0x03)
    
    data = cat.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    print "Success"
except:
    exit(0)
sense.show_message("Set month", text_colour=(200, 0, 60))
monthPress = False
monthNum = 1
show_number(1, 200, 0, 60)
while monthPress == False:
    for event in sense.stick.get_events():
        #check if the joystick was pressed
        if event.action == "pressed":
            #check whithc direction
            if event.direction == "right" or event.direction == "up":
                monthNum = monthNum + 1
                if monthNum >= 13:
                    monthNum = 1
                sense.clear()
                show_number(monthNum, 200, 0, 60)

            if event.direction == "down" or event.direction == "left":
                monthNum = monthNum - 1
                if monthNum <= 0:
                    monthNum = 12
                sense.clear()
                show_number(monthNum, 200, 0, 60)
            if event.direction == "middle":
                monthPress = True
                break

sense.show_message("Set day", text_colour=(200, 0, 60))
dayPress = False
dayNum = 1
show_number(1, 200, 0, 60)
for event in sense.stick.get_events():
    print ""
while dayPress == False:
    for event in sense.stick.get_events():
        #check if the joystick was pressed
        if event.action == "pressed":
            #check whithc direction
            if event.direction == "right" or event.direction == "up":
                dayNum = dayNum + 1
                if dayNum >= 29:
                    if monthNum == 1 or monthNum == 3 or monthNum == 5 or monthNum == 7 or monthNum == 8 or monthNum == 10 or monthNum == 12:
                        if dayNum >= 32:
                            dayNum = 1
                    if monthNum == 2:
                        if dayNum >= 29:
                            dayNum = 1
                    if monthNum == 4 or monthNum == 6 or monthNum == 9 or monthNum == 11:
                        if dayNum >= 31:
                            dayNum = 1
                sense.clear()
                show_number(dayNum, 200, 0, 60)

            if event.direction == "down" or event.direction == "left":
                dayNum = dayNum - 1
                if dayNum <= 0:
                                        
                    if monthNum == 1 or monthNum == 3 or monthNum == 5 or monthNum == 7 or monthNum == 8 or monthNum == 10 or monthNum == 12:
                        dayNum = 31
                    if monthNum == 2:
                        dayNum = 28
                    if monthNum == 4 or monthNum == 6 or monthNum == 9 or monthNum == 11:
                        dayNum = 30
                sense.clear()
                show_number(dayNum, 200, 0, 60)
            if event.direction == "middle":
                dayPress = True
                break


sense.show_message("Set hour", text_colour=(200, 0, 60))
hourPress = False
hourNum = 0
show_number(hourNum, 200, 0, 60)

for event in sense.stick.get_events():
    print ""
while hourPress == False:
    for event in sense.stick.get_events():
        #check if the joystick was pressed
        if event.action == "pressed":
            #check whithc direction
            if event.direction == "right" or event.direction == "up":
                hourNum = hourNum + 1
                if hourNum >= 24:
                    hourNum = 0
                sense.clear()
                show_number(hourNum, 200, 0, 60)

            if event.direction == "down" or event.direction == "left":
                hourNum = hourNum - 1
                if hourNum <= 0:
                    hourNum = 23
                sense.clear()
                show_number(hourNum, 200, 0, 60)
            if event.direction == "middle":
                hourPress = True
                break

sense.show_message("Set minute", text_colour=(200, 0, 60))
minPress = False
minNum = 00
show_number(minNum, 200, 0, 60)

for event in sense.stick.get_events():
    print ""
while minPress == False:
    for event in sense.stick.get_events():
        #check if the joystick was pressed
        if event.action == "pressed":
            #check whithc direction
            if event.direction == "right" or event.direction == "up":
                minNum = minNum + 1
                if minNum >= 60:
                    minNum = 0
                sense.clear()
                show_number(minNum, 200, 0, 60)

            if event.direction == "down" or event.direction == "left":
                minNum = minNum - 1
                if minNum <= 0:
                    minNum = 59
                sense.clear()
                show_number(minNum, 200, 0, 60)
            if event.direction == "middle":
                minPress = True
                break
sense.clear()
timeStart = time.time()
print "\nMonth: " + str(monthNum) + "  Day: " + str(dayNum) + "  Time: " + str(hourNum) + ":" + str(minNum)

fileNum = 0
if os.path.isfile("/home/pi/light.json"):
    exists = True
    while exists:
        fileNum = fileNum + 1
        pathName = "/home/pi/light" + str(fileNum) + ".json"
        exists = os.path.isfile(pathName)

    soundName = "/home/pi/sound" + str(fileNum) + ".json"
    tempName = "/home/pi/temp" + str(fileNum) + ".json"
    lightName = "/home/pi/light" + str(fileNum) + ".json"
    movementName = "/home/pi/movement" + str(fileNum) + ".json"
    print lightName
    
timeArray = []
timeLabel = {}
timeLabel["month"] = monthNum
timeLabel["day"] = dayNum
timeLabel["hour"] = hourNum
timeLabel["min"] = minNum
timeArray.append(timeLabel)
if fileNum == 0:
    timeName = "/home/pi/time.json"
else:
    timeName = "/home/pi/time" + str(fileNum) + ".json"
save_to_file(timeArray, timeName)

t1 = createWAV()
t2 = processWAV()
t3 = tempTaking()
t4 = movementDetector()
t5 = lightSensor()

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()


for event in sense.stick.get_events():
    print ""


#print subprocess.check_output(['arecord','--duration=5','talking1.wav'])
#my_file = "talking1.wav"
#while os.path.exists(my_file) == False:
#    print "Waiting..."
#print subprocess.check_output(['python', 'detectVoiceInWav.py', 'talking1.wav', 'results1.json'])
#print subprocess.check_output(['./reaper/REAPER/build/reaper', '-i', 'talking1.wav', '-f', 'talking1.fo', '-p', 'bla.pm', '-a'])

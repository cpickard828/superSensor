from sense_hat import SenseHat

sense = SenseHat()

xList = []
yList = []
zList = []
finalStable = False
foundMean = False
print "Calibrating..."
while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    

    x=round(x,3)
    y=round(y,3)
    z=round(z,3)
    print "X: " + str(x) + "Y: " + str(y)
    stable = True
    for xCom in xList:
        if x < xCom -0.01 or x > xCom + 0.01:
            stable = False

    for yCom in yList:
        if y < yCom -0.01 or y > yCom + 0.01:
            stable = False

    if stable:
        if len(xList) < 251:
            xList.append(x)
            yList.append(y)
    else:
        xList = []
        yList = []
        finalStable = False

    if len(xList)>250 and finalStable == False:
        print "----------------Calibrated!---------------"
        finalStable = True
        foundMean = True
        meanX = float(sum(xList))/len(xList)
        meanX = round(meanX, 3)
        meanY = float(sum(yList))/len(yList)
        meanY = round(meanY, 3)
        print "X: " + str(meanX)
        print "Y: " + str(meanY)
    if foundMean:
        if x >= meanX + .008 or x <= meanX - 0.008 or y >= meanY + 0.008 or y <= meanY - 0.008:
            print "Movement detected: " +  "x={0}, y={1}, z={2}".format(x,y,z)
            #print("x={0}, y={1}, z={2}".format(x,y,z))
    #print("x={0}, y={1}, z={2}".format(x,y,z))

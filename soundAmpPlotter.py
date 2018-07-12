import matplotlib.pyplot as plt
import json
import sys
if len(sys.argv) < 2:
    print "Error: too few command line arguments"
    print "Usage: python tempPlotter.py foo.json (graph.png)"
    sys.exit(1)

with open(sys.argv[1]) as json_data:
    d = json.load(json_data)
counter = 0
for x in d:
    seg = x[len(x) - 1]
    x1 = seg["time_started"]
    x2 = float(seg["time_started"]) + float(seg["length_of_recording"])
    xx = [x1, x2]
    med = [seg["med_amp"], seg["med_amp"]]
    mean = [seg["mean_amp"], seg["mean_amp"]]
    #maxY = [seg["max_amp"], seg["max_amp"]]
    y25 = [seg["25_amp"], seg["25_amp"]]
    y75 = [seg["75_amp"], seg["75_amp"]]

    #plt.plot(xx, maxY, marker='o', markerfacecolor='blue', color='skyblue', label = 'Max' if counter == 0 else "")

    plt.plot(xx, mean, color='red', linestyle='dashed', label='Mean' if counter == 0 else "")
    
    plt.plot(xx, y75, color='blue', label = "75th perc." if counter == 0 else "")
    plt.plot(xx, med, color='green', label='Median' if counter == 0 else "")
    plt.plot(xx, y25, color='olive', label="25th perc." if counter == 0 else "")

    if counter == 0:
        counter = counter + 1
plt.xlabel('Time (seconds)')
plt.ylabel('Digital Amplitude')
plt.title('Digital Amplitude over Time')
plt.legend()
#plt.show()
if len(sys.argv)==2:
    plt.savefig("/home/pi/graphs/soundAmp.png")
else:
    plt.savefig("/home/pi/graphs/" + sys.argv[2])

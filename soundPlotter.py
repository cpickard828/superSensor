import matplotlib.pyplot as plt
import json
import sys
if len(sys.argv) != 2:
    print "Error: wrong number of command line arguments"
    print "Usage: python tempPlotter.py foo.json"
    sys.exit(1)

with open(sys.argv[1]) as json_data:
    d = json.load(json_data)

for x in d:
    seg = x[len(x) - 1]
    x1 = seg["time_started"]
    x2 = float(seg["time_started"]) + float(seg["length_of_recording"])
    xx = [x1, x2]
    y = [seg["percent_time_w_speech"], seg["percent_time_w_speech"]]
    plt.plot(xx, y)
plt.title("Speech Detection")
plt.xlabel("Time (seconds)")
plt.ylabel("Percentage of Time Interval where Speech was Detected")
#plt.show()
plt.savefig('/home/pi/graphs/speechDet.png')

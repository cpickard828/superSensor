import sys
import matplotlib.pyplot as plt
import json

if len(sys.argv) != 2:
    print "Error: wrong number of command line arguments"
    print "Usage: python tempPlotter.py foo.json"
    sys.exit(1)


with open(sys.argv[1]) as json_data:
    d = json.load(json_data)

for a in d:
    y = round(a["temperature(farenheit)"], 3)
    x = round(a["time_taken(seconds)"], 3)

    plt.plot([x], [y], marker="o", markersize=3, color="red")
plt.title("Temperature over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Temperature (Farenheit)")
#plt.show()
plt.savefig("/home/pi/graphs/temp.png")

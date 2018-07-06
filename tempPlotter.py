import sys
import matplotlib.pyplot as plt
import json

if len(sys.argv) < 2:
    print "Error: too few command line arguments"
    print "Usage: python tempPlotter.py foo.json (graph.png)"
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
if len(sys.argv) == 2:
    plt.savefig("/home/pi/graphs/temp.png")
else:
    plt.savefig("/home/pi/graphs/" + sys.argv[2])

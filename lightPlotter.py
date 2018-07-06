import sys
import matplotlib.pyplot as plt
import json

if len(sys.argv)  < 2:
    print "Error: too few command line arguments"
    print "Usage: python tempPlotter.py foo.json (graph.png)"
    sys.exit(1)

with open(sys.argv[1]) as json_data:
    d = json.load(json_data)
counter = 0
for a in d:
    x = a["time_taken"]
    y1 = a["Vis_Val"]
    y2 = a["Inf_Val"]

    plt.plot([x], [y2], marker="x", color="red", markersize=5, label = "Infrared" if counter == 0 else "")
    plt.plot([x], [y1], marker="o", color="blue", markersize=3, label = "Visible" if counter == 0 else "")


    if counter == 0:
        counter = counter + 1
plt.legend()
plt.xlabel("Time (seconds)")
plt.ylabel("Lux")
plt.title("Lux Readings over Time")
#plt.show()
if len(sys.argv) == 2:
    plt.savefig("/home/pi/graphs/light.png")
else:
    plt.savefig("/home/pi/graphs/" + sys.argv[2])

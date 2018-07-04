import matplotlib.pyplot as plt
import json

with open("movementData.json") as json_data:
    d = json.load(json_data)

y = [1, 1]
for x in d:
    plt.plot([x["beg"], x["end"]], y, color="blue")
plt.title("Movmement Detection over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("= 1.0 if Movement Detected")
#plt.show()
plt.savefig("/home/pi/graphs/movement.png")
#x1 = [1, 4.5]
#y1 = [1, 1]
#x2 = [6.2, 7.7]
#x3 = [14.4, 16.9]
#plt.plot(x1, y1)
#plt.plot(x2, y1)
#plt.plot(x3, y1)
#plt.show()

# superSensor
# Cameron Pickard

If this is your first time operating this raspberryPi, make sure to follow the installations.txt instructions!!

	- Also watch my powerpoint to see how to run the Pi as a user.

Make sure the camera is plugged in, and the light sensor is connected correctly.

If camera and light sensor are connected upon bootup of the raspberryPi, the program will start automatically.

Main program is main.py. Run the superSensor by typing "sudo python main.py". Sudo is IMPORTANT.

main.py does much of the speech detection through code in vad.py.

All "Plotter.py" files are used to plot data from their respective .json files in the dayX/A/ directories. Of course, data must be collected first for this functionality to be used. 

To see plotter usage, just type "sudo python tempPlotter.py" to see the usage of the tempPlotter, for example.

Most other files in this directory are test files I created before implementing code in main.py, and can be ignored.


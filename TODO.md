# Things left to accomplish...
# Cameron Pickard

- Create a 3D Printed case
	- almost done...
- Fine tune movement detection algorithm in main.py
	- Not quite perfect
- Finish implementing the functionality of thread #6 in main.py
	- This thread was intended to detect bluetooth low-energy devices and SSID's of wifi networks

- BIG ISSUE: In main.py, fix audio processing thread so that it doesn't so far behind the audio recording thread.
	- I semi-fixed by checking for low-amplitude before processing...
	- But this was not enough; major gaps in thread progress after 24 hours of program running
	- Could potentially be fixed by letting the audio recording thread take a few hours off each night?
	- Worst case scenario: The thread code is poorly optimized and needs to be rewritten.

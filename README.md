# rigol_ds1054z
Python Class for controlling the Rigol DS1054z Oscilloscope

There is no license for this work... it is use at your own risk (I assume no liability).

This python class uses visa, which means that you will need to install: pyusb, pyvisa and pyvisa-py
See this article on setting these up and testing:
https://hackaday.com/2016/11/16/how-to-control-your-instruments-from-a-computer-its-easier-than-you-think/
If using linux and a raspberry pi, you will want to make the pi user a member of the usb group. This will allow
you to not need to run as root.

I wanted to control my Rigol DS1054z in python to automate my scope initization and data collection.
I am a hardware guy and my only formal training is a C++ class in college. My purpose in sharing the code
is to help others... if you find any bugs please let me know and I will upload the fix.

The two coolest parts of the code is (1) save a screen capture to a file and (2) easily collect waveform data.
You may also like how I can easily perform any measurement the scope offers, and specify units like s, ms, us and 
v, mv and uv. 

**Note: you will need to edit rigol_ds1054z to specify your specific scope device. See the hackaday webpage for how to do this.

**Note: when using "write_waveform_data" the first character in the data file is invalid, it needs to be manually stripped from the file. I could not find an easy way to remove it. If you find a way, please let me know.

Files:
rigol_ds1054z.py <- this is a class which will be imported by the high-level script
test_rigol.py    <- this is the high-level script that creates an instance of the class and calls functions

I hope this helps at least one person.

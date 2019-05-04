import visa
import datetime
import time
import re
import csv
from math import floor, log10

class rigol_ds1054z:
	
	# Constructor
	def __init__(self, debug=False):
		resources = visa.ResourceManager('@py')
		# insert your device here
		# resources.list_resources() will show you the USB resource to put below
		self.oscilloscope = resources.open_resource('USB0::6833::1230::DS1ZA192107675::0::INSTR')
		self.debug = debug

	def print_info(self):
		self.oscilloscope.write('*IDN?')
		fullreading = self.oscilloscope.read_raw()
		readinglines = fullreading.splitlines()
		print("Scope information: " + readinglines[0])
		time.sleep(2)
	
	class measurement:
		def __init__(self, name='', description='', command='', unit='', return_type=''):
			self.name        = name
			self.description = description
			self.command     = command
			self.unit        = unit
			self.return_type = return_type
	
	max_voltage           = measurement(name='max_voltage',          command='VMAX', unit='Volts',         return_type='float', description='voltage value from the highest point of the waveform to the GND')
	min_voltage           = measurement(name='min_voltage',          command='VMIN', unit='Volts',         return_type='float', description='voltage value from the lowest point of the waveform to the GND')
	peak_to_peak_voltage  = measurement(name='peak_to_peak_voltage', command='VPP',  unit='Volts',         return_type='float', description='voltage value from the highest point to the lowest point of the waveform')
	top_voltage           = measurement(name='top_voltage',          command='VTOP', unit='Volts',         return_type='float', description='voltage value from the flat top of the waveform to the GND')
	base_voltage          = measurement(name='base_voltage',         command='VBAS', unit='Volts',         return_type='float', description='voltage value from the flat base of the waveform to the GND')
	top_to_base_voltage   = measurement(name='top_to_base_voltage',  command='VAMP', unit='Volts',         return_type='float', description='voltage value from the top of the waveform to the base of the waveform')
	average_voltage       = measurement(name='average_voltage',      command='VAVG', unit='Volts',         return_type='float', description='arithmetic average value on the whole waveform or on the gating area')
	rms_voltage           = measurement(name='rms_voltage',          command='VRMS', unit='Volts',         return_type='float', description='root mean square value on the whole waveform or the gating area')
	upper_voltage         = measurement(name='upper_voltage',        command='VUP',  unit='Volts',         return_type='float', description='actual voltage value corresponding to the threshold maximum value')
	mid_voltage           = measurement(name='mid_voltage',          command='VMID', unit='Volts',         return_type='float', description='actual voltage value corresponding to the threshold middle value')
	lower_voltage         = measurement(name='lower_voltage',        command='VLOW', unit='Volts',         return_type='float', description='actual voltage value corresponding to the threshold minimum value')
	overshoot_voltage     = measurement(name='overshoot_percent',    command='OVER', unit='%%',            return_type='float', description='ratio of the difference of the maximum value and top value of the waveform to the amplitude value')
	preshoot_voltage      = measurement(name='preshoot_percent',     command='PRES', unit='%%',            return_type='float', description='ratio of the difference of the minimum value and base value of the waveform to the amplitude value')
	variance_voltage      = measurement(name='variance_voltage',     command='VARI', unit='Volts',         return_type='float', description='average of the sum of the squares for the difference between the amplitude value of each waveform point and the waveform average value on the whole waveform or on the gating area')
	period_rms_voltage    = measurement(name='period_rms_voltage',   command='PVRMS',unit='Volts',         return_type='float', description='root mean square value within a period of the waveform')
	period_time           = measurement(name='period_time',          command='PER',  unit='Seconds',       return_type='float', description='time between the middle threshold points of two consecutive, like-polarity edges')
	frequency             = measurement(name='frequency',            command='FREQ', unit='Hz',            return_type='float', description='reciprocal of period')
	rise_time             = measurement(name='rise_time',            command='RTIM', unit='Seconds',       return_type='string',description='time for the signal amplitude to rise from the threshold lower limit to the threshold upper limit')
	fall_time             = measurement(name='fall_time',            command='FTIM', unit='Seconds',       return_type='string',description='time for the signal amplitude to fall from the threshold upper limit to the threshold lower limit')
	positive_width_time   = measurement(name='positive_width_time',  command='PWID', unit='Seconds',       return_type='float', description='time difference between the threshold middle value of a rising edge and the threshold middle value of the next falling edge of the pulse')
	negative_width_time   = measurement(name='negative_width_time',  command='NWID', unit='Seconds',       return_type='float', description='time difference between the threshold middle value of a falling edge and the threshold middle value of the next rising edge of the pulse')
	positive_duty_percent = measurement(name='positive_duty_ratio',  command='PDUT', unit='%%',            return_type='float', description='ratio of the positive pulse width to the period')
	negative_duty_percent = measurement(name='negative_duty_ratio',  command='NDUT', unit='%%',            return_type='float', description='ratio of the negative pulse width to the period')
	max_voltage_time      = measurement(name='max_voltage_time',     command='TVMAX',unit='Seconds',       return_type='float', description='time corresponding to the waveform maximum value')
	min_voltage_time      = measurement(name='min_voltage_time',     command='TVMIN',unit='Seconds',       return_type='float', description='time corresponding to the waveform minimum value')
	positive_pulse_number = measurement(name='positive_pulse_number',command='PPUL', unit='Occurances',    return_type='int',   description='number of positive pulses that rise from below the threshold lower limit to above the threshold upper limit')
	negative_pulse_number = measurement(name='negative_pulse_number',command='NPUL', unit='Occurances',    return_type='int',   description='number of negative pulses that fall from above the threshold upper limit to below the threshold lower limit')
	positive_edges_number = measurement(name='positive_edges_number',command='PEDG', unit='Occurances',    return_type='int',   description='number of rising edges that rise from below the threshold lower limit to above the threshold upper limit')
	negative_edges_number = measurement(name='negative_edges_number',command='NEDG', unit='Occurances',    return_type='int',   description='number of falling edges that fall from above the threshold upper limit to below the threshold lower limit')
	rising_delay_time     = measurement(name='rising_delay_time',    command='RDEL', unit='Seconds',       return_type='string',description='time difference between the falling edges of source 1 and source 2. Negative delay indicates that the selected falling edge of source 1 occurred after that of source 2')
	falling_delay_time    = measurement(name='falling_delay_time',   command='FDEL', unit='Seconds',       return_type='string',description='time difference between the falling edges of source 1 and source 2. Negative delay indicates that the selected falling edge of source 1 occurred after that of source 2')
	rising_phase_ratio    = measurement(name='rising_phase_ratio',   command='RPH',  unit='Degrees',       return_type='float', description='rising_delay_time / period_time x 360 degrees')
	falling_phase_ratio   = measurement(name='falling_phase_ratio',  command='FPH',  unit='Degrees',       return_type='float', description='falling_delay_time / period_time x 360 degrees')
	positive_slew_rate    = measurement(name='positive_slew_rate',   command='PSLEW',unit='Volts / Second',return_type='float', description='divide the difference of the upper value and lower value on the rising edge by the corresponding time')
	negative_slew_rate    = measurement(name='negative_slew_rate',   command='NSLEW',unit='Volts / Second',return_type='float', description='divide the difference of the lower value and upper value on the falling edge by the corresponding time')
	waveform_area         = measurement(name='waveform_area',        command='MAR',  unit='Volt Seconds',  return_type='float', description='algebraic sum of the area of the whole waveform within the screen. area of the waveform above the zero reference is positive and the area of the waveform below the zero reference is negative')
	first_period_area     = measurement(name='first_period_area',    command='MPAR', unit='Volt Seconds',  return_type='float', description='algebraic sum of the area of the first period of the waveform on the screen. area of the waveform above the zero reference is positive and the area of the waveform below the zero reference is negative')

	single_measurement_list = [max_voltage,         min_voltage,           peak_to_peak_voltage,  top_voltage,           base_voltage,          top_to_base_voltage,
							   average_voltage,     rms_voltage,           upper_voltage,         mid_voltage,           lower_voltage,         overshoot_voltage,
							   preshoot_voltage,    variance_voltage,      period_rms_voltage,    period_time,           frequency,             rise_time,
							   fall_time,           positive_width_time,   negative_width_time,   positive_duty_percent, negative_duty_percent, max_voltage_time,
							   min_voltage_time,    positive_pulse_number, negative_pulse_number, positive_edges_number, negative_edges_number, positive_slew_rate,
							   negative_slew_rate,  waveform_area,         first_period_area]

	double_measurement_list = [rising_phase_ratio, falling_phase_ratio, rising_delay_time, falling_delay_time]

	def powerise10(self, x):
		""" Returns x as a*10**b with 0 <= a < 10"""
		if x == 0: return 0,0
		Neg = x < 0
		if Neg: x = -x
		a = 1.0 * x / 10**(floor(log10(x)))
		b = int(floor(log10(x)))
		if Neg: a = -a
		return a,b
	
	def eng_notation(self, x):
		"""Return a string representing x in an engineer friendly notation"""
		a,b = self.powerise10(x)
		if -3 < b < 3: return "%.4g" % x
		a = a * 10**(b % 3)
		b = b - b % 3
		return "%.4gE%s" % (a,b)

	def get_measurement(self, channel=1, meas_type=max_voltage):
		self.oscilloscope.write(':MEAS:ITEM? ' + meas_type.command + ',CHAN' + str(channel))
		fullreading = self.oscilloscope.read_raw()
		readinglines = fullreading.splitlines()
		if (meas_type.return_type == 'float'):
			reading = float(readinglines[0])
			if (meas_type.unit == '%%'):
				percentage_reading = reading*100
				print ("Channel " + str(channel) + " " + meas_type.name + " value is %0.2F " + meas_type.unit) % percentage_reading
			else:
				eng_reading = self.eng_notation(reading)
				print ("Channel " + str(channel) + " " + meas_type.name + " value is " + eng_reading + " " + meas_type.unit)
		elif (meas_type.return_type == 'int'):
			reading = int(float(readinglines[0]))
			print ("Channel " + str(channel) + " " + meas_type.name + " value is %d " + meas_type.unit) % reading
		else:
			reading = str(readinglines[0])
			print ("Channel " + str(channel) + " " + meas_type.name + " value is " + reading + " " + meas_type.unit)
		return reading
	
	# if no filename is provided, the timestamp will be the filename
	def write_screen_capture(self, filename=''):
		self.oscilloscope.write(':DISP:DATA? ON,OFF,PNG')
		raw_data = self.oscilloscope.read_raw()[11:] # strip off first 11 bytes
		# save image file
		if (filename == ''):
			filename = "rigol_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".png"
		fid = open(filename, 'wb')
		fid.write(raw_data)
		fid.close()
		print ("Wrote screen capture to filename " + '\"' + filename + '\"')
		time.sleep(5)
		
	def close(self):
		self.oscilloscope.close()
		print "Closed USB session to oscilloscope"
		
	def reset(self):
		self.oscilloscope.write('*RST')
		print "Reset oscilloscope"
		time.sleep(8)
		
	# probe should either be 10.0 or 1.0, per the setting on the physical probe
	def setup_channel(self, channel=1, on=1, offset_divs=0.0, volts_per_div=1.0, probe=10.0):
		if (on == 1):
			self.oscilloscope.write(':CHAN' + str(channel) + ':DISP ' + 'ON')
			self.oscilloscope.write(':CHAN' + str(channel) + ':SCAL ' + str(volts_per_div))
			self.oscilloscope.write(':CHAN' + str(channel) + ':OFFS ' + str(offset_divs*volts_per_div))
			self.oscilloscope.write(':CHAN' + str(channel) + ':PROB ' + str(probe))
			print ("Turned on CH" + str(channel) + ", position is " + str(offset_divs) + " divisions from center, " + str(volts_per_div) + " volts/div, scope is " + str(probe) + "x")
		else:
			self.oscilloscope.write(':CHAN' + str(channel) + ':DISP OFF')
			print ("Turned off channel " + str(channel))
	
	def val_and_unit_to_real_val(self, val_with_unit='1s'):
		number = int(re.search(r"([0-9]+)",val_with_unit).group(0))
		unit = re.search(r"([a-z]+)",val_with_unit).group(0).lower()
		if (unit == 's' or unit == 'v'):
			real_val_no_units = number
		elif (unit == 'ms' or unit == 'mv'):
			real_val_no_units = number * 0.001
		elif (unit == 'us' or unit == 'uv'):
			real_val_no_units = number * 0.000001
		elif (unit == 'ns' or unit == 'nv'):
			real_val_no_units = number * 0.000000001
		else:
			real_val_no_units = number
		return real_val_no_units

	# remember to always use lowercase time_per_div units, the regex look for lowercase
	def setup_timebase(self, time_per_div='1ms', delay='1ms'):
		time_per_div_real = self.val_and_unit_to_real_val(time_per_div)
		self.oscilloscope.write(':TIM:MAIN:SCAL ' + str(time_per_div_real))
		print ("Timebase was set to " + time_per_div + " per division")
		delay_real = self.val_and_unit_to_real_val(delay)
		self.oscilloscope.write(':TIM:MAIN:OFFS ' + str(delay_real))
	
	# remember to always use lowercase level units, the regex look for lowercase
	def setup_trigger(self, channel=1, slope_pos=1, level='100mv'):
		level_real = self.val_and_unit_to_real_val(level)
		self.oscilloscope.write(':TRIG:EDG:SOUR CHAN' + str(channel))
		if (slope_pos == 0):
			self.oscilloscope.write(':TRIG:EDG:SLOP NEG')
		else:
			self.oscilloscope.write(':TRIG:EDG:SLOP POS')
		self.oscilloscope.write(':TRIG:EDG:LEV ' + str(level_real))
		if (slope_pos == 1):
			print ("Triggering on CH" + str(channel) + " positive edge with level of " + level)
		else:
			print ("Triggering on CH" + str(channel) + " negative edge with level of " + level)
	
	# decode channel is either 1 or 2, only two decodes can be present at any time
	# use uppercase for encoding, valid choices are HEX, ASC, DEC, BIN, LINE
	# position_divs is the number of division (from bottom) to position the decode
	def setup_i2c_decode(self, decode_channel=1, on=1, sda_channel=1, scl_channel=2, encoding='HEX', position_divs=1.0):
		if (on == 0):
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':CONF:LINE OFF')
		else:
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':MODE IIC')
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':DISP ON')
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':FORM ' + encoding)
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':POS ' + str(400-position_divs*50))
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':THRE AUTO')
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':CONF:LINE ON')
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':IIC:CLK CHAN' + str(scl_channel))
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':IIC:DATA CHAN' + str(sda_channel))
			self.oscilloscope.write(':DEC' + str(decode_channel) + ':IIC:ADDR RW')

	def single_trigger(self):
		self.oscilloscope.write(':SING')
		time.sleep(3)
		
	def force_trigger(self):
		self.oscilloscope.write(':TFOR')
		time.sleep(3)
		
	def run_trigger(self):
		self.oscilloscope.write(':RUN')
		time.sleep(3)
		
	# only allowed values are 6e3, 6e4, 6e5, 6e6, 12e6 for single channels
	# only allowed values are 6e3, 6e4, 6e5, 6e6, 12e6 for   dual channels
	# only allowed values are 3e3, 3e4, 3e5, 3e6, 6e6  for 3 or 4 channels
	# the int conversion is needed for scientific notation values
	def setup_mem_depth(self, memory_depth=12e6):
		self.oscilloscope.write(':ACQ:MDEP ' + str(int(memory_depth)))
		print "Acquire memory depth set to %d samples" % memory_depth

	def write_waveform_data(self, channel=1, filename=''):
		self.oscilloscope.write(':WAV:SOUR: CHAN' + str(channel))
		time.sleep(1)
		self.oscilloscope.write(':WAV:MODE NORM')
		self.oscilloscope.write(':WAV:FORM ASC')
		self.oscilloscope.write(':ACQ:MDEP?')
		fullreading = self.oscilloscope.read_raw()
		readinglines = fullreading.splitlines()
		mdepth = int(readinglines[0])
		num_reads = (mdepth / 15625) +1
		if (filename == ''):
			filename = "rigol_waveform_data_channel_" + str(channel) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".csv"
		fid = open(filename, 'wb')
		print ("Started saving waveform data for channel " + str(channel) + " " + str(mdepth) + " samples to filename " + '\"' + filename + '\"')
		for read_loop in range(0,num_reads):
			self.oscilloscope.write(':WAV:DATA?')
			fullreading = self.oscilloscope.read_raw()
			readinglines = fullreading.splitlines()
			reading = str(readinglines[0])
			reading = reading.replace(",", "\n")
			fid.write(reading)
		fid.close()

	def write_scope_settings_to_file(self, filename=''):
		self.oscilloscope.write(':SYST:SET?')
		raw_data = self.oscilloscope.read_raw()[11:] # strip off first 11 bytes
		
		if (filename == ''):
			filename = "rigol_settings_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".stp"
		fid = open(filename, 'wb')
		fid.write(raw_data)
		fid.close()
		print ("Wrote oscilloscope settings to filename " + '\"' + filename + '\"')
		time.sleep(5)
		
	def restore_scope_settings_from_file(self, filename=''):
		if (filename == ''):
			print "ERROR: must specify filename\n"
		else:
			with open(filename, mode='rb') as file: # b is important -> binary
				fileContent = file.read()
				valList = list()
				#alter ending to append new CRLF
				fileContent = fileContent + chr(13) + chr(10)
				#convert to a list that write_binary_values can iterate
				for x in range(0,len(fileContent)-1):
					valList.append(ord(fileContent[x]))
				self.oscilloscope.write_binary_values(':SYST:SET ', valList, datatype='B', is_big_endian=True) 
			print ("Wrote oscilloscope settings to scope")
			time.sleep(8)

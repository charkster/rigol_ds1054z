from rigol_ds1054z import rigol_ds1054z
import time
import smbus

# rigol_ds1054z class functions were writen to allow the high-level script
#  to be easy to read. Values with units are passed as strings, where the
#  unit can be stripped and converted to a base-10 value to be multiplied
#  by the value passed with it. This script sets up I2C decoding on the scope
#  to demonstrate triggering on SDA data (you don't need a slave device,
#  the scope is just observing the master write out to the bus)

scope = rigol_ds1054z()
scope.print_info()
scope.reset()
scope.setup_channel(channel=1,on=1,offset_divs=2.0, volts_per_div=2.0)
scope.setup_channel(channel=2,on=1,offset_divs=-2.0,volts_per_div=2.0)
scope.setup_timebase(time_per_div='2us',delay='10us')
scope.setup_mem_depth(memory_depth=6e3)
scope.setup_trigger(channel=1,slope_pos=1,level='500mv')
scope.setup_i2c_decode(sda_channel=1, scl_channel=2)
scope.single_trigger()
i2c = smbus.SMBus(1)
i2c.write_quick(0x50) #
time.sleep(3)
for measurement in scope.single_measurement_list:
	scope.get_measurement(channel=1, meas_type=measurement)
for measurement in scope.single_measurement_list:
	scope.get_measurement(channel=2, meas_type=measurement)
scope.get_measurement(channel=1, meas_type=scope.max_voltage)
scope.write_screen_capture(filename='rigol_i2c_no_slave.png')
scope.write_waveform_data(channel=1)
scope.write_waveform_data(channel=2)
scope.close()

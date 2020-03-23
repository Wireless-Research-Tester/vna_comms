import pyvisa as visa
import numpy

class data:
    def __init__(self, measurement_type, freq, theta, phi, value):
        self.measurement_type=measurement_type
        self.freq=freq
        self.theta=theta
        self.phi=phi
        self.value=value
    
class lin_freq:
    def __init__(self, start, end, points):
        self.start = start
        self.end = end
        self.points = points

def reset():
    rm = visa.ResourceManager()
    rm.list_resources()
    vna=rm.open_resource('GPIB0::16::INSTR')	#Make sure that the VNA HP-IB address is set to 16
    vna.read_termination = '\n'
    vna.write('PRES')	#Resetting VNA
    vna.write('FORM4')
    print(vna.query('*IDN?'))
	
def setup(freq_settings, sweep_type):	#for freq_settings contains list of frequencies, please order frequencies from smallest to largest
	rm = visa.ResourceManager()
	vna=rm.open_resource('GPIB0::16::INSTR')
	if(sweep_type==1):              #sweep_type: 1 means frequency list, 0 means linear frequency
		if(len(freq_settings)>32):	#if sweep_type is frequency list, only take a max of 32 frequencies 
			print('too many frequencies!')
			return 0
		for i in range(0, len(freq_settings)):
			freq = freq_settings[i]
			vna.write('EDITLIST;SADD; CENT %d HZ; SDON' % freq)
			vna.write('LISFREQ')
		return 1
	else:
		print('linear frequency...')	#if freq_settings contains linear frequency settings, see format in lin_freq class definition	
		vna.write('STAR %d HZ' % freq_settings.start)
		vna.write('STOP %d HZ' % freq_settings.end)
		vna.write('POIN %d' % freq_settings.points)
		vna.write('LINFREQ')
		return 1
	
def get_S21(freq_settings, sweep_type, theta, phi):
    temp_dataset = []
    rm = visa.ResourceManager()
    vna=rm.open_resource('GPIB0::16::INSTR')
    vna.read_termination = '\n'
    vna.write('S21')
    vna.write('AUTO')
    vna.write('DATI')
    vna.write('DISPMEMO')   #might not need this tho
    vna.write('OUTPFORM')
    if(sweep_type==1):
        for i in range(0, len(freq_settings)):
            temp_dataset.append(data('S21', freq_settings[i], theta, phi, vna.read_ascii_values()[0]))
    else:
        span = freq_settings.end - freq_settings.start
        for i in range(0, freq_settings.points):
            temp_dataset.append(data('S21', freq_settings.start+i*span/(freq_settings.points-1), theta, phi, vna.read_ascii_values()[0]))
    return temp_dataset
    
def get_S11(freq_settings, sweep_type, theta, phi):
    temp_dataset = []
    rm = visa.ResourceManager()
    vna=rm.open_resource('GPIB0::16::INSTR')
    vna.read_termination = '\n'
    vna.write('S11')
    vna.write('AUTO')
    vna.write('DATI')
    vna.write('DISPMEMO')
    vna.write('OUTPFORM')
    if(sweep_type==1):
        for i in range(0, len(freq_settings)):
            temp_dataset.append(data('S11', freq_settings[i], theta, phi, vna.read_ascii_values()[0]))
    else:
        span = freq_settings.end - freq_settings.start
        for i in range(0, freq_settings.points):
            temp_dataset.append(data('S11', freq_settings.start+i*span/(freq_settings.points-1), theta, phi, vna.read_ascii_values()[0]))
    return temp_dataset
    

def calibrate():
	print('work in progress!')
	

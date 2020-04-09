import pyvisa as visa
import numpy
from syntaxes import find_command, Action, Model

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

def reset(model):
    rm = visa.ResourceManager()
    rm.list_resources()
    vna=rm.open_resource('GPIB0::16::INSTR')	#Make sure that the VNA HP-IB address is set to 16
    vna.read_termination = '\n'
    vna.write(find_command(model,Action.RESET))	#Resetting VNA
    vna.write(find_command(model,Action.FORM4)) 
    vna.close()


def setup(freq_settings, sweep_type, avg, bw, model):	#for freq_settings contains list of frequencies, please order frequencies from smallest to largest
    rm = visa.ResourceManager()
    vna=rm.open_resource('GPIB0::16::INSTR')
    if(sweep_type==1):              #sweep_type: 0-linear frequency, 1-frequency list
        if(len(freq_settings)>30):	#if sweep_type is frequency list, only take a max of 30 frequencies
            print('too many frequencies in frequency list!')
            return 1
        for i in range(0, len(freq_settings)):
            freq = freq_settings[i]
            vna.write(find_command(model,Action.ADD_LIST_FREQ,freq))
            vna.write(find_command(model,Action.LIST_FREQ_MODE))
    else:
        vna.write(find_command(model, Action.LIN_FREQ_START, freq_settings.start))
        vna.write(find_command(model, Action.LIN_FREQ_END, freq_settings.end))
        vna.write(find_command(model, Action.LIN_FREQ_POINTS, freq_settings.points))
        vna.write(find_command(model, Action.LIN_FREQ_MODE))
    vna.write(find_command(model, Action.AVG_FACTOR, avg))
    vna.write(find_command(model, Action.AVG_ON))
    vna.write(find_command(model, Action.AVG_RESET))
    vna.write(find_command(model, Action.IF_BW, bw))
    vna.close()
    return 0


def get_data(freq_settings, sweep_type, theta, phi, data_type, model): #data_type: 0-S11, 1-S21
    temp_dataset = []
    rm = visa.ResourceManager()
    vna=rm.open_resource('GPIB0::16::INSTR')
    vna.read_termination = '\n'
    if(data_type==1):
        vna.write(find_command(model, Action.S21))
    else:
        vna.write(find_command(model, Action.S11))
    vna.write(find_command(model, Action.AUTO_SCALE))
    vna.write(find_command(model, Action.DATA_TO_MEM))
    vna.write(find_command(model, Action.DISPLAY_MEM))
    vna.write(find_command(model, Action.OUTPUT_FORMATTED_DATA))
    if(sweep_type==1):
        for i in range(0, len(freq_settings)):
            if(data_type==1):
                temp_dataset.append(data('S21', freq_settings[i], theta, phi, vna.read_ascii_values()[0]))
            else:
                temp_dataset.append(data('S11', freq_settings[i], theta, phi, vna.read_ascii_values()[0]))
    else:
        span = freq_settings.end - freq_settings.start
        for i in range(0, freq_settings.points):
			freq = freq_settings.start+i*span/(freq_settings.points-1)
            if(data_type==1):
                temp_dataset.append(data('S21', freq, theta, phi, vna.read_ascii_values()[0]))
            else:
                temp_dataset.append(data('S11', freq, theta, phi, vna.read_ascii_values()[0]))
    vna.close()
    return temp_dataset


def calibrate(model):
    rm = visa.ResourceManager()
    vna=rm.open_resource('GPIB0::16::INSTR')
    vna.write(find_command(model, Action.CAL_S11_1_PORT))
    input('Connect OPEN circuit to PORT 1. Press enter when ready...')
    vna.write(find_command(model, Action.CAL_S11_1_PORT_OPEN))
    input('Connect SHORT circuit to PORT 1. Press enter when ready...')
    vna.write(find_command(model, Action.CAL_S11_1_PORT_SHORT))
    input('Connect matched LOAD to PORT 1. Press enter when ready...')
    vna.write(find_command(model, Action.CAL_S11_1_PORT_LOAD))
    vna.write(find_command(model, Action.SAVE_1_PORT_CAL))
    print('Calibration is complete!')
    vna.close()

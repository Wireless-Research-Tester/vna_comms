import pyvisa as visa
import math
from syntaxes import find_command, Action, check_model


class data:
    def __init__(self, measurement_type, freq, theta, phi, value_mag, value_phase):
        self.measurement_type = measurement_type
        self.freq = freq
        self.theta = theta
        self.phi = phi
        self.value_mag = value_mag
        self.value_phase = value_phase


class lin_freq:
    def __init__(self, start, end, points):
        self.start = start
        self.end = end
        self.points = points


class session:
    def __init__(self, resource):
        self.rm = visa.ResourceManager()
        self.vna = self.rm.open_resource(resource)
        self.vna.read_termination = '\n'
        self.model = check_model(self.vna.query('*IDN?'))
        self.vna.write(find_command(self.model, Action.FORM4))
        self.freq = None

    def reset(self):
        self.vna.write(find_command(self.model, Action.RESET))

    def setup(self, freq, avg, bw):
        self.freq = freq
        if isinstance(self.freq, list):
            if len(self.freq) > 30:  # if sweep type is frequency list, only take a max of 30 frequencies
                print('too many frequencies in frequency list!')
                return 1
            for i in range(0, len(self.freq)):
                freq_temp = self.freq[i]
                self.vna.write(find_command(self.model, Action.ADD_LIST_FREQ, freq_temp))
                self.vna.write(find_command(self.model, Action.LIST_FREQ_MODE))
        else:
            self.vna.write(find_command(self.model, Action.LIN_FREQ_START, self.freq.start))
            self.vna.write(find_command(self.model, Action.LIN_FREQ_END, self.freq.end))
            self.vna.write(find_command(self.model, Action.LIN_FREQ_POINTS, self.freq.points))
            self.vna.write(find_command(self.model, Action.LIN_FREQ_MODE))
        self.vna.write(find_command(self.model, Action.AVG_FACTOR, avg))
        self.vna.write(find_command(self.model, Action.AVG_ON))
        self.vna.write(find_command(self.model, Action.AVG_RESET))
        self.vna.write(find_command(self.model, Action.IF_BW, bw))
        return 0

    def get_data(self, theta, phi, data_type):
        temp_dataset = []
        if data_type == 'S21':
            self.vna.write(find_command(self.model, Action.S21))
        else:
            self.vna.write(find_command(self.model, Action.S11))
        self.vna.write(find_command(self.model, Action.POLAR))
        self.vna.write(find_command(self.model, Action.POLAR_LOG_MARKER))
        self.vna.write(find_command(self.model, Action.AUTO_SCALE))
        self.vna.write(find_command(self.model, Action.DATA_TO_MEM))
        self.vna.write(find_command(self.model, Action.DISPLAY_MEM))
        self.vna.write(find_command(self.model, Action.OUTPUT_FORMATTED_DATA))
        if isinstance(self.freq, list):
            for i in range(0, len(self.freq)):
                rectangular_temp = self.vna.read_ascii_values()
                mag_temp = 20 * math.log(
                    math.sqrt(rectangular_temp[0] * rectangular_temp[0] + rectangular_temp[1] * rectangular_temp[1]),
                    10)
                phase_temp = phase(rectangular_temp)
                if data_type == 'S21':
                    temp_dataset.append(data('S21', self.freq[i], theta, phi, mag_temp, phase_temp))
                else:
                    temp_dataset.append(data('S11', self.freq[i], theta, phi, mag_temp, phase_temp))
        else:
            span = self.freq.end - self.freq.start
            for i in range(0, self.freq.points):
                freq = self.freq.start + i * span / (self.freq.points - 1)
                rectangular_temp = self.vna.read_ascii_values()
                mag_temp = 20 * math.log(
                    math.sqrt(rectangular_temp[0] * rectangular_temp[0] + rectangular_temp[1] * rectangular_temp[1]),
                    10)
                phase_temp = phase(rectangular_temp)
                if data_type == 1:
                    temp_dataset.append(data('S21', freq, theta, phi, mag_temp, phase_temp))
                else:
                    temp_dataset.append(data('S11', freq, theta, phi, mag_temp, phase_temp))
        return temp_dataset

    def calibrate(self):
        self.vna.write(find_command(self.model, Action.CAL_S11_1_PORT))
        input('Connect OPEN circuit to PORT 1. Press enter when ready...')
        self.vna.write(find_command(self.model, Action.CAL_S11_1_PORT_OPEN))
        input('Connect SHORT circuit to PORT 1. Press enter when ready...')
        self.vna.write(find_command(self.model, Action.CAL_S11_1_PORT_SHORT))
        input('Connect matched LOAD to PORT 1. Press enter when ready...')
        self.vna.write(find_command(self.model, Action.CAL_S11_1_PORT_LOAD))
        self.vna.write(find_command(self.model, Action.SAVE_1_PORT_CAL))
        print('Calibration is complete!')


def phase(rect_coord):
    if rect_coord[0] == 0:
        if rect_coord[1] > 0:
            p = 90
        else:
            p = -90
    elif rect_coord[1] == 0:
        if rect_coord[0] > 0:
            p = 0
        else:
            p = 180
    else:
        p = math.degrees(math.atan(rect_coord[1] / rect_coord[0]))

    if rect_coord[0] < 0:
        if rect_coord[1] > 0:
            p = p + 180
        elif rect_coord[1] < 0:
            p = p - 180
    return p

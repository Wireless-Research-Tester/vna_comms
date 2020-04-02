import numpy

class data:
    def __init__(self, measurement_type, freq, theta, phi, value):
        self.measurement_type=measurement_type
        self.freq=freq
        self.theta=theta
        self.phi=phi
        self.value=value
        
#theta set to 90 degrees, 10 total frequencies: 1 GHz, 1.1 GHz...1.9 GHz 
def get_data(): 
    temp_dataset = []
    for i in range(0, 360):
        temp_dataset.append(data('S21', 1000000000, 90, i, round(-30-abs(i-180)/6,4)))
        temp_dataset.append(data('S21', 1100000000, 90, i, round(-30-abs(i-170)/6,4)))
        temp_dataset.append(data('S21', 1200000000, 90, i, round(-30-abs(i-160)/6,4)))
        temp_dataset.append(data('S21', 1300000000, 90, i, round(-30-abs(i-150)/6,4)))
        temp_dataset.append(data('S21', 1400000000, 90, i, round(-30-abs(i-140)/6,4)))
        temp_dataset.append(data('S21', 1500000000, 90, i, round(-30-abs(i-130)/6,4)))
        temp_dataset.append(data('S21', 1600000000, 90, i, round(-30-abs(i-120)/6,4)))
        temp_dataset.append(data('S21', 1700000000, 90, i, round(-30-abs(i-110)/6,4)))
        temp_dataset.append(data('S21', 1800000000, 90, i, round(-30-abs(i-100)/6,4)))
        temp_dataset.append(data('S21', 1900000000, 90, i, round(-30-abs(i-90)/6,4)))
    return temp_dataset

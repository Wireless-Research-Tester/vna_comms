import vna_comms as comms
import time


sess = comms.session('GPIB0::16::INSTR')
sess.reset()
time.sleep(3)
sess.setup([10, 20, 30, 40, 50], 8, 3000)
time.sleep(5)
sess.calibrate()
time.sleep(1)
temp = sess.get_data(90, 75, 'S21')
for i in range(0, len(temp)):
    print("Measurement Type: {}, Frequency: {} MHz, Magnitude: {} dB, Phase: {} degrees".format(temp[i].measurement_type
                                                                                                , temp[i].freq,
                                                                                                temp[i].value_mag,
                                                                                                temp[i].value_phase))

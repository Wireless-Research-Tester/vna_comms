import vna_comms as comms
import time

sess = comms.session('GPIB0::16::INSTR')
list_points = [5, 10, 15, 20, 25, 30]
lin_points = [201, 401, 801, 1601]
IF_BW = 3700
avg_list = [8]

file = open("avg_timing_results.csv", 'w')
file.write('sweep_type,points,avg_factor,data_type,data_complete_time\n')

# list frequency sweep timing
for pts in list_points:
    freq_list = []
    for i in range(0, pts):
        freq_list.append(1 + i * 5999/(pts-1))
    for avg in avg_list:
        sess.reset()
        sess.setup(freq_list, avg, IF_BW)
        print("Type: list, Pts: {}, Avg: {}".format(pts, avg))
        sess.rst_avg('S11')

        start_time = time.time()
        temp = sess.get_data(90, 45, 'S11')
        data_duration_s11 = time.time() - start_time

        sess.rst_avg('S21')

        start_time = time.time()
        temp = sess.get_data(90, 45, 'S21')
        data_duration_s21 = time.time() - start_time

        file = open("avg_timing_results.csv", 'a')
        file.write("list,{},{},S11,{},\n".format(pts, avg, data_duration_s11))
        file.write("list,{},{},S21,{},\n".format(pts, avg, data_duration_s21))
        file.close()

# linear frequency sweep timing:
for pts in lin_points:
    freq_list = comms.lin_freq(1, 6000, pts)
    for avg in avg_list:
        sess.reset_all()
        sess.setup(freq_list, avg, IF_BW)
        print("Type: linear, Pts: {}, Avg: {}".format(pts, avg))
        sess.rst_avg('S11')

        start_time = time.time()
        temp = sess.get_data(90, 45, 'S11')
        data_duration_s11 = time.time() - start_time

        sess.rst_avg('S21')

        start_time = time.time()
        temp = sess.get_data(90, 45, 'S21')
        data_duration_s21 = time.time() - start_time

        file = open("avg_timing_results.csv", 'a')
        file.write("linear,{},{},S11,{},\n".format(pts, avg, data_duration_s11))
        file.write("linear,{},{},S21,{},\n".format(pts, avg, data_duration_s21))
        file.close()
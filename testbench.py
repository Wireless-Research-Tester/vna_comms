import vna_comms as comms


def tb_2():
    sess = comms.session('GPIB0::16::INSTR')
    sess.reset_all()
    sess.setup([1000, 1500, 2000], 8, 3700)
    temp = sess.get_data(90, 180, 'S21')
    print(temp[0].value_mag, temp[0].value_phase)
    print(temp[1].value_mag, temp[1].value_phase)
    print(temp[2].value_mag, temp[2].value_phase)

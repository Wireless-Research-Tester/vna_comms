from enum import Enum, auto


class Action(Enum):
    RESET = auto()
    FORM4 = auto()
    ADD_LIST_FREQ = auto()
    LIST_FREQ_MODE = auto()
    LIN_FREQ_START = auto()
    LIN_FREQ_END = auto()
    LIN_FREQ_POINTS = auto()
    LIN_FREQ_MODE = auto()
    AVG_FACTOR = auto()
    AVG_ON = auto()
    AVG_RESET = auto()
    IF_BW = auto()
    S21 = auto()
    S11 = auto()
    POLAR = auto()
    POLAR_LOG_MARKER = auto()
    AUTO_SCALE = auto()
    DATA_TO_MEM = auto()
    DISPLAY_MEM = auto()
    OUTPUT_FORMATTED_DATA = auto()
    CAL_S11_1_PORT = auto()
    CAL_S11_1_PORT_OPEN = auto()
    CAL_S11_1_PORT_SHORT = auto()
    CAL_S11_1_PORT_LOAD = auto()
    SAVE_1_PORT_CAL = auto()


class Model(Enum):
    HP_8753D = auto()


def check_model(string):
    if '8753D' in string:
        return Model.HP_8753D
    else:
        return 0


def find_command(model, action, arg=0):
    commands = {
        Action.RESET: RESET(model),
        Action.FORM4: FORM4(model),
        Action.ADD_LIST_FREQ: ADD_LIST_FREQ(model, arg),
        Action.LIST_FREQ_MODE: LIST_FREQ_MODE(model),
        Action.LIN_FREQ_START: LIN_FREQ_START(model, arg),
        Action.LIN_FREQ_END: LIN_FREQ_END(model, arg),
        Action.LIN_FREQ_POINTS: LIN_FREQ_POINTS(model, arg),
        Action.LIN_FREQ_MODE: LIN_FREQ_MODE(model),
        Action.AVG_FACTOR: AVG_FACTOR(model, arg),
        Action.AVG_ON: AVG_ON(model),
        Action.AVG_RESET: AVG_RESET(model),
        Action.IF_BW: IF_BW(model, arg),
        Action.S21: S21(model),
        Action.S11: S11(model),
        Action.POLAR: POLAR(model),
        Action.POLAR_LOG_MARKER: POLAR_LOG_MARKER(model),
        Action.AUTO_SCALE: AUTO_SCALE(model),
        Action.DATA_TO_MEM: DATA_TO_MEM(model),
        Action.DISPLAY_MEM: DISPLAY_MEM(model),
        Action.OUTPUT_FORMATTED_DATA: OUTPUT_FORMATTED_DATA(model),
        Action.CAL_S11_1_PORT: CAL_S11_1_PORT(model),
        Action.CAL_S11_1_PORT_OPEN: CAL_S11_1_PORT_OPEN(model),
        Action.CAL_S11_1_PORT_SHORT: CAL_S11_1_PORT_SHORT(model),
        Action.CAL_S11_1_PORT_LOAD: CAL_S11_1_PORT_LOAD(model),
        Action.SAVE_1_PORT_CAL: SAVE_1_PORT_CAL(model),
    }
    return commands.get(action)


def RESET(model):
    commands = {
        Model.HP_8753D: 'PRES',
    }
    return commands.get(model)


def FORM4(model):
    commands = {
        Model.HP_8753D: 'FORM4',
    }
    return commands.get(model)


def ADD_LIST_FREQ(model, arg):
    argument_valid = {
        Model.HP_8753D: arg * 10 ** 6 in range(30000, 6 * 10 ** 9),
    }

    commands = {
        Model.HP_8753D: 'EDITLIST; SADD; CENT %d MHZ; SDON' % arg,
    }
    if (argument_valid.get(model)):
        return commands.get(model)
    else:
        return 0


def LIST_FREQ_MODE(model):
    commands = {
        Model.HP_8753D: 'LISFREQ',
    }
    return commands.get(model)


def LIN_FREQ_START(model, arg):
    argument_valid = {
        Model.HP_8753D: arg * 10 ** 6 in range(30000, 6 * 10 ** 9),
    }

    commands = {
        Model.HP_8753D: 'STAR %d MHZ' % arg,
    }
    if (argument_valid.get(model)):
        return commands.get(model)
    else:
        return 0


def LIN_FREQ_END(model, arg):
    argument_valid = {
        Model.HP_8753D: arg * 10 ** 6 in range(30000, 6 * 10 ** 9),
    }

    commands = {
        Model.HP_8753D: 'STOP %d MHZ' % arg,
    }
    if (argument_valid.get(model)):
        return commands.get(model)
    else:
        return 0


def LIN_FREQ_POINTS(model, arg):
    argument_valid = {
        Model.HP_8753D: arg in range(1, 1633),
    }

    commands = {
        Model.HP_8753D: 'POIN %d' % arg,
    }
    if argument_valid.get(model):
        return commands.get(model)
    else:
        return 0


def LIN_FREQ_MODE(model):
    commands = {
        Model.HP_8753D: 'LINFREQ',
    }
    return commands.get(model)


def AVG_FACTOR(model, arg):
    argument_valid = {
        Model.HP_8753D: arg in range(1, 1000),
    }

    commands = {
        Model.HP_8753D: 'AVERFACT %d' % arg,
    }
    if (argument_valid.get(model)):
        return commands.get(model)
    else:
        return 0


def AVG_ON(model):
    commands = {
        Model.HP_8753D: 'AVERO1',
    }
    return commands.get(model)


def AVG_RESET(model):
    commands = {
        Model.HP_8753D: 'AVERREST',
    }
    return commands.get(model)


def IF_BW(model, arg):
    argument_valid = {
        Model.HP_8753D: arg == 10 or arg == 30 or arg == 100 or arg == 300 or arg == 1000 or arg == 3000 or arg == 3700,
    }

    commands = {
        Model.HP_8753D: 'IFBW %d' % arg,
    }
    if argument_valid.get(model):
        return commands.get(model)
    else:
        return 0


def S21(model):
    commands = {
        Model.HP_8753D: 'S21',
    }
    return commands.get(model)


def S11(model):
    commands = {
        Model.HP_8753D: 'S11',
    }
    return commands.get(model)


def POLAR(model):
    commands = {
        Model.HP_8753D: 'POLA'
    }
    return commands.get(model)


def POLAR_LOG_MARKER(model):
    commands = {
        Model.HP_8753D: 'POLMLOG'
    }
    return commands.get(model)


def AUTO_SCALE(model):
    commands = {
        Model.HP_8753D: 'AUTO',
    }
    return commands.get(model)


def DATA_TO_MEM(model):
    commands = {
        Model.HP_8753D: 'DATI',
    }
    return commands.get(model)


def DISPLAY_MEM(model):
    commands = {
        Model.HP_8753D: 'DISPMEMO',
    }
    return commands.get(model)


def OUTPUT_FORMATTED_DATA(model):
    commands = {
        Model.HP_8753D: 'OUTPFORM',
    }
    return commands.get(model)


def CAL_S11_1_PORT(model):
    commands = {
        Model.HP_8753D: 'CALIS111',
    }
    return commands.get(model)


def CAL_S11_1_PORT_OPEN(model):
    commands = {
        Model.HP_8753D: 'CLASS11A',
    }
    return commands.get(model)


def CAL_S11_1_PORT_SHORT(model):
    commands = {
        Model.HP_8753D: 'CLASS11B',
    }
    return commands.get(model)


def CAL_S11_1_PORT_LOAD(model):
    commands = {
        Model.HP_8753D: 'CLASS11C',
    }
    return commands.get(model)


def SAVE_1_PORT_CAL(model):
    commands = {
        Model.HP_8753D: 'SAV1',
    }
    return commands.get(model)

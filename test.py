import pyfirmata
from pyfirmata import Arduino
from Device.Motor import Model_17HS3401, Model_MG90S
from Device.Switch import Model_2A
from Tools.Json import loadJson
from Structure.Arm import PickDropMechanism_V1
from Structure.BarLinkage import FourBarLinkage

# Get config in json
PATH_CONFIG = 'config_driver.json'
config = loadJson(PATH_CONFIG)

# Get all config for device
config_board = config['board']
config_ena_motor = config['ena_motor']

config_motor_right = config['motor_right']
config_switch_right = config['switch_right']

config_motor_left = config['motor_left']
config_switch_left = config['switch_left']

config_motor_arm = config['motor_arm']

# Config all device
board = Arduino(config_board)
pyfirmata.util.Iterator(board).start()

ena_motor_pin = config_ena_motor['pin']
ena_pin = board.get_pin(f'd:{ena_motor_pin}:o')
ena_pin.write(config_ena_motor['input'])

switch_right = Model_2A(board=board, **config_switch_right)
motor_right = Model_17HS3401(board=board, **config_motor_right)

motor_arm = Model_MG90S(board=board, **config_motor_arm)

switch_left = Model_2A(board=board, **config_switch_left)
motor_left = Model_17HS3401(board=board, **config_motor_left)


link_1 = FourBarLinkage(motor=motor_right, limit_swith=[switch_right, None])
link_1.step(20000)
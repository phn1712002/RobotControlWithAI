import pyfirmata
from pyfirmata import Arduino
from Tools.Json import loadJson
from Device.Motor import Model_17HS3401, Model_MG90S
from Device.Switch import Model_2A
from Device.Gear import SpurGear
from Structure.Arm import PickDropMechanism_V1
from Structure.BarLinkage import FourBarLinkage


###  Get config in json ### 

PATH_CONFIG = 'config_driver.json'
config = loadJson(PATH_CONFIG)

###  Get all config for device ### 

config_board = config['board']
config_ena_motor = config['ena_motor']

config_motor_right = config['motor_right']
config_switch_right = config['switch_right']

config_motor_left = config['motor_left']
config_switch_left = config['switch_left']

config_motor_arm = config['motor_arm']

### Config all device ### 

# Config board
board = Arduino(config_board)
pyfirmata.util.Iterator(board).start()

# Enable motor stepper in CNC V3
ena_motor_pin = config_ena_motor['pin']
ena_pin = board.get_pin(f'd:{ena_motor_pin}:o')
ena_pin.write(config_ena_motor['input'])

# Config switch and motor right
switch_right = Model_2A(board=board, **config_switch_right)
motor_right = Model_17HS3401(board=board, **config_motor_right)

# Config switch and motor left
switch_left = Model_2A(board=board, **config_switch_left)
motor_left = Model_17HS3401(board=board, **config_motor_left)

# Config motor arm
motor_arm = Model_MG90S(board=board, **config_motor_arm)

### Config structure robot ### 
link_1 = FourBarLinkage(motor=motor_right, limit_swith=[switch_right, None], )
gear_link_1 = SpurGear(z=[1, 2])
link_1.step(steps=gear_link_1.calcParameter(200, True))

link_2 = FourBarLinkage(motor=motor_left, limit_swith=[switch_left, None])

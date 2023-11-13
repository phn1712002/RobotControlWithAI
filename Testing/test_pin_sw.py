import keyboard as kb
from Tools.CMD import clearCMD
from Structure.Robot import Robot_V1

# Create all object
clearCMD()
PATH_CONFIG = 'config_driver.json'
rb = Robot_V1(PATH_CONFIG)

while not kb.is_pressed('esc'):
    print(f"{rb.multi_switch.switch_left.checkClick()} - {rb.multi_switch.switch_mid.checkClick()} - {rb.multi_switch.switch_right.checkClick()}")

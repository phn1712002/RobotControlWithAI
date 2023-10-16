from Structure.Robot import Robot_V1

PATH_CONFIG = 'config_driver.json'
rb = Robot_V1(PATH_CONFIG)
rb.controlOneLink(1, 120)

while True:
    print(f"{rb.switch_right.checkClick()} - {rb.switch_left.checkClick()} - {rb.switch_a_2motor.checkClick()}")
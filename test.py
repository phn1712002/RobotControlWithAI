from Structure.Robot import Robot_V1

PATH_CONFIG = 'config_driver.json'
rb = Robot_V1(PATH_CONFIG)
rb.controlOneLink(1, 120)
rb.controlOneLink(2, 120)

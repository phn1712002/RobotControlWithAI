from Structure.Robot import Robot_V1
PATH_CONFIG = 'config_driver.json'
rb = Robot_V1(PATH_CONFIG)

rb.controlOneLink(index=0, angle_or_oc=-100)

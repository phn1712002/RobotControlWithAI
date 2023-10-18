import numpy as np, keyboard as kb
from Tools.Excel import writeExcel
from Structure.Robot import Robot_V1


PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)

while True:
    random_link_action = np.random.randint(low=0, high=3)
    random_angle_action = np.random.randint(low=-360, high=360)
    status_angle_current = rb.getAngleThreeLink()
    _, check_break = rb.controlOneLink(index_link=random_link_action, angle_or_oc=random_angle_action)
    data_save = [random_link_action, 
                 random_angle_action, 
                 status_angle_current[0], 
                 status_angle_current[1], 
                 status_angle_current[2], 
                 int(check_break)]
    writeExcel(path=PATH_EXCEL, data=data_save)
    if kb.is_pressed('esc'):
        break
    
import numpy as np, keyboard as kb
from Tools.Excel import writeExcel
from Structure.Robot import Robot_V1
PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)

while True:
    link = np.random.randint(low=1, high=3)
    angle = np.random.randint(low=20, high=180)
    sign = np.random.randint(low=-100, high=100)
    if sign == 0: angle = 0
    else: angle = sign * angle / abs(sign)
    
    print(f"{link} : {angle}")
    print(f"{rb.multi_switch.limit_left} - {rb.multi_switch.limit_right}")
    
    rb.controlOneLink(index_link=link, angle_or_oc=angle)
    if kb.is_pressed('esc'): break                  
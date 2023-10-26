import numpy as np, keyboard as kb
from Tools.Excel import writeExcel
from Structure.Robot import Robot_V1
PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)

while True:
    link = np.random.randint(low=1, high=3)
    angle = np.random.randint(low=40, high=180)
    sign = np.random.randint(low=-1, high=2)
    print(f"{link} : {sign*angle}")
    rb.controlOneLink(index_link=link, angle_or_oc=sign*angle)
    if kb.is_pressed('esc'): break                       
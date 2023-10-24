import numpy as np, keyboard as kb
from Tools.Excel import writeExcel
from Structure.Robot import Robot_V1


PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)
check_break = rb.controlOneLink(index_link=2, angle_or_oc=-99999)
check_break = rb.controlOneLink(index_link=1, angle_or_oc=99999)
check_break = rb.controlOneLink(index_link=2, angle_or_oc=99999)

                       
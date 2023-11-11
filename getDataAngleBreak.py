import numpy as np, keyboard as kb, time, os
from Tools.Excel import writeExcel
from Structure.Robot import Robot_V1


PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)
time_delay_steps = 0.1


# Loop
while not kb.is_pressed('esc'):
    # Create paramenter
    link = np.random.randint(low=1, high=3)
    angle = np.random.randint(low=20, high=180)
    sign = np.random.randint(low=-100, high=100)
    if sign == 0: angle = 0
    else: angle = sign * angle / abs(sign)
    
    # Print info
    #os.system('cls')
    #print(f"{link} : {angle} : {rb.multi_switch.limit_left} - {rb.multi_switch.limit_right}")
    
    # Enter
    #while True: 
    #    if kb.is_pressed('enter'): break   
    
    # Control RB
    rb.controlOneLink(index_link=link, angle_or_oc=angle)
    
    # Stop in time
    time.sleep(time_delay_steps)                
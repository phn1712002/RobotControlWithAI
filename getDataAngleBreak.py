import numpy as np, keyboard as kb, time, os
from Tools.Excel import writeExcel
from Tools.CMD import clearCMD
from Structure.Robot import Robot_V1


PATH_CONFIG = 'config_driver.json'
PATH_EXCEL = './Dataset/Dataset_AngleBreak.xlsx'
rb = Robot_V1(PATH_CONFIG)
time_delay_steps = 0.1


# Loop
count = 0
while not kb.is_pressed('esc'):
    # Count id
    count +=1 
    
    # Create paramenter
    link = np.random.randint(low=1, high=3)
    angle = np.random.randint(low=20, high=180)
    sign = np.random.randint(low=-100, high=100)
    if sign == 0: angle = 0
    else: angle = sign * angle / abs(sign)
    
    # Print info
    clearCMD()
    print(f"ID: {count} - Link: {link} - Angle: {angle}")
      
    # Control RB
    break_check = rb.controlOneLink(index_link=link, angle_or_oc=angle)
    
    # Save data
    data_save = {
        'link': link,
        'angle': angle,
        'break_check': break_check
    }
    writeExcel(path=PATH_EXCEL, data=data_save)
    
    # Stop in time
    time.sleep(time_delay_steps)                
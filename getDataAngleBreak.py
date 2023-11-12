import numpy as np, keyboard as kb, time
from Tools.Excel import writeExcel
from Tools.CMD import clearCMD
from Structure.Robot import Robot_V1

# Create all
clearCMD()
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
    angle_input = round(np.random.uniform(low=-180, high=180), 2)
    
    # Print info
    clearCMD()
    print(f"ID: {count} - Link: {link} - Angle: {angle_input} - Limit: {rb.multi_switch.limit_left} - {rb.multi_switch.limit_right}")
    
    # Control RB
    angle_before_steps = rb.getAngleOneLink(index_link=link)
    angle_after_steps, in_progress_break = rb.controlOneLink(index_link=link, angle_or_oc=angle_input)
    
    # Save data to excel
    data_save = {
        'id': count,
        'link': link,
        'angle_before_steps': angle_before_steps,
        'angle_input': angle_input,
        'angle_after_steps': angle_after_steps,
        'in_progress_break': int(in_progress_break)
    }
    print(writeExcel(path=PATH_EXCEL, data=data_save))
    
    # Stop in time
    time.sleep(time_delay_steps)                
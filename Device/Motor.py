from pyfirmata import Arduino
from Device.Components import ElectronicComponents
import time
import numpy as np

# Interfaces
class Motor(ElectronicComponents):
    def __init__(self, board: Arduino, name=None):
        super().__init__(board=board, name=name)
        self.history_step_angle = None
        
    def classify(self) -> str: pass
    
# Class
class Model_17HS3401(Motor):
    def __init__(self, 
                 board:Arduino,
                 step_pin:int, 
                 dir_pin:int,
                 div_step=1,
                 pos_dir=0,
                 name=None):
        
        # Env
        super().__init__(board=board, name=name)
        self.dir_pin = board.get_pin(f'd:{dir_pin}:o')
        self.step_pin = board.get_pin(f'd:{step_pin}:o')
        self.div_step = div_step
        self.pos_dir = pos_dir
        
        # Save info step motor
        self.history_step_angle = 0
        self._step_angle_conts = 1.8
        self.step_angle = self._step_angle_conts / div_step
        
        
    def step(self, angle, delay=0.0001, checkStop=None):
        
        # Convert angle, i
        if angle.__class__ is tuple:
            angle, i = angle
        elif angle.__class__ is int:
            i = 1

        # Calc steps of motor with angle and get dir 
        steps = angle / self.step_angle
        direction = None
        sign_steps = np.sign(steps)  
        steps = np.abs(int(steps))
        if sign_steps == True: direction = self.pos_dir
        else: direction = not self.pos_dir 
        
        # Calc angle to check break
        angle_check_stop = self.history_step_angle + self._step_angle_conts * sign_steps
        
        # Create checkPoint show break in steps
        in_progress_break = False
        
        # Set dir motor
        self.dir_pin.write(direction)
        for _ in range(steps):
            
           # Control Motor
            self.step_pin.write(1)
            time.sleep(delay)
            self.step_pin.write(0)
            time.sleep(delay)
            
            # Calc angle future
            temp_angle = self.history_step_angle + self.step_angle * i * sign_steps
            
            # Wait angle to check break
            check_break = False
            if sign_steps == 1 and temp_angle >= angle_check_stop: check_break = True
            if sign_steps == -1 and temp_angle <= angle_check_stop: check_break = True
            
            # Check break
            if check_break:
                if not checkStop is None:
                    if checkStop(angle=temp_angle, sign_steps=sign_steps) == True:
                        in_progress_break = True
                        break
                    angle_check_stop += self._step_angle_conts * sign_steps
                        
            # Save info angle step motor
            self.history_step_angle = temp_angle
            
        return self.history_step_angle, in_progress_break
                          
class Model_MG90S(Motor):
    def __init__(self, board:Arduino, pin:int, name=None):
        super().__init__(board=board, name=name)
        self.servo = board.get_pin(f'd:{pin}:s')
        
        
    def step(self, angle, delay=1):
        self.servo.write(angle)
        time.sleep(delay)
        return angle
             
            

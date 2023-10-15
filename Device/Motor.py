from pyfirmata import Arduino
from Device.Components import ElectronicComponents
import time
import numpy as np

# Interfaces
class Motor(ElectronicComponents):
    def __init__(self, board: Arduino, name=None):
        super().__init__(board=board, name=name)
        self._history_step_angle = None
        
    def classify(self) -> str: pass
    
    def step(self) -> int: pass
    
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
        self._history_step_angle = 0
        self.step_angle = 1.8 / div_step
        
    def step(self, angle, delay=0.0001, checkStop=None):
        
        if angle.__class__ is list:
            angle, i = angle
        elif angle.__class__ is int:
            i = 1

        steps = angle / self.step_angle
        direction = None
        sign_steps = np.sign(steps)  
        steps = np.abs(int(steps))
        if sign_steps == True: direction = self.pos_dir
        else: direction = not self.pos_dir 
        
        check_break = False
        self.dir_pin.write(direction)
        for _ in range(steps):
            
            # Control Motor
            self.step_pin.write(1)
            time.sleep(delay)
            self.step_pin.write(0)
            time.sleep(delay)
            
            # Save info angle step motor
            self._history_step_angle += self.step_angle * i * sign_steps
            
            # Check stop motor
            if not checkStop is None:
                if checkStop(angle=self._history_step_angle, sign_steps=sign_steps) == True:
                    check_break = True
                    break
                
        return self._history_step_angle, check_break
     
    def classify(self):
        return "step"
                         
class Model_MG90S(Motor):
    def __init__(self, board:Arduino, pin:int, name=None):
        super().__init__(board=board, name=name)
        self.servo = board.get_pin(f'd:{pin}:s')
        
        
    def step(self, angle, delay=1):
        self.servo.write(angle)
        time.sleep(delay)
        return angle
        
    def classify(self):
        return "servo"
             
            

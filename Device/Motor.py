from pyfirmata import Arduino
from Device.Components import ElectronicComponents
import time

# Interfaces
class Motor(ElectronicComponents):
    def __init__(self, board: Arduino, name=None):
        super().__init__(board=board, name=name)
        
    def classify(self) -> str: pass
    
    def step(self) -> int: pass
    
# Class
class Model_17HS3401(Motor):
    def __init__(self, 
                 board:Arduino,
                 step_pin:int, 
                 dir_pin:int, 
                 name=None):
        
        # Env
        super().__init__(board=board, name=name)
        self.dir_pin = board.get_pin(f'd:{dir_pin}:o')
        self.step_pin = board.get_pin(f'd:{step_pin}:o')
        
        # Save info step motor
        self._history_step_angle = 0
        self.step_angle = 1.8
        
    def step(self, steps=1, direction=1, delay=0.005, checkStop=None):
        
        if not checkStop is None:
            if checkStop(self._history_step_angle) == True: return self._history_step_angle
            
        self.dir_pin.write(direction)
        for _ in range(steps):
            # Control Motor
            self.step_pin.write(1)
            time.sleep(delay)
            self.step_pin.write(0)
            time.sleep(delay)
            # Save info angle step motor
            if direction:
                self._history_step_angle += self.step_angle 
            else: 
                self._history_step_angle -= self.step_angle
            
            if not checkStop is None:
                if checkStop(self._history_step_angle) == True: break
                
                 
        return self._history_step_angle
     
    def classify(self):
        return "step"
                         
class Model_MG90S(Motor):
    def __init__(self, board:Arduino, pin:int, name=None):
        super().__init__(board=board, name=name)
        self.servo = board.get_pin(f'd:{pin}:s')
        
        
    def step(self, deg, delay=1):
        self.servo.write(deg)
        time.sleep(delay)
        return deg
        
    def classify(self):
        return "servo"
             
            

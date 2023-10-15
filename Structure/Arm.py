import time
from Device.Motor import Motor
from Device.Components import MechanicalComponents
from Device.Gear import SpurGear

# Interfaces
class ArmMechanical(MechanicalComponents):
    def __init__(self, 
                 angle_open=120, 
                 angle_close=0,
                 material=None,
                 name=None):
        super().__init__(name=name, material=material)
        self.angle_open = angle_open
        self.angle_close = angle_close
        
    def open(self): pass
    def close(self): pass
    def pick(self, delay): pass
    def drop(self, delay): pass
        
# Class
class PickDropMechanism_V1(ArmMechanical):
    def __init__(self, 
                 motor: Motor, 
                 z=[1, 2], 
                 angle_limit=[0 , 120], 
                 material=None,
                 name=None):
        
        super().__init__(name=name, material=material)
        self.motor = motor
        # Save angle
        self.gear = SpurGear(z)
        self.angle_limit = [self.gear.calcParameter(angle_limit[0], True)[0], self.gear.calcParameter(angle_limit[1], True)[0]]
        
    def open(self, delay=1):
        self.motor.step(self.angle_open, delay)
        return None
    
    def close(self, delay=1):
        self.motor.step(self.angle_close, delay)
        return None
    
    def pick(self, delay=1):
        self.motor.step(self.angle_open)
        time.sleep(delay)
        self.motor.step(self.angle_close)
        return None
    
    def drop(self, delay=1):
        return self.pick(delay=delay)
    
   
    
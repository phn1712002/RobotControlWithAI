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
                 angle_open=120, 
                 angle_close=0,
                 material=None,
                 name=None):
        
        super().__init__(name=name, material=material)
        self.motor = motor
        if not self.motor.classify == "servo":
            pass
        
        # Save angle
        self.gear = SpurGear(z)
        self.angle_open = self.gear.calcParameter(angle_open)
        self.angle_close = self.gear.calcParameter(angle_close)
    
        # Reset motor
        self.close()
    
    def open(self):
        self.motor.step(self.angle_open)
        return self
    
    def close(self):
        self.motor.step(self.angle_close)
        return self
    
    def pick(self, delay=1):
        self.motor.step(self.angle_open)
        time.sleep(delay)
        self.motor.step(self.angle_close)
        return self
    
    def drop(self, delay=1):
        return self.pick(delay=delay)
    
   
    
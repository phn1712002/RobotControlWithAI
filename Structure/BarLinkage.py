import numpy as np
from Device.Motor import Motor
from Device.Switch import Switch
from Device.Components import MechanicalComponents

# Interfaces
class BarLinkage(MechanicalComponents):
    def __init__(self, geometric_size, name=None, material=None):
        super().__init__(name, material)
        self.geometric_size = geometric_size

# Classo
class FourBarLinkage(BarLinkage):
    def __init__(self, 
                 motor:Motor, 
                 limit_swith: Switch,
                 geometric_size={40, 20, 40, 30},
                 pos_dir=0,
                 material=None,
                 name=None,
                 ):
        super().__init__(geometric_size, name=name, material=material)
        self.motor = motor 
        self.limit_swith = limit_swith
        self.pos_dir = pos_dir
        self.status_break = None
        
    def step(self, angle=1, delay=0.0001, checkStop=None):
        
        def checkStop_fn(self, sign_steps):
            check = self.limit_swith.checkClick()
            if check: 
                if self.status_break != sign_steps:
                    self.status_break = sign_steps
                    check = False
            return check
        
        if checkStop is None: return self.motor.step(angle=angle, delay=delay, checkStop=lambda _, sign_steps: checkStop_fn(self, sign_steps))        
        else: return self.motor.step(angle=angle, delay=delay, checkStop=checkStop)         

            
        
    
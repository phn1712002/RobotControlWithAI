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
                 geometric_size={40, 20, 40, 30},
                 limit_swith=[None, None],
                 limit_angle=[-np.Inf, np.Inf],
                 material=None,
                 name=None,
                 ):
        super().__init__(geometric_size, name=name, material=material)
        self.motor = motor 
        self.limit_swith = limit_swith
        self.limit_angle = limit_angle
        
    def step(self, steps=1, direction=1, delay=0.005):
        
        def checkStop(self, angle):
            check = False
            if not self.limit_swith[0] is None:
                if self.limit_swith[0].checkClick() == True: check = True
            if not self.limit_swith[1] is None:
                if self.limit_swith[1].checkClick() == True: check = True 
            if angle < self.limit_angle[0] or angle > self.limit_angle[1]:
                check = True
                
            return check
            
        self.motor.step(steps=steps, direction=direction, delay=delay, checkStop=lambda angle: checkStop(self, angle))
    

            
        
    
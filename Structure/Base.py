from Device.Components import MechanicalComponents
from Device.Motor import Motor
from Device.Gear import SpurGear

class Base_V1(MechanicalComponents):
    def __init__(self, 
                 motor: Motor, 
                 z=[1, 2], 
                 angle_limit=[-60, 60],
                 material=None,
                 name=None):
        super().__init__(name=name, material=material)
        self.motor = motor
        self.gear = SpurGear(z=z)
        self.angle_limit = [self.gear.calcParameter(angle_limit[0], True)[0], self.gear.calcParameter(angle_limit[1], True)[0]]
        
    def step(self, angle, delay, checkStop=None):
        def checkStop_fn(self, angle, sign_steps):
            check = angle < self.angle_limit[0] or angle > self.angle_limit[1]
            if check: 
                if self.status_break != sign_steps:
                    self.status_break = sign_steps
                    check = False
            return check
        
        if checkStop is None: return self.motor.step(angle=self.gear.calcParameter(input=angle, inverse=False), delay=delay, checkStop=lambda angle, sign_steps: checkStop_fn(self, angle, sign_steps))        
        else: return self.motor.step(angle=self.gear.calcParameter(input=angle, inverse=False), delay=delay, checkStop=checkStop)        
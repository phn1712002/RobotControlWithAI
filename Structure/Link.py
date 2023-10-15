
from Structure.BarLinkage import FourBarLinkage
from Device.Motor import Motor
from Device.Gear import SpurGear
from Device.Components import MechanicalComponents
from Device.Switch import Switch

class Link_V1(MechanicalComponents):
    def __init__(self, 
                 motor: Motor, 
                 limit_switch: Switch,
                 z=[1, 2],
                 delay_motor=0.0001,
                 name=None,
                 ):
        super().__init__(name=name)
        self.motor = motor
        self.gear = SpurGear(z=z)
        self.link = FourBarLinkage(motor=motor, limit_swith=limit_switch)
        self.delay_motor = delay_motor
        
    def step(self, angle):
        return self.link.step(angle=self.gear.calcParameter(input=angle, inverse=True), delay=self.delay_motor)
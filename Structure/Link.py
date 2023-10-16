from Device.Components import MechanicalComponents
from Device.Motor import Motor
from Device.Switch import Switch
from Device.Gear import SpurGear

# Class
class Link_V1(MechanicalComponents):
    def __init__(self, 
                 motor:Motor, 
                 limit_switch: Switch,
                 z=[1, 2],
                 delay_motor=0.0001,
                 name=None,
                 ):
        super().__init__(name=name)
        self.motor = motor 
        self.limit_switch = limit_switch
        self.gear = SpurGear(z=z)
        self.delay_motor = delay_motor
        self.status_break = {
            'sign_steps_break': None,
            'wait_break_current': False
        }
        
    def step(self, angle=0):
        
        
        def checkStop_fn(self, sign_steps):
            """ Function callbacks using in steps with task checkStop (stop motor when got stuck)
            Args:
                self (Link_V1): Self Structure
                sign_steps (int, [-1, 1]): Dir of motor

            Returns:
                bool: True - Break, False - No Break
            """
            
            # Get status all switch 
            check = 0
            for index in self.limit_switch:
                check += index.checkClick()
            check = bool(check) # Convert to bool 
            
            # Checking break
            if check:
                # Direction change exists
                if self.status_break['sign_steps_break'] != sign_steps:
                    # Check break firts time
                    if self.status_break['sign_steps_break'] is None: 
                        self.status_break['sign_steps_break'] = sign_steps
                        return False
                    else:
                        # Setup status wait break current
                        self.status_break['wait_break_current'] = True
                        return False
            # Check status wait break current -> success -> change 
            if not check and self.status_break['wait_break_current']:
                self.status_break['wait_break_current'] = False
                self.status_break['sign_steps_break'] = sign_steps
            return check
        
        # Control motor step
        return self.motor.step(angle=self.gear.calcParameter(input=angle,inverse=True), 
                               delay=self.delay_motor, 
                               checkStop=lambda angle, sign_steps: checkStop_fn(self, sign_steps)
                               )        
          
    def resetAngle(self):
        def checkStop_fn(self):
            check = True
            return check

        if self.motor.step(angle=-99999, delay=self.delay_motor, checkStop=lambda angle, sign_steps: checkStop_fn(self))[1]:
            self.motor._history_step_angle = 0
            return True
        else: return False
            
        
    
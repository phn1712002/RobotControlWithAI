from Device.Components import MechanicalComponents
from Device.Motor import Motor
from Device.Gear import SpurGear

# Class
class Base_V1(MechanicalComponents):
    def __init__(self, 
                 motor: Motor, 
                 z=[1, 2], 
                 angle_dir_def = 30,
                 angle_limit=[-60, 60],
                 delay_motor=0.0001,
                 name=None):
        super().__init__(name=name)
        self.motor = motor
        self.gear = SpurGear(z=z)
        self.angle_limit = angle_limit
        self.angle_dir_def = angle_dir_def
        self.delay_motor = delay_motor
        self.status_break = {
            'sign_steps_break': None,
            'wait_break_current': False
        }
        
    def step(self, angle):
        def checkStop_fn(self, angle, sign_steps):
            """ Function callbacks using in steps with task checkStop (stop motor when got stuck)
                Like fucntion checkStop_fn in Link.py
                Just different checkStop with angle, no switch limit
    
            Args:
                self (Link_V1): Self Structure
                sign_steps (int, [-1, 1]): Dir of motor
                angle (float) : angle current of Structure

            Returns:
                bool: True - Break, False - No Break
            """
            # Check angle
            check = angle < self.angle_limit[0] or angle > self.angle_limit[1] # Diffenrent Link.py
            
            # Like fucntion checkStop_fn in Link.py
            if check: 
                if self.status_break['sign_steps_break'] != sign_steps:
                    if self.status_break['sign_steps_break'] is None: 
                        self.status_break['sign_steps_break'] = sign_steps
                        return True
                    else:
                        self.status_break['wait_break_current'] = True
                        return True
            if not check and self.status_break['wait_break_current']:
                self.status_break['wait_break_current'] = False
                self.status_break['sign_steps_break'] = sign_steps
            return check
        
        # Control motor step
        return self.motor.step(angle=self.gear.calcParameter(input=angle, inverse=True), delay=self.delay_motor, checkStop=lambda angle, sign_steps: checkStop_fn(self, angle, sign_steps))        
    
    def resetAngle(self):
        def checkStop_fn(self):
            check = True
            return check
    
        if self.motor.step(angle=-99999, delay=self.delay_motor, checkStop=lambda angle, sign_steps: checkStop_fn(self))[1]:
            self.motor.history_step_angle = 0
            return True
        else: return False
        
    def getAngle(self):
        return self.motor.history_step_angle
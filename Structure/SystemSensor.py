from pyfirmata import Arduino
from Device.Switch import Switch, Model_2A, Model_2A_Analog
from Device.Components import ElectronicComponents

class SystemSensor(ElectronicComponents):
    def __init__(self, name=None, board=None, pin=0):
        super().__init__(name, board, pin)
    def checkStop(self, check_right: bool, sign_steps: int): pass
    
class MultiSwitch_V1(SystemSensor):
    def __init__(self, board: Arduino, config_switch_right: Switch, config_switch_left: Switch, config_switch_2mid: Switch, name=None):
        super().__init__(name, board, None)
        self.board = board
        self.config_switch_right = config_switch_right
        self.config_switch_left = config_switch_left
        self.config_switch_mid = config_switch_2mid
         
        self.switch_right = Model_2A(board=board, **self.config_switch_right)
        self.switch_left = Model_2A(board=board, **self.config_switch_left)
        self.switch_mid = Model_2A_Analog(board=board, **self.config_switch_mid)
        
        self.sign_steps_break_right = None
        self.wait_break_current_right = False
        
        self.sign_steps_break_left = None
        self.wait_break_current_left = False
        
    def checkStop(self, check_right: bool, sign_steps: int):
            """ Function callbacks using in steps with task checkStop (stop motor when got stuck)
            Args:
                check_right: True - Check motor right, False - Check motor left
                sign_steps (int, [-1, 1]): Dir of motor

            Returns:
                bool: True - Break, False - No Break
            """
            
            # Check switch mid 2 motor
            check_mid = self.switch_mid.checkClick()
            
            # Check switch right/left
            if check_right: check = bool(self.switch_right.checkClick() + check_mid)
            else: check = bool(self.switch_left.checkClick() + check_mid)
            
            # Check stop
            if check:
                # Using paramter of motor right or left ?
                if check_right:
                    # Direction change exists
                    if self.sign_steps_break_right != sign_steps:
                        # Check break firts time
                        if self.sign_steps_break_right is None: 
                            self.sign_steps_break_right = sign_steps
                            # Change status sign break, uses no 2 motor steps reverse dir -> no got stuck in structure 
                            if check_mid: 
                                self.sign_steps_break_left = self.sign_steps_break_right * -1
                            return True
                        else:
                            # Setup status wait break current
                            self.wait_break_current_right = True
                            return False
                else:
                    if self.sign_steps_break_left != sign_steps:
                        if self.sign_steps_break_left is None: 
                            self.sign_steps_break_left = sign_steps
                            if check_mid: 
                                self.sign_steps_break_right = self.sign_steps_break_left * -1
                            return True
                        else:
                            self.wait_break_current_left = True
                            return False
                        
            # Check status wait break current -> success -> change 
            if not check and self.wait_break_current_right:
                self.wait_break_current_right = False
                self.sign_steps_break_right = sign_steps
                        
            if not check and self.wait_break_current_left:
                self.wait_break_current_left = False
                self.sign_steps_break_left = sign_steps
                    
            return check
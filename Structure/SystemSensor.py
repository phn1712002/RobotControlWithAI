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
        self.config_switch_2mid = config_switch_2mid
         
        self.switch_right = Model_2A(board=board, **self.config_switch_right)
        self.switch_left = Model_2A(board=board, **self.config_switch_left)
        self.switch_mid = Model_2A_Analog(board=board, **self.config_switch_2mid)
        
        self.sign_steps_break_right = None
        self.sign_steps_break_left = None
        
        self.wait_break_current = False
        
        self.sign_change_2motor = False
        self.last_sign_change_2motor = 0
        
        self.history_motor_control = None
        self.change_motor_control = False
        
        
    def checkStop(self, check_right: bool, sign_steps: int):
            """ Function callbacks using in steps with task checkStop (stop motor when got stuck)
            Args:
                check_right: True - Check motor right, False - Check motor left
                sign_steps (int, [-1, 1]): Dir of motor

            Returns:
                bool: True - Break, False - No Break
            """
            print(f"{check_right} - {self.switch_left.checkClick()} - {self.switch_right.checkClick()} - {self.switch_mid.checkClick()} - {self.sign_steps_break_left} - {self.sign_steps_break_right}")


            check_mid = self.switch_mid.checkClick()
            if check_right: check = bool(self.switch_right.checkClick() + check_mid)
            else: check = bool(self.switch_left.checkClick() + check_mid)
            
            if self.history_motor_control is None: self.history_motor_control = check_right
            elif self.history_motor_control != check_right:
                self.history_motor_control = check_right
                self.change_motor_control = True
            else: self.change_motor_control = False
            
            if self.sign_change_2motor and not self.change_motor_control:
                if check_right: self.sign_steps_break_left = self.last_sign_change_2motor
                else: self.sign_steps_break_right = self.last_sign_change_2motor
                self.sign_change_2motor = False
            
            if check_right:
                if not self.wait_break_current:
                    if check:
                        if self.sign_steps_break_right != sign_steps:
                            if self.sign_steps_break_right is None:
                                self.sign_steps_break_right = sign_steps
                                if check_mid:
                                    self.last_sign_change_2motor = self.sign_steps_break_left
                                    self.sign_steps_break_left = -self.sign_steps_break_right
                                    self.sign_change_2motor = True
                                return True
                            else:
                                self.sign_steps_break_right = None
                                self.wait_break_current = True
                                return False
                        else: 
                            self.sign_steps_break_right = sign_steps
                            if check_mid:
                                self.last_sign_change_2motor = self.sign_steps_break_left
                                self.sign_steps_break_left = -self.sign_steps_break_right
                                self.sign_change_2motor = True
                            return True
                    else: return False
                else:
                    if not check: self.wait_break_current = False
                    return False
            else: 
                if not self.wait_break_current:
                    if check:
                        if self.sign_steps_break_left != sign_steps:
                            if self.sign_steps_break_left is None:
                                self.sign_steps_break_left = sign_steps
                                if check_mid:
                                    self.last_sign_change_2motor = self.sign_steps_break_right
                                    self.sign_steps_break_right = -self.sign_steps_break_left
                                    self.sign_change_2motor = True
                                return True
                            else:
                                self.sign_steps_break_left = None
                                self.wait_break_current = True
                                return False
                        else: 
                            self.sign_steps_break_left = sign_steps
                            if check_mid:
                                self.last_sign_change_2motor = self.sign_steps_break_right
                                self.sign_steps_break_right = -self.sign_steps_break_left
                                self.sign_change_2motor = True
                            return True
                    else: return False
                else:
                    if not check: self.wait_break_current = False
                    return False
            
            
            """
            if self.history_motor_control is None: self.history_motor_control = check_right
            elif self.history_motor_control != check_right:
                self.history_motor_control = check_right
                self.change_motor_control = True
            
            

            # Check switch mid 2 motor
            check_mid = self.switch_mid.checkClick()
            
            # Check switch right/left
            if check_right: check = bool(self.switch_right.checkClick() + check_mid)
            else: check = bool(self.switch_left.checkClick() + check_mid)
            
            
            # Check sto
            if check and not self.wait_break_current_left and not self.wait_break_current_right:
                # Using paramter of motor right or left ?
                if check_right:
                    # Direction change exists
                    if self.sign_steps_break_right != sign_steps:
                        # Check break firts time
                        if self.sign_steps_break_right is None: 
                            self.sign_steps_break_right = sign_steps
                            # Change status sign break, uses no 2 motor steps reverse dir -> no got stuck in structure 
                            if check_mid:
                                self.last_sign_change_2motor_left = self.sign_steps_break_left
                                self.sign_steps_break_left = self.sign_steps_break_right * -1
                                self.sign_change_2motor = True
                            return True
                        else:
                            # Setup status wait break current
                            self.wait_break_current_right = True
                            return False
                    else:
                        if check_mid: 
                            self.last_sign_change_2motor_left = self.sign_steps_break_left
                            self.sign_steps_break_left = self.sign_steps_break_right * -1
                            self.sign_change_2motor = True
                        return True 
                else:
                    if self.sign_steps_break_left != sign_steps:
                        if self.sign_steps_break_left is None: 
                            self.sign_steps_break_left = sign_steps
                            self.sign_change_2motor_first = True
                            if check_mid: 
                                self.last_sign_change_2motor_right = self.sign_steps_break_right
                                self.sign_steps_break_right = self.sign_steps_break_left * -1
                                self.sign_change_2motor = True
                            return True
                        else:
                            self.wait_break_current_left = True
                            return False
                    else:
                        if check_mid: 
                            self.last_sign_change_2motor_right = self.sign_steps_break_right
                            self.sign_steps_break_right = self.sign_steps_break_left * -1
                            self.sign_change_2motor = True
                        return True
                        
            # Check status wait break current -> success -> change
            if self.wait_break_current_right or self.wait_break_current_left:
                if not check and self.wait_break_current_right:
                    self.wait_break_current_right = False
                    self.sign_steps_break_right = sign_steps
                    if self.sign_change_2motor and not self.change_motor_control:
                        self.sign_steps_break_left = self.last_sign_change_2motor_left
                        self.sign_change_2motor = False
                        self.change_motor_control = False    
                         
                if not check and self.wait_break_current_left:
                    self.wait_break_current_left = False
                    self.sign_steps_break_left = sign_steps
                    if self.sign_change_2motor and not self.change_motor_control: 
                        self.sign_steps_break_right = self.last_sign_change_2motor_right
                        self.sign_change_2motor = False
                        self.change_motor_control = False
                return False
            else:
                if check_right: self.sign_steps_break_right = sign_steps
                else: self.sign_steps_break_left = sign_steps

            return 
            """
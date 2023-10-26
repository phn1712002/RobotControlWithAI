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
        
        self.limit_left = [None, None]
        self.limit_right = [None, None]
        
        self.wait_break_current = False
        
        self.sign_change_2motor = False
        self.last_sign_change_2motor = [0,0]
        
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
            #print(f"{check_right} - {self.switch_left.checkClick()} - {self.switch_right.checkClick()} - {self.switch_mid.checkClick()} - {self.sign_steps_break_left} - {self.sign_steps_break_right}")


            check_mid = self.switch_mid.checkClick()
            if check_right: check = bool(self.switch_right.checkClick() + check_mid)
            else: check = bool(self.switch_left.checkClick() + check_mid)
            
            if self.history_motor_control is None: self.history_motor_control = check_right
            elif self.history_motor_control != check_right:
                self.history_motor_control = check_right
                self.change_motor_control = True
            else: self.change_motor_control = False
            
            if self.sign_change_2motor and not self.change_motor_control:
                if check_right: self.limit_left[self.last_sign_change_2motor[0]] = self.last_sign_change_2motor[1]
                else: self.limit_right[self.last_sign_change_2motor[0]] = self.last_sign_change_2motor[1]
                self.sign_change_2motor = False
            
            
            if self.wait_break_current:
                if not check: 
                    self.wait_break_current = False
                    index_check_reverse = int(max(-sign_steps, 0))
                    if check_right: self.limit_right[index_check_reverse] = None
                    else: self.limit_left[index_check_reverse] = None
                return False
            
            if check_right:
                if check:
                    index_check = int(max(sign_steps, 0))
                    index_check_reverse = int(max(-sign_steps, 0))
                
                    if sign_steps in self.limit_right: 
                        if check_mid:
                            self.last_sign_change_2motor = [index_check_reverse, self.limit_left[index_check_reverse]]
                            self.sign_change_2motor = True
                            self.limit_left[index_check_reverse] = -sign_steps
                        return True
                    else:
                            if -sign_steps in self.limit_right:
                                self.wait_break_current = True
                                return False
                            else:
                                self.limit_right[index_check] = sign_steps
                                if check_mid:
                                    self.last_sign_change_2motor = [index_check_reverse, self.limit_left[index_check_reverse]]
                                    self.sign_change_2motor = True
                                    self.limit_left[index_check_reverse] = -sign_steps
                                return True  
                else: return False
            else:
                if check:
                    index_check = int(max(sign_steps, 0))
                    index_check_reverse = int(max(-sign_steps, 0))
                
                    if sign_steps in self.limit_left: 
                        if check_mid:
                            self.last_sign_change_2motor = [index_check_reverse, self.limit_right[index_check_reverse]]
                            self.sign_change_2motor = True
                            self.limit_right[index_check_reverse] = -sign_steps
                        return True
                    else:
                            if -sign_steps in self.limit_left:
                                self.wait_break_current = True
                                return False
                            else:
                                self.limit_left[index_check] = sign_steps
                                if check_mid:
                                    self.last_sign_change_2motor = [index_check_reverse, self.limit_right[index_check_reverse]]
                                    self.sign_change_2motor = True
                                    self.limit_right[index_check_reverse] = -sign_steps
                                return True  
                else: return False
            
            
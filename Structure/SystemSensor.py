from pyfirmata import Arduino
from Device.Switch import Switch, Model_2A, Model_2A_Analog
from Device.Components import ElectronicComponents
from Tools.Delay import delayMicroseconds, delaySeconds

class SystemSensor(ElectronicComponents):
    def __init__(self, name=None, board=None, pin=0):
        super().__init__(name, board, pin)
    def checkStop(self, check_right: bool, sign_steps: int, exit=False): pass
    
class MultiSwitch_V1(SystemSensor):
    def __init__(self, board: Arduino, 
                 config_switch_right: Switch, 
                 config_switch_left: Switch, 
                 config_switch_2mid: Switch, 
                 time_delay_break_out = 0.5,
                 name=None):
        super().__init__(name, board, None)
        self.board = board
        self.config_switch_right = config_switch_right
        self.config_switch_left = config_switch_left
        self.config_switch_2mid = config_switch_2mid
         
        self.switch_right = Model_2A(board=board, **self.config_switch_right)
        self.switch_left = Model_2A(board=board, **self.config_switch_left)
        self.switch_mid = Model_2A_Analog(board=board, **self.config_switch_2mid)
        

        
        self.limit_left = [None, 1]
        self.limit_right = [None, 1]
        
        self.wait_break_out = False
        self.last_change_2motor = [None, None]
        self.change_2motor = False
        
        self.time_delay_break_out = time_delay_break_out
        
        
    def checkStop(self, check_right: bool, sign_steps: int, exit=False):
            """ Function callbacks using in steps with task checkStop (stop motor when got stuck)
            Args:
                check_right: True - Check motor right, False - Check motor left
                sign_steps (int, [-1, 1]): Dir of motor

            Returns:
                bool: True - Break, False - No Break
            """
            if not exit: 
                #
                check_m = self.switch_mid.checkClick() 
                check_r = self.switch_right.checkClick()
                check_l = self.switch_left.checkClick()
                
                #
                index_check = int(max(sign_steps, 0))
                index_check_rev = int(max(-sign_steps, 0))
                
                #
                if check_right: check = bool(check_m + check_r)
                else: check = bool(check_m + check_l)
                
                #
                if self.wait_break_out:
                    if not check:
                        delaySeconds(self.time_delay_break_out)
                        self.wait_break_out = False
                        if check_right: 
                            self.limit_right[index_check_rev] = None
                            if self.change_2motor: 
                                if check_l: self.limit_left[self.last_change_2motor[0]] = self.last_change_2motor[1]
                                else: self.limit_left[index_check] = None
                                self.change_2motor = False
                        else: 
                            self.limit_left[index_check_rev] = None
                            if self.change_2motor: 
                                if check_r: self.limit_right[self.last_change_2motor[0]] = self.last_change_2motor[1]
                                else: self.limit_right[index_check] = None
                                self.change_2motor = False
                    return False
                #
                if check_right:
                    if sign_steps in self.limit_right: 
                        return True
                    elif -sign_steps in self.limit_right:
                        self.wait_break_out = True
                        return False
                else: 
                    if sign_steps in self.limit_left: 
                        return True
                    elif -sign_steps in self.limit_left:
                        self.wait_break_out = True
                        return False
                
                #
                if check and not self.wait_break_out:
                    if check_right: 
                        self.limit_right[index_check] = sign_steps
                        if check_m:
                            self.change_2motor = True
                            self.last_change_2motor = [index_check_rev, self.limit_left[index_check_rev]]
                            self.limit_left[index_check_rev] = -sign_steps
                    else: 
                        self.limit_left[index_check] = sign_steps
                        if check_m:
                            self.change_2motor = True
                            self.last_change_2motor = [index_check_rev, self.limit_right[index_check_rev]]
                            self.limit_right[index_check_rev] = -sign_steps
                    return True
                else: self.wait_break_out = False
                    
            
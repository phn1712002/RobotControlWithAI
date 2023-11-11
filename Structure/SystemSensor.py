import os
from pyfirmata import Arduino
from Device.Switch import Switch, Model_2A, Model_2A_Analog
from Device.Components import ElectronicComponents
from Tools.Delay import delayMicroseconds, delaySeconds

class SystemSensor(ElectronicComponents):
    def __init__(self, name=None, board=None, pin=0):
        super().__init__(name, board, pin)
        
    def checkStop(self, check_right: bool, sign_steps: int, exit=False):
        """
        Function callbacks using in steps with task checkStop (stop motor when got stuck)
        Args:
            check_right: True - Check motor right, False - Check motor left
            sign_steps (int, [-1, 1]): Dir of motor
            exit: Not used

        Returns:
            bool: True - Break, False - No Break
        """
        return False
    
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

        self.limit_left = [None, 1.0]
        self.limit_right = [None, 1.0]
        
        self.wait_break_out = False
        self.last_change_2motor = {
            'index':None, 
            'value':None
            } 
        
        self.change_2motor = False
        
        self.time_delay_break_out = time_delay_break_out
    
    def checkStop(self, check_right=True, sign_steps=1, exit=False):
            """
            Function to check if the motor should stop when it gets stuck.

            Args:
                check_right (bool): True - Check motor right, False - Check motor left
                sign_steps (int, [-1, 1]): Dir of motor
                exit (bool): True - Exit the function, False - Continue the function

            Returns:
                bool: True - Break, False - No Break
            """
    
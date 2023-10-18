from pyfirmata import Arduino
from .Components import ElectronicComponents

# Interfaces
class Switch(ElectronicComponents):
    def __init__(self, board: Arduino, pin: int, name=None):
        super().__init__(board=board, pin=pin, name=name)

    def checkClick(self): pass
# Class
class Model_2A(Switch):
    def __init__(self, 
                 board:Arduino, 
                 pin:int, 
                 inverse_message=False,
                 name=None):
        
        super().__init__(board=board, pin=pin, name=name)
        self.button = board.get_pin(f'd:{self.pin}:i')
        self.inverse_message = inverse_message
    
    def checkClick(self):
        """
            Check switch is pressed ?
        Returns:
            bool: True - switch is pressed and False - no is pressed
        """
        if self.inverse_message: 
            return not self.button.read()
        else:
            return self.button.read()
        
class Model_2A_Analog(Switch):
    """
        Like class Model_2A just different com of board using analog no digital  
    """
    def __init__(self, board: Arduino, pin: int, inverse_message=False, name=None):
        super().__init__(board, pin, name)
        self.button = board.get_pin(f'a:{self.pin}:i')
        self.inverse_message = inverse_message
        
    def checkClick(self):
        if self.inverse_message: 
            return not bool(self.button.read())
        else:
            return bool(self.button.read())
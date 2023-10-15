from pyfirmata import Arduino
from Device.Components import ElectronicComponents

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
    
    def checkClick(self, delay=0.0001):
        if self.inverse_message: 
            return not self.button.read()
        else:
            return self.button.read()
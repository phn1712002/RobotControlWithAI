import pyfirmata
from Tools.Json import loadJson, saveJson
from pyfirmata import Arduino
from Device.Motor import Model_17HS3401, Model_MG90S
from Device.Switch import Model_2A
from Device.Gear import SpurGear
from Structure.Arm import PickDropMechanism_V1
from Structure.Base import Base_V1
from Structure.BarLinkage import FourBarLinkage
from Device.Peripherals import Camera, Micro

class Robot_V1:
    def __init__(self, config_or_path):
        if config_or_path.__class__ is str:
            self.config = loadJson(config_or_path)
        else:
            self.config = config_or_path 
            
        ###  Get all config for device ### 
        self.config_board = self.config['board']
        self.config_cam = self.config['camera']
        self.config_mic = self.config['mic']
        
        self.config_ena_motor = self.config['ena_motor']
        self.config_delay_motorST = self.config['delay_motorST']
        
        self.config_motor_mid = self.config['motor_mid']
        self.config_link_base = self.config['link_base']
        
        self.config_motor_left = self.config['motor_left']
        self.config_switch_left = self.config['switch_left']
        self.config_link_1 = self.config['link_1']
        
        self.config_motor_right = self.config['motor_right']
        self.config_switch_right = self.config['switch_right']
        self.config_link_2 = self.config['link_2']
        
        self.config_motor_arm = self.config['motor_arm'] 
        self.config_link_arm = self.config['link_arm']
        
        # Config board
        self.board = Arduino(self.config_board)
        pyfirmata.util.Iterator(self.board).start()

        # Enable motor stepper in CNC V3
        self.ena_motor_pin = self.config_ena_motor['pin']
        self.ena_pin = self.board.get_pin(f'd:{self.ena_motor_pin}:o')
        self.ena_pin.write(self.config_ena_motor['input'])

        # Config switch and motor right
        self.switch_right = Model_2A(board=self.board, **self.config_switch_right)
        self.motor_right = Model_17HS3401(board=self.board, **self.config_motor_right)

        # Config switch and motor left
        self.switch_left = Model_2A(board=self.board, **self.config_switch_left)
        self.motor_left = Model_17HS3401(board=self.board, **self.config_motor_left)
        
        # Config switch and motor left
        self.motor_mid = Model_17HS3401(board=self.board, **self.config_motor_mid)

        # Config motor arm
        self.motor_arm = Model_MG90S(board=self.board, **self.config_motor_arm)
        
        ### Config structure robot ###
        # Camera
        self.cam = Camera(**self.config_cam)
        
        # Micro
        self.mic = Micro(**self.config_mic)
        
        # Link_base
        self.link_base = Base_V1(motor=self.motor_mid, **self.config_link_base)
        
        # Link_1
        self.link_1 = FourBarLinkage(motor=self.motor_left, limit_swith=self.switch_left)
        self.gear_link_1 = SpurGear(**self.config_link_1)
        
        # Link_2
        self.link_2 = FourBarLinkage(motor=self.motor_right, limit_swith=self.switch_right)
        self.gear_link_2 = SpurGear(**self.config_link_2)
        
        # Link_arm
        self.link_arm = PickDropMechanism_V1(motor=self.motor_arm, **self.config_link_arm)
        
        
    def controlOneLink(self, index, angle_or_oc):
        if index == 0:
            output = self.link_base.step(angle=angle_or_oc, delay=self.config_delay_motorST)
        elif index == 1:
            output = self.link_1.step(angle=self.gear_link_1.calcParameter(input=angle_or_oc, inverse=True), delay=self.config_delay_motorST)
        elif index == 2:
            output = self.link_2.step(angle=self.gear_link_2.calcParameter(input=angle_or_oc, inverse=True), delay=self.config_delay_motorST)
        elif index == 3:
            if angle_or_oc: output = self.link_arm.open(delay=1)
            else: output = self.link_arm.close(delay=0.5)
        return output

    def controlThreeLink(self, angle:tuple):
        output_link_base = self.link_base.step(angle=angle[0], delay=self.config_delay_motorST)
        output_link1 = self.link_1.step(angle=self.gear_link_1.calcParameter(input=angle[1], inverse=True), delay=self.config_delay_motorST)
        output_link2 = self.link_2.step(angle=self.gear_link_2.calcParameter(input=angle[2], inverse=True), delay=self.config_delay_motorST)
        return output_link_base, output_link1, output_link2

    def resetAngleLink(self):
        def checkStop_linkbase_fn(base: Base_V1): pass
        def checkStop_linkN_fn(link: FourBarLinkage):
            check = link.limit_swith.checkClick()
            if check: link.motor._history_step_angle = 0
            return check 
        
        self.link_base.step(angle=-999999, delay=self.config_delay_motorST, checkStop=lambda _: checkStop_linkbase_fn(self.link_base))
        self.link_1.step(angle=-999999, delay=self.config_delay_motorST, checkStop=lambda _: checkStop_linkN_fn(self.link_1)) 
        self.link_2.step(angle=-999999, delay=self.config_delay_motorST, checkStop=lambda _: checkStop_linkN_fn(self.link_2))
        self.link_arm.close()
    
    def getFrameInCam(self): return self.cam.getFrame()
    def getFrameInMic(self): return self.mic.getFrame()  
    def viewCam(self): return self.cam.liveView()
    def viewMic(self): return self.mic.playFrame()
    
    def getConfig(self, path=None):
        if not path is None: return saveJson(path=path, data=self.config)
        return self.config
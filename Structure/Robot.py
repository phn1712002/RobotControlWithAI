import pyfirmata
from Tools.Json import loadJson, saveJson
from pyfirmata import Arduino
from Device.Motor import Model_17HS3401, Model_MG90S
from Device.Switch import Model_2A, Model_2A_Analog
from Structure.Arm import PickDropMechanism_V1
from Structure.Base import Base_V1
from Structure.Link import Link_V1
from Structure.SystemSensor import MultiSwitch_V1
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
        
        self.config_motor_mid = self.config['motor_mid']
        self.config_link_base = self.config['link_base']
        
        self.config_switch_a_2motor = self.config['switch_a_2motor']
        
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

        # Config mutil switch 
        self.multi_switch = MultiSwitch_V1(board=self.board, 
                                           config_switch_right=self.config_switch_right,
                                           config_switch_left=self.config_switch_left,
                                           config_switch_2mid=self.config_switch_a_2motor)
        
        # Config motor right
        self.motor_right = Model_17HS3401(board=self.board, **self.config_motor_right)

        # Config smotor left
        self.motor_left = Model_17HS3401(board=self.board, **self.config_motor_left)
        
        # Config motor mid
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
        self.link_1 = Link_V1(motor=self.motor_left, system_sensor=self.multi_switch, **self.config_link_1, right=False)
        
        # Link_2
        self.link_2 = Link_V1(motor=self.motor_right, system_sensor=self.multi_switch, **self.config_link_2, right=True)

        # Link_arm
        self.link_arm = PickDropMechanism_V1(motor=self.motor_arm, **self.config_link_arm)
        
        
    def controlOneLink(self, index_link, angle_or_oc):
        if index_link == 0:
            output = self.link_base.step(angle=angle_or_oc)
        elif index_link == 1:
            output = self.link_1.step(angle=angle_or_oc)
        elif index_link == 2:
            output = self.link_2.step(angle=angle_or_oc)
        elif index_link == 3:
            if angle_or_oc: output = self.link_arm.open()
            else: output = self.link_arm.close()
        return output

    def getAngleOneLink(self, index_link):
        if index_link == 0:
            angle = self.link_base.getAngle()
        elif index_link == 1:
            angle = self.link_base.getAngle()
        elif index_link == 2:
            angle = self.link_base.getAngle()
        return angle 
    
    def getAngleThreeLink(self):
        return self.link_base.getAngle(), self.link_1.getAngle(), self.link_2.getAngle()  
    
    def controlThreeLink(self, angle:tuple):
        output_link_base = self.link_base.step(angle=angle[0])
        output_link1 = self.link_1.step(angle=angle[1])
        output_link2 = self.link_2.step(angle[2])
        return output_link_base, output_link1, output_link2

    
    def resetAngleLink(self): 
        self.link_base.resetAngle()
        self.link_1.resetAngle()
        self.link_2.resetAngle()
        self.link_arm.close()
        
    def statusSearch(self): pass
    def statusListen(self): pass
    def statusAction(self): pass
    def statusRetraining(self): pass
    
    
    def getFrameInCam(self): return self.cam.getFrame()
    def getFrameInMic(self): return self.mic.getFrame()  
    def viewCam(self): return self.cam.liveView()
    def viewMic(self): return self.mic.playFrame()
    
    def getConfig(self, path=None):
        if not path is None: return saveJson(path=path, data=self.config)
        return self.config
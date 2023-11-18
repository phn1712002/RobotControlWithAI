import pyfirmata, numpy as np, tensorflow as tf, keyboard
from Feature.Data import string_maps
from Tools.Json import loadJson, saveJson
from Feature.Deductive import fixTextVietnamese, checkCommandAccept, getDirAndStrOfNER, getNumberAngleFromText, getDirMotorFromText, getNameObjFromText
from pyfirmata import Arduino
from Device.Motor import Model_17HS3401, Model_MG90S
from .Arm import PickDropMechanism_V1
from .Base import Base_V1
from .Link import Link_V1
from .SystemSensor import MultiSwitch_V1
from Device.Peripherals import Camera, Micro
from ModelAI.WaveUnet.Architecture.Model import WaveUnet_tflite
from ModelAI.Wav2Vec2.Architecture.Model import Wav2Vec2_tflite
from ModelAI.BiLSTM.Architecture.Model import NERBiLSTM_tflite

class  Robot_V1:
    def __init__(self, config_or_path):
        if config_or_path.__class__ is str:
            self.config = loadJson(config_or_path)
        else:
            self.config = config_or_path 
        
        
        ### CONST
        self.ANGLE_MAX_CONTROL = np.Inf
        self.ANGLE_FREEZE = 0 
        self.OBJ_EMPTY = None
        self.INDEX_LINK_BASE = 0
        self.INDEX_LINK_1 = 1
        self.INDEX_LINK_2 = 2 
        self.INDEX_LINK_ARM = 3
        
        ###  Get all config for device ###
        self.config_robot = self.config['robot']
        
        self.config_board = self.config['board']
        self.config_cam = self.config['camera']
        self.config_mic = self.config['mic']
        self.path_model = self.config['path_model']
        
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
        
        self.config_multi_switch = self.config['multi_switch']
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
                                           config_switch_2mid=self.config_switch_a_2motor, **self.config_multi_switch)
        
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
        
        ### Config model AI of Robot ###
        # Model remove noise in audio 
        self.remove_noise_audio = WaveUnet_tflite(path=self.path_model)
        self.automatic_speech_recognition = Wav2Vec2_tflite(path=self.path_model)
        self.named_entity_recognition = NERBiLSTM_tflite(path=self.path_model)

        # Check status start of Robot 
        if not self.checkStatusStart(): raise Exception("Please set the robot state to the starting position")
    
    def checkStatusStart(self):
        if self.multi_switch.switch_right.checkClick() and self.multi_switch.switch_left.checkClick(): return True
        return False
    
    def buildModelAI(self):
        self.remove_noise_audio = self.remove_noise_audio.build()
        self.automatic_speech_recognition = self.automatic_speech_recognition.build()
        self.self.named_entity_recognition = self.named_entity_recognition.build()
        
        
    def controlOneLink(self, index_link, angle_or_oc):
        if index_link == self.INDEX_LINK_BASE:
            output = self.link_base.step(angle=angle_or_oc)
        elif index_link == self.INDEX_LINK_1:
            output = self.link_1.step(angle=angle_or_oc)
        elif index_link == self.INDEX_LINK_2:
            output = self.link_2.step(angle=angle_or_oc)
        elif index_link == self.INDEX_LINK_ARM:
            if angle_or_oc: output = self.link_arm.open()
            else: output = self.link_arm.close()
        return output

    def getAngleOneLink(self, index_link):
        if index_link == 0:
            angle = self.link_base.getAngle()
        elif index_link == 1:
            angle = self.link_1.getAngle()
        elif index_link == 2:
            angle = self.link_2.getAngle()
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

    def statusListen(self, play_audio_recoding=False, key_play_recoding=lambda: keyboard.wait('enter')):
        # Get audio in mic
        speech = np.squeeze(self.mic.getFrame(key_play_recoding=key_play_recoding))
        if play_audio_recoding: self.viewMic(speech)
        
        # Remove noise in audio
        speech = self.remove_noise_audio.predict(speech)
        if play_audio_recoding: self.viewMic(speech)

         
        # Automatic Speech Recognition
        text_command = self.automatic_speech_recognition.predict(speech)
        
        # Fix text 
        text_command = fixTextVietnamese(text_command)
        
        # Named entity
        named_entity = self.named_entity_recognition.predict(text_command)
        
        # Format output named entity
        text_array, named_entity_array = getDirAndStrOfNER(named_entity)
        
        # Check Command Accept
        accept = checkCommandAccept(string_maps['space'].join(named_entity_array))
    
        #
        if accept:
            number_angle = self.ANGLE_FREEZE
            # Add dir in number
            dir_action = getDirMotorFromText(text_array, named_entity_array)
            if not dir_action is None:
                # Text to number
                number_angle = getNumberAngleFromText(text_array, named_entity_array)
                if number_angle is None : number_angle = self.ANGLE_MAX_CONTROL * dir_action
                else: number_angle *= dir_action

            
            obj_search = getNameObjFromText(text_array, named_entity_array)
            self.statusSearch(number_angle, obj_search)
           
           
    def statusSearch(self, number_angle:int=0, obj_search=None):
        if obj_search is self.OBJ_EMPTY: self.link_base.step(number_angle)
        else: info_rectangle = self.link_base.stepSearchObj(number_angle, obj_search)
        if not info_rectangle is self.OBJ_EMPTY: self.statusAction(self.getAngleThreeLink, info_rectangle)
        
    def statusAction(status, info_rectangle): pass
    def statusRetraining(self): pass
    
    
    def getFrameInCam(self): return self.cam.getFrame()
    def getFrameInMic(self): return self.mic.getFrame()  
    def viewCam(self): return self.cam.liveView()
    def viewMic(self, audio_data): 
        if isinstance(audio_data, tf.Tensor): audio_data = audio_data.numpy()
        return self.mic.playFrame(audio_data)
    
    def getConfig(self, path=None):
        if not path is None: return saveJson(path=path, data=self.config)
        return self.config
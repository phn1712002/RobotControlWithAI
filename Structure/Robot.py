import pyfirmata, numpy as np, tensorflow as tf, keyboard
from Tools.Json import loadJson, saveJson
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
    
    
    
    def buildModelAI(self):
        self.remove_noise_audio = self.remove_noise_audio.build()
        self.automatic_speech_recognition = self.automatic_speech_recognition.build()
        self.self.named_entity_recognition = self.named_entity_recognition.build()
        
        
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

         
        # Automatic Speech_recognition
        text_command = self.automatic_speech_recognition.predict(speech)
        
        # Named entity
        named_entity = self.named_entity_recognition.predict(text_command)
        
        # Entity classification
        grouped_data = {}
        flag = None
        index = 0
        change = False
        label_skip = ['X', 'UNK']

        for word, label in named_entity:
            tag = label.split('-')
            tag = tag[len(tag) - 1]
            if tag not in label_skip:
                # Check entity change
                if flag != tag:
                    flag = tag
                    change = True
                if change: 
                    index += 1
                    change = False
                
                # Tag with index tag in string
                tag = tag + f'_{index}' 
                
                # Entity division
                if tag in grouped_data:
                    join_word = grouped_data[tag] + ' ' + word
                    grouped_data[tag] = join_word
                else:
                    grouped_data[tag] = word
        print(grouped_data)
        
        # Check name
        call_true_name = False
        tag_name = 'N_1'
        if tag_name in grouped_data: call_true_name = (grouped_data[tag_name] == self.config_robot['name'])
        
        # Get action
        action = None
        tag_name = 'AC_2'
        if tag_name in grouped_data: action = grouped_data[tag_name]
        
        # Get name obj
        obj = None
        tag_name = 'OBJ_3'
        if tag_name in grouped_data: action = grouped_data[tag_name]
        
        # Get direction search
        loc = None
        indicative_phrase_direction_in_place = ['xoay', 'quay']
        tag_name = 'LOC_4'
        if action in  indicative_phrase_direction_in_place: tag_name = 'LOC_3'
        if tag_name in grouped_data: action = grouped_data[tag_name]
        
        # Return
        if call_true_name and not tag_name is None: return action, loc, obj
        else: return None


    def statusSearch(self, infor_from_listen=None):
        if infor_from_listen is None: return None
        else:
            action, loc, obj = infor_from_listen
            
            # Rotating status in place
            indicative_phrase_direction_in_place = ['xoay', 'quay']
            if action in indicative_phrase_direction_in_place:
                if loc == 'phải':
                    sign_step = 1
                elif loc == 'trái':
                    sign_step = -1
                self.controlOneLink(index_link=0, angle_or_oc=sign_step * self.link_base.angle_dir_def)
            
    def statusAction(self): pass
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
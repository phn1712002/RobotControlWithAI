import cv2, mujoco

class World_Venv_V1:
    def __init__(self, path_xml:str, path_folder_model:str):
        self.path_xml = path_xml
        self.path_folder_model = path_folder_model
        self.model = mujoco.MjModel.from_xml_path(path_xml)
        #self.sim = MjSim(self.model)
        #self.viewer = MjViewer(self.sim)
        
    def controlThreeLink(self, angle=(0, 0, 0)):
        check_break = self.checkBreak(angle)
        status_current = self.getAngleThreeLink()
        if not check_break:
            self.sim.data.ctrl[0] = angle[0]
            self.sim.data.ctrl[1] = angle[1]
            self.sim.data.ctrl[2] = angle[2]
            self.sim.step()
        status_future = self.getAngleThreeLink()
        reward, complete = self.getReward(angle, status_current, status_future, check_break)
        return status_future, reward, complete

    def checkBreak(self, angle=(0, 0, 0)):
        return False
    
    def getReward(self, angle_control, status_current, status_future, check_break): pass
    
    def getAngleThreeLink(self):
        return self.sim.data.ctrl
    
    def getCamera(self): pass

    def createPosNewInAeraWorking(self):
        pos = (0, 0, 0)
        return pos
    
    # Code like GymAI of OpenAI
    def step(self, angle:tuple):
        if len(angle) == 3: return self.controlThreeLink(angle=angle)
        else: return None
   
    def state(self): 
        return self.getAngleThreeLink(self)
    
    def reset(self): pass
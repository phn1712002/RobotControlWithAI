
from Structure.Robot import Robot_V1


PATH_CONFIG = 'config_driver.json'
rb = Robot_V1(PATH_CONFIG)
rb.statusListen(play_audio_recoding=True)


"""
import cv2, mujoco
from mujoco import MjModel, Renderer, MjData
xml = "./VirtualEnvironment/arm_robot_simulation.xml"
model = MjModel.from_xml_path(xml)
data = MjData(model)
# Make renderer and render
renderer = Renderer(model)

mujoco.mj_forward(model, data)
renderer.update_scene(data)
pixels = renderer.render()
bgr_image = cv2.cvtColor(pixels, cv2.COLOR_RGBA2BGR)
cv2.imshow("MuJoCo Image", bgr_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""

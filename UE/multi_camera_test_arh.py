import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import os

xml_path = 'left_hand_light.xml' #xml file (assumes this is in the same folder as this file)
simend = 100 #simulation time
print_camera_config = 0
model = mj.MjModel.from_xml_path(xml_path)
data = mj.MjData(model)

def init_controller(model,data):
    #initialize the controller here. This function is called once, in the beginning
    pass

def controller(model, data):
    #put the controller here. This function is called inside the simulation.
    pass


dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname + "/" + xml_path)
xml_path = abspath




# Initialize GLFW to create a window
if not glfw.init():
    raise Exception("GLFW can't be initialized")

window = glfw.create_window(1200, 900, "Demo", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)
glfw.swap_interval(1)

# Define abstract cameras and visualization options
cam = mj.MjvCamera()
cam2 = mj.MjvCamera()
opt = mj.MjvOption()
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150)

# Initialize the cameras
mj.mjv_defaultFreeCamera(model, cam)
mj.mjv_defaultFreeCamera(model, cam2)
mj.mjv_defaultOption(opt)

# Set the parameters for the first camera
cam.azimuth = 90
cam.elevation = -50
cam.distance = 3
cam.lookat = np.array([0.0, 0.0, 0.0])

# Set the parameters for the second camera
cam2.azimuth = 270
cam2.elevation = -50
cam2.distance = 4
cam2.lookat = np.array([0.0, 0.0, 0.0])

# Render loop
while not glfw.window_should_close(window):
    # Update the simulation
    mj.mj_step(model, data)

    # Render from the first camera
    viewport1 = mj.MjrRect(0, 0, 600, 900)
    mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL, scene)
    mj.mjr_render(viewport1, scene, context)

    # Render from the second camera
    viewport2 = mj.MjrRect(600, 0, 600, 900)
    mj.mjv_updateScene(model, data, opt, None, cam2, mj.mjtCatBit.mjCAT_ALL, scene)
    mj.mjr_render(viewport2, scene, context)

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Terminate GLFW when done
glfw.terminate()

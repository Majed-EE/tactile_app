import mujoco as mj
from mujoco.glfw import glfw
import numpy as np
import time as T
import math
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import json
import cv2
scene_no=0
scene_xml=["vertical_arh_soft_scene.xml","vertical_arh_sphere_scene.xml"]

xml_path = scene_xml[scene_no]#"vertical_arh_soft_scene.xml"  #"arh_soft_scene1.xml"   #"arh_sphere_scene1.xml"   #"left_hand_light.xml"   #"arh_sphere_scene1.xml"  #"arh_soft_scene1.xml"    #'left_hand_light_with_cube.xml'#"arh_soft_scene1.xml"   #'left_hand_light.xml' #xml file (assumes this is in the same folder as this file)
# simend = 100 #simulation time
N = 300
print_camera_config = 0
model = mj.MjModel.from_xml_path(xml_path)
data = mj.MjData(model)

global body_dict, all_axis

global finger_0,finger_1,finger_2,finger_3,open
finger_0=['rfj0', 'rfj1', 'rfj2', 'rfj3']
finger_1=['mfj0', 'mfj1', 'mfj2', 'mfj3']
finger_2=['ffj0', 'ffj1', 'ffj2', 'ffj3']
finger_3=['thj0', 'thj1', 'thj2', 'thj3']


simend=N


tree = ET.parse(xml_path)
root = tree.getroot()
body_dict = {}
joint_dict={}
body_id=0
joint_flag=False
for body in root.findall('.//body'):
        body_name = body.get('name')
        if body_name is None:
            continue
        # body.findall('joint')
        for joint in body.findall('joint'):
            joint_flag=True
            joint_name = joint.get('name')
            # print(joint_name)
            body_dict[body_id]={"body_name":body_name,
                               "body_id":body_id,
                                "joint_name": joint.get('name')
            # "joint_type" : joint.get('type'),
            # # joint_pos = joint.get('pos'),
            # # joint_axis = joint.get('axis')
            # "joint_range" : joint.get('range')
            }
        if not joint_flag: # if link is present
            body_dict[body_id]={"body_name":body_name,
                               "body_id":body_id}
        joint_flag=False
            
        body_id+=1
# print(body_dict)
try:

    for key in body_dict.keys():
        if "joint_name" in body_dict[key]:
            # print(body_dict[key]["joint_name"])
            actuator_name=body_dict[key]["joint_name"].replace('j', 'a')
            body_dict[key]["actuator_name"]=actuator_name



    actuator_list=[["ffa0",0,8],["ffa1",1,9],["ffa2",2,10],["ffa3",3,11],
            ["mfa0",4,4],["mfa1",5,5],["mfa2",6,6],["mfa3",7,7],
            ["rfa0",8,0],["rfa1",9,1],["rfa2",10,2],["rfa3",11,3],
            ["tha0",12,12],["tha1",13,13],["tha2",14,14],["tha3",15,15]]
    def actuator_key(act_name):

        # index_found=False
        for index in range(len(actuator_list)):
            if actuator_list[index][0]==act_name:
                # print(index)
                return index
            
    for key in body_dict.keys():
        if 'actuator_name' in body_dict[key].keys():
            # print(body_dict[key]['actuator_name'])        
            ind=actuator_key(body_dict[key]['actuator_name'])
            # print(actuator_list[ind])
            body_dict[key]['actuator_id']=actuator_list[ind][1]
            body_dict[key]['joint_id']=actuator_list[ind][2] # ["actuator name", actuator_id ,joint_id  ]


    # print(body_dict)

            # body_dict[key]['body_name']=actuator_list[ind][1]
            # body_dict[key]['joint_id']=actuator_list[ind][2] # ["actuator name", actuator_id ,joint_id  ]
except:
    pass


#######################  Body dict complete #############








def load_dict_from_json(filename):
    with open(filename, 'r') as json_file:
        dictionary = json.load(json_file)
    return dictionary


body_dict = load_dict_from_json('body_dict.json')

# print(body_dict)

#########################################################

def getTipInfo():
    global body_dict
    for key in body_dict.keys():
        tip_id=[]
        if 'actuator_name' not in body_dict[key].keys():
            # print(body_dict[key]['actuator_name'])        
            # ind=actuator_key(body_dict[key]['actuator_name'])
            # print(actuator_list[ind])
            if "tip" in body_dict[key]['body_name']:
                body_name=body_dict[key]['body_name']
                body_id=body_dict[key]['body_id']
                print(body_name,body_id)
                tip_id.append(body_id)
    return tip_id

print("tip body name and id")
tip_list=getTipInfo()

# print("applied force")
# print(data.cfrc_ext[tip_list])
# print(data.xfrc_applied[tip_list[0]])









def getJointInfo():
    global body_dict
    global model
    joint_name_list=[]
    joint_id_list=[]
    # print(f"numJoints {model.njnt}")
    for key in body_dict.keys():
        if 'joint_name' in body_dict[key].keys():
            # print(f"joint name {body_dict[key]['joint_name']} | joint id: {body_dict[key]['joint_id']}")
            joint_name_list.append(body_dict[key]['joint_name'])
            joint_id_list.append(body_dict[key]['joint_id'])
    return joint_name_list,joint_id_list

joint_list,joint_id_list=getJointInfo()
# print(joint_list)



def getActuatorInfo():
    global body_dict
    global model
    for key in body_dict.keys():
        if 'actuator_name' in body_dict[key].keys():
            print(f"actuator name {body_dict[key]['actuator']} | actuator id: {body_dict[key]['actuator_id']}")


def getBodyInfo():
    global body_dict
    global model
    print(f"numBody {model.nbody-1}") # -1 for the world
    

    for key in body_dict.keys():
        if 'body_name' in body_dict[key].keys():
            print(f"body name {body_dict[key]['body_name']} | body id: {body_dict[key]['body_id']}")




######################### Mapping Variables ############################### 







######################### Control Variables ################################

def setPositionControl(joint_id,angle):
    q_start = 0
    q_end = math.radians(angle); # ending angle # 90 degrees-------------------
    q = np.linspace(q_start,q_end,N)
    data.qpos[joint_id] = q_start;
    # print(q)
    return q


 


def positionControlArray(list_joint_id,list_target_angle):
    if len(list_joint_id)==len(list_target_angle):
        for joint_id in range (len(list_joint_id)):
            set_position_servo(list_joint_id[joint_id],list_target_angle[joint_id])

def set_position_servo(joint_id,bend_angle):
    
    # model.actuator_gainprm[actuator_no,0]=kp
    # model.actuator_biasprm[actuator_no,1]=-kp
    # print(f"joint id {joint_id}")
    # print(joint_id)
    data.ctrl[joint_id]=math.radians(bend_angle)
    # print("ctrl matrix")
    # print(data.ctrl)




def actuator_name2id(actuator_name):
    actuator_id=None
    for key, value in enumerate(body_dict):
         if "actuator_name" in body_dict[key]:
            if body_dict[key]["actuator_name"]==actuator_name:
            # actuator_name=body_dict[key]["joint_name"].replace('j', 'a')
                actuator_id=body_dict[key]["actuator_id"]
                return actuator_id



def joint_name2id(joint_name):
    joint_id=None
    global body_dict
    # print("global body dict")

    # print(body_dict)
    # print("global")
    # print("in joint_name2id block")
    for key in body_dict.keys():
        #  print(key)
         body_dict[key]
         if "joint_name" in body_dict[key]:
            if body_dict[key]["joint_name"]==joint_name:
            # actuator_name=body_dict[key]["joint_name"].replace('j', 'a')
                joint_id=body_dict[key]["joint_id"]
                return joint_id 


def joint_id2name(joint_id):
    # joint_id=None
    global body_dict

    for key in body_dict.keys():
        #  print(key)
        #  print(joint_id)
         body_dict[key]
        #  print(body_dict[key])
         if "joint_id" in body_dict[key]:
            if body_dict[key]["joint_id"]==joint_id:
            # actuator_name=body_dict[key]["joint_name"].replace('j', 'a')
                joint_name=body_dict[key]["joint_name"]
                return joint_name 












open=True

def controller(model,data):
    global finger_0,finger_1,finger_2,finger_3,open
    finger_0=['rfj0', 'rfj1', 'rfj2', 'rfj3']
    finger_1=['mfj0', 'mfj1', 'mfj2', 'mfj3']
    finger_2=['ffj0', 'ffj1', 'ffj2', 'ffj3']
    finger_3=['thj0', 'thj1', 'thj2', 'thj3']


    finger_0a=['rfj1', 'rfj2', 'rfj3']
    finger_1a=['mfj1', 'mfj2', 'mfj3']
    finger_2a=['ffj1', 'ffj2', 'ffj3']
    # finger_3a=['thj1', 'thj2', 'thj3']


    if open:

        joint_name_list=finger_1a[:2] #finger_0a+finger_1a+finger_2a+finger_3
        # joint_name_list,_=getJointInfo() # ['rfj0', 'rfj1',
        # 'rfj2', 'rfj3', 'mfj0', 'mfj1', 'mfj2', 'mfj3', 'ffj0', 'ffj1', 'ffj2', 'ffj3', 'thj0', 'thj1', 'thj2', 'thj3']
        target_bend_list_radian=[0.824,1.16,0.865,0.496] #[90,90,90,90]#[0.824,1.16,0.865,0.496]
        # for x in range(len(target_bend_list_radian)):

            
        target_bend_list_thumb=[math.degrees(x) for x in target_bend_list_radian ]
        target_bend_list=[90]*(len(joint_name_list)*1) #+target_bend_list_thumb
        # print(target_bend_list)
        joint_id_list=[]
        for joint_name in range(len(joint_name_list)):

            joint_id=joint_name2id(joint_name_list[joint_name])
            joint_id_list.append(joint_id)
        # print(f"return joint id is {joint_id}")
        # print(joint_id)
        positionControlArray(joint_id_list,target_bend_list)








    if not open:
        joint_name_list=finger_0+finger_1+finger_2+finger_3
        # joint_name_list,_=getJointInfo() # ['rfj0', 'rfj1',
        # 'rfj2', 'rfj3', 'mfj0', 'mfj1', 'mfj2', 'mfj3', 'ffj0', 'ffj1', 'ffj2', 'ffj3', 'thj0', 'thj1', 'thj2', 'thj3']
        # target_bend_list_radian=[0.824,1.16,0.865,0.496] #[90,90,90,90]#[0.824,1.16,0.865,0.496]
        # for x in range(len(target_bend_list_radian)):

            
        # target_bend_list_thumb=[math.degrees(x) for x in target_bend_list_radian ]
        target_bend_list=[0]*(len(finger_2)*4)
        # print(target_bend_list)
        joint_id_list=[]
        for joint_name in range(len(joint_name_list)):

            joint_id=joint_name2id(joint_name_list[joint_name])
            joint_id_list.append(joint_id)
        # print(f"return joint id is {joint_id}")
        # print(joint_id)
        positionControlArray(joint_id_list,target_bend_list)





#set the controller
mj.set_mjcb_control(controller)

############################################ Controller Varables #################################################







################################################ Camera Position Orientation #############################333

def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)

def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    # update mouse position
    glfw.get_cursor_pos(window)

def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
        return

    # get current window size
    width, height = glfw.get_window_size(window)

    # get shift key state
    PRESS_LEFT_SHIFT = glfw.get_key(
        window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(
        window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx/height,
                      dy/height, scene, cam)

def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)





########################################## Camera Variables Start #####################################################
# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

if not glfw.init():
    raise Exception("GLFW can't be initialized")

window = glfw.create_window(1200, 900, "Demo", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)
glfw.swap_interval(1)


cam = mj.MjvCamera()
# cam2 = mj.MjvCamera()
opt = mj.MjvOption()
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150)


mj.mjv_defaultCamera(cam) ## change to default free camera for multiple camera mount
# mj.mjv_defaultFreeCamera(model, cam2)
mj.mjv_defaultOption(opt)
scene = mj.MjvScene(model, maxgeom=10000)
context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

cam.azimuth = 85
cam.elevation = 0.4
cam.distance = 0.6
cam.lookat = np.array([0.0, 0.0, 0.0])

# cam.azimuth = 84.79999999999995 ; cam.elevation = 0.39999999999994823 ; cam.distance =  0.5520500437097977
# cam.lookat =np.array([ 0.0 , 0.0 , 0.0 ])


# cam2.azimuth = 270
# cam2.elevation = -50
# cam2.distance = 4
# cam2.lookat = np.array([0.0, 0.0, 0.0])

# install GLFW mouse and keyboard callbacks
glfw.set_key_callback(window, keyboard)
glfw.set_cursor_pos_callback(window, mouse_move)
glfw.set_mouse_button_callback(window, mouse_button)
glfw.set_scroll_callback(window, scroll)



############################################################ CAM context ################################################

# joint_id=13

# print(body_dict)
print("\n")

def custom_array(data_array):
    custom_array=np.copy(data_array)
    return custom_array
# joint_torque_array=[]
all_axis=[]
index=0
all_axis.append(index)
# torque_targeJnt=[3,7]
torque_stack_array=np.copy(data.qfrc_actuator)
# actuator_force_stack=np.copy(data.actuator_force)
data_to_check= data.qfrc_smooth#cfrc_int #qfrc_inverse   #  qfrc_constraint#data.qfrc_smooth
check_np=custom_array(data_to_check)


angle_stack_array=np.copy(data.qpos)
# print(torque_stack_array)
# # while not glfw.window_should_close(window):
frame_count=simend
frames=[]
for x in range(simend):
 
    step_start = T.time()
    mj.mj_step(model, data)
    joint_angles = np.copy(data.qpos)
    joint_torques = np.copy(data.qfrc_actuator)
    actuator_force=np.copy(data.qfrc_smooth)
    data_check_loop=np.copy(data_to_check)
    # actuator_force=np.copy(data.actuator_force)
    qfrc_inv_array=np.copy(data.qfrc_inverse)

    


    torque_stack_array=np.vstack((torque_stack_array,joint_torques))
    angle_stack_array=np.vstack((angle_stack_array,joint_angles))
    # actuator_force_stack=np.vstack((actuator_force_stack,actuator_force))
    check_np=np.vstack((check_np,data_check_loop))
    # print(qfrc_inv_array)
    # print("\n")
    # print(check_np)

    joint_angles_thumb=np.degrees(joint_angles[12:])
    # print(joint_angles_thumb[0])

    # print("applied force")
    # print(data.cfrc_ext[tip_list])
    # print(data.contact)


    if joint_angles_thumb[0]>=41:
        open=True
        # pass
    

        # Get contact forces
  
        # for i in range(ncon):
        #     contact = data.contact[i]
        #     force = np.zeros(6)
        #     mj.mj_contactForce(model, data, i, force)
        #     print("ncon:")
        #     print(f"{ncon} and \nforce: {force[:3]} ")
        #     contact_forces.append(force)

    ncon = data.ncon
    print(ncon)
    contact_info = []



    for i in range(ncon):
        contact = data.contact[i]
        body1 = model.geom_bodyid[contact.geom1]
        body2 = model.geom_bodyid[contact.geom2]
        force = np.zeros(6)
        mj.mj_contactForce(model, data, i, force)
        contact_info.append((body1, body2, force))
        print(contact_info)
        

    # Print the body IDs and contact forces
    for i, (body1, body2, force) in enumerate(contact_info):
        body1_name = mj.mj_id2name(model, mj.mjtObj.mjOBJ_BODY, body1)
        body2_name = mj.mj_id2name(model, mj.mjtObj.mjOBJ_BODY, body2)
        print(f"Contact {i}: Body1 = {body1_name}, Body2 = {body2_name}, Force = {force[:3]}, Torque = {force[3:]}")







        # print(contact_forces)

    all_axis.append(index)
    index+=1
    # print(index)
    # data.qpos[joint_id] = q[x];
    # data.qpos[1] = q1[i];

    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # print(f"angle {math.degrees(joint_angles[joint_id])}")
    
    # # print(f"torque {joint_torques[joint_id]}")
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


    ############## camera scene buffer viewport etc setting ##############################33
        # get framebuffer viewport
    viewport_width, viewport_height = glfw.get_framebuffer_size(
        window)
    viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

     #print camera configuration (help to initialize the view)
    if (print_camera_config==1):
        print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
        print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')


    mj.mjv_updateScene(model, data, opt, None, cam,
                       mj.mjtCatBit.mjCAT_ALL.value, scene)
    mj.mjr_render(viewport, scene, context)


    width,height=viewport_width, viewport_height
    # viewport1 = mj.MjrRect(0, 0, 600, 900)
    # mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL, scene)
    # mj.mjr_render(viewport1, scene, context)


    # viewport2 = mj.MjrRect(600, 0, 600, 900)
    # mj.mjv_updateScene(model, data, opt, None, cam2, mj.mjtCatBit.mjCAT_ALL, scene)
    # mj.mjr_render(viewport2, scene, context)



    #################################### frame details ################################3
    # Frame from the renderer 
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    depth = np.zeros((height, width), dtype=np.float32)
    mj.mjr_readPixels(rgb, depth, viewport, context)
    
    # RGB to BGR for OpenCV
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    rotated_image = cv2.rotate(bgr, cv2.ROTATE_180)
    flipped_frame = cv2.flip(rotated_image, 1)

    # Save the frame as an image
    image_path = f'scene_des/zzz_frame_{x:04d}.png'
    cv2.imwrite(image_path, flipped_frame)
    
    # frame info
    # frames.append(bgr)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()





############################### graph plotter and data #######################################333



target_joint=[joint for joint in range (0,16)]
target_joint_name=[joint_id2name(joint_id) for joint_id in target_joint]
print(target_joint_name)



def graph_plotter_joints(target_stack_array,attribute):
    global all_axis,target_joint, target_joint_name

    plt.figure(figsize=(10, 6))
    for joint in range(len(target_joint)):
        # print(torque_stack_array[0])

        plt.plot(all_axis, target_stack_array[target_joint[joint]], linestyle='-',label=f'{attribute} for joint {target_joint_name[joint]}')


        # plt.scatter(all_axis,  torque_stack_array[target_joint[joint]], color='r', label=f'Torque for joint {target_joint[joint]}')

    plt.title(f'{attribute} of joints')
    plt.xlabel('Steps')
    plt.ylabel(f'{attribute}')
    plt.legend()
    plt.grid(True)

    plt.show()

angle_stack_array=np.degrees(angle_stack_array.T)
torque_stack_array=torque_stack_array.T
finger_3
# actuator_force_stack=actuator_force_stack.T
unconstrained_torque_stack=check_np.T
# graph_plotter_joints(angle_stack_array,"Angle")
# graph_plotter_joints(unconstrained_torque_stack, "Torque")





# Save frames as a video file
# output_video_path = 'simulation_output.avi'
# fps = 30
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# for frame in frames:
#     video_writer.write(frame)

# video_writer.release()

# # Optionally, save individual frames as images
# for i, frame in enumerate(frames):
#     image_path = f'frame_{i:04d}.png'
#     Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(image_path)

# print(f'Video saved as {output_video_path}')


















print("end of program")


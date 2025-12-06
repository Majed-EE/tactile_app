#!/usr/bin/env python3
# original code
import websocket
import json
from time import sleep
import threading
import numpy as np
import logging
import sys, asyncio

# if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure logger
state=["rest","fast", "slow"]
state_id=1
file_name=__file__[:-3]+"log.log"
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler(file_name),  # Log to file
        logging.StreamHandler()              # Log to console
    ]
)

log_data=True
print("running filename: ", file_name)




global k,N
N=100 # total time steps
taxel_log=[]
k=0

ip = "10.50.49.23"
#"192.168.0.103"  # your computer IP on the network
port = 5000  # the port the server is running on



lastmessage = {"message": "No message"}  # default message you will overwrite when you get update

def on_message(wsapp, message):
    global lastmessage  # globalize to overwrite original
    try:
        data = json.loads(message)
    except Exception:
        pass
    else:
        try:
            if data["message"] == "Welcome":  # get the Welcome Message with details, print if you like
                logging.info(f"Data: {data}")
                print(f"type(data): {type(data)}")

                t=0.1 # sleep time between messages
                print(f"sleeping for {t} second")
                sleep(t)
            else:
                lastmessage = data
        except Exception:
            pass  # ignore message as it's probably invalid

def threader(target, args=False, **targs):
    # args is tuple of arguments for threaded function other key-value pairs will be sent to Thread
    if args:
        targs["args"] = (args,)
    thr = threading.Thread(target=target, **targs)
    thr.daemon = True
    thr.start()
from matplotlib import pyplot as plt
def mesreader():  # this is your app reading the last valid message you received
    global k, N
    plt.ion()
    # fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    data_x, data_y, data_z = [], [], []
    while True:  # to run forever
        try:
            if lastmessage["message"] != "No message":
                # logging.info(f"\n####################################\nI received: \n{lastmessage}\n")
                print(f"type(lastmessage): {type(lastmessage)}")
            
                # for k,v in lastmessage.items():
                #     print(k)
                taxel_np=np.asarray(lastmessage['1']['special'])
                # print(f"taxel_np shape: {taxel_np.shape}") # (16,12)
                raw_taxel_value=taxel_np[:, :3]
                normalized_force=taxel_np[:, -1:]
                # print(f"sliced taxel shape {raw_taxel_value}, {normalized_force}")
                # print(f"slice taxel shape {taxel_np[:, :3].shape}, {}")
                taxel_np = np.hstack((raw_taxel_value, normalized_force))# what is this doing
                # taxel_np=taxel_np[:,:3]
                # print(f"row taxels shape: {taxel_np.shape}") # raw x,y,z for each taxel->[16,3]
                # t=0.01
                # print(f"value of k: {k}\nsleeping for {t} seconds")
                if k<N: # total time step
                    taxel_log.append(taxel_np)
                    print("sample k of N: ", k,N)
                    k+=1
     
                    # plt.pause(0.1)

                else:
                    final_np=np.array(taxel_log)
                    if log_data:
                        print("saving numpy array")
                        # plt.savefig("running_plot_XelaUSkin.png")
                        
                        print(f"shape of final array: {final_np.shape}")
                        name_File="z_sample"+state[state_id]+"_taxel_log.npy"
                        np.save(name_File, final_np)
                    else: 
                        print("Not logging data, program end")
                        print(f"shape of final array: {final_np.shape}")
                
                # sleep(t)
                pass
            t1=0.05 # sleep time between messages
            print(f"sleeping for {t1} seconds")
            sleep(t1)  # your calculations and processes here (sleep is used as simulation here)
        except KeyboardInterrupt:
            break  # break on KeyboardInterrupt
        except Exception as e:
            logging.error(f"Exception: {type(e).__name__}: {e}")

try:  # try to close the app once you press CTRL + C
    threader(mesreader, name="Receiver")  # start you main app
    websocket.setdefaulttimeout(1)  # you should avoid increasing it.
    wsapp = websocket.WebSocketApp("ws://{}:{}".format(ip, port), on_message=on_message)  # set up WebSockets
    wsapp.run_forever()  # Run until connection dies
except Exception:
    exit()
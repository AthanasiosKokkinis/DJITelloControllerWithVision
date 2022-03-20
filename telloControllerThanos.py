from djitellopy import Tello
import cv2
from pynput import keyboard
from threading import Thread
#left_right=0

def initializeTello(): # Gia na kanw arxikopoihsh drone
    tello_drone=Tello() # Antikeimeno
    tello_drone.connect() # Sundesh
    print(tello_drone.get_battery()) # Mas dinei thn mpataria
    tello_drone.for_back_velocity=0 # Mhdenizw arxikes taxuthtes
    tello_drone.left_right_velocity=0
    tello_drone.up_down=0
    tello_drone.yaw_velocity=0
    tello_drone.speed=0
    tello_drone.steamoff() # Stamataw to stream an einai anoikto 
    return trello_drone

def shareVision(): # Dwse video
    global drone
    drone.streamon() # Anoigw to stream
    frame_read=drone.get_frame_read() # Pairnw ta frames gia panta
    recording=True
    while recording: # Den eimai sigouros oti xreiazetai
        cv2.imshow("Tello vision",frame_read.frame) # Mallon den xreiazetai na kanw ontws lhpsh neou frame
        sleep(1/30) # 8ewrhtika 30 fps

def drone_handler(key): # Controller
    global drone # Pragmatika, h Python einai toso xalia pou me anagkazei na xrhsimopoiw global, gt to keyboard den me afhnei na kanw polla....
    step=1
    speed=10
    angle_step=5
    if key==keyboard.Key.esc:
        drone.land() # Prosgeiwsh
        exit()
    elif key==keyboard.Key.d:
        drone.go_xyz_speed(step,0,0,speed) # Fantasou na exw kanei patata me tis dieu8unseis xD
        print("Right")
    elif key==keyboard.Key.w:
        drone.go_xyz_speed(0,step,0,speed)
        print("Forward")
    elif key.char==keyboard.Key.a:
        drone.go_xyz_speed(-step,0,0,speed)
        print("Left")
    elif key==keyboard.Key.s:
        drone.go_xyz_speed(0,-step,0,speed)
        print("Back")
    elif key==keyboard.Key.space:
        drone.go_xyz_speed(0,0,step,speed)
        print("Up")
    elif key==keyboard.Key.shift_l:
        drone.go_xyz_speed(0,0,-step,speed)
        print("Down")
    elif key=='e':
        drone.rotate_clockwise(angle_step)
        print("Clockwise rotation")
    elif key=='q':
        drone.rotate_counter_clockwise(angle_step)
        print("Counter clockwise rotation")

def main(): # Main sunarthsh
    drone=initializeTello() # Drone init
    drone.takeoff() # Flyyy
    keyboard_listener=keyboard.Listener(on_press=drone_handler) # Poia sunarthsh 8a akouei
    keyboard_listener.start() # Thread gia keyboard
    vision_thread=Thread(target=shareVision)
    vision_thread.start() # Thread gia camera
    
main()



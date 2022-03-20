from djitellopy import Tello
import cv2
from pynput import keyboard
from threading import Thread
#left_right=0

def initializeTello(): # Drone initialization
    tello_drone=Tello()
    tello_drone.connect() # Connect to drone
    print(tello_drone.get_battery()) # Battery percentage
    tello_drone.for_back_velocity=0 # Make initial velocities zero
    tello_drone.left_right_velocity=0
    tello_drone.up_down=0
    tello_drone.yaw_velocity=0
    tello_drone.speed=0
    tello_drone.steamoff() # Stop video streaming if open
    return trello_drone

def shareVision(): # Function for video streaming
    global drone
    drone.streamon() # Open the stream
    frame_read=drone.get_frame_read() # This is a callback function which returns the frames 
    recording=True
    while recording:
        cv2.imshow("Tello vision",frame_read.frame) # Show the frame
        sleep(1/30) # Limit video to 30fps

def drone_handler(key): # Controller
    global drone # Global drone object
    step=1 # Step for translational movement, might get deleted in future updates.
    speed=10 # Speed of movement
    angle_step=5 # Step for rotational movement
    if key==keyboard.Key.esc:
        drone.land() # Land the drone
        exit()
    elif key==keyboard.Key.d:
        drone.go_xyz_speed(step,0,0,speed) # Move to the right
        print("Right")
    elif key==keyboard.Key.w:
        drone.go_xyz_speed(0,step,0,speed) # Move forward
        print("Forward")
    elif key.char==keyboard.Key.a:
        drone.go_xyz_speed(-step,0,0,speed) # Move to the keft
        print("Left")
    elif key==keyboard.Key.s:
        drone.go_xyz_speed(0,-step,0,speed) # Move backwards
        print("Back")
    elif key==keyboard.Key.space:
        drone.go_xyz_speed(0,0,step,speed) # Go up
        print("Up")
    elif key==keyboard.Key.shift_l:
        drone.go_xyz_speed(0,0,-step,speed) # Go down
        print("Down")
    elif key=='e':
        drone.rotate_clockwise(angle_step) # Rotate clockwise
        print("Clockwise rotation")
    elif key=='q':
        drone.rotate_counter_clockwise(angle_step) # Rotate anti-clockwise
        print("Counter clockwise rotation")

def main(): # Main fucntion
    drone=initializeTello() # Drone init
    drone.takeoff() # Fly
    keyboard_listener=keyboard.Listener(on_press=drone_handler) # Thread for keyboard
    keyboard_listener.start() 
    vision_thread=Thread(target=shareVision) # Vision thread
    vision_thread.start()
    
main()



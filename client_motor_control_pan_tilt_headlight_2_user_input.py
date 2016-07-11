import time
import roboclaw

import socket
from socket import error as SocketError
import errno

import pigpio

#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
roboclaw.Open("/dev/ttyACM0",115200)

address = 0x80
overall_speed = 10
direction1 = ""
direction2 = ""


pi = pigpio.pi()
top_servo = 17
mid_servo = 5
btm_servo = 6
mid_pos = 2150
btm_pos = 500
top_pos = 1200
pi.set_servo_pulsewidth(top_servo, top_pos)
pi.set_servo_pulsewidth(mid_servo, mid_pos)
pi.set_servo_pulsewidth(btm_servo, btm_pos)

pi.set_mode(22, pigpio.OUTPUT) #light


##TCP_IP = '192.168.2.125'
##TCP_PORT = 5005
##BUFFER_SIZE = 1  # Normally 1024, but we want fast response
##
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.bind((TCP_IP, TCP_PORT))
##s.listen(1)

def forward(motor, speed):
    if motor == 1:
        roboclaw.ForwardM1(address, speed)
        global direction1
        direction1 = "forward"

    else:
        roboclaw.ForwardM2(address, speed)
        global direction2
        direction2 = "forward"

def reverse(motor, speed):
    if motor == 1:
        roboclaw.BackwardM1(address, speed)
        global direction1
        direction1 = "reverse"
    else:
        roboclaw.BackwardM2(address, speed)
        global direction2
        direction2 = "reverse"

def stop(motor):
    if motor == 1:
        roboclaw.ForwardM1(address, 0)
        global direction1
        direction1 = "stop"
    else:
        roboclaw.ForwardM2(address, 0)
        global direction2
        direction2 = "stop"
    
def turn_left(speed):
    roboclaw.ForwardM1(address, speed)
    global direction1
    direction1 = "forward"
    roboclaw.BackwardM2(address, speed)
    global direction2
    direction2 = "reverse"

def turn_right(speed):
    roboclaw.BackwardM1(address, speed)
    global direction1
    direcetion1 = "reverse"
    roboclaw.ForwardM2(address, speed)
    global direction2
    direction2 = "forward"

def change_speed(change):
    global overall_speed
    if change == "q":
        overall_speed += 5
        print("Go faster")
    elif change == "e":
        overall_speed -= 5
        print("Go slower")
    else:
         overall_speed = change
         
    print"Speed: " 
    print overall_speed
    global direction1
    global direction2

    if direction1 == "forward":
        forward(1, overall_speed)
    elif direction1 == "reverse":
        reverse(1, overall_speed)
    if direction1 == "stop":
        stop(1)

    if direction2 == "forward":
        forward(2, overall_speed)
    elif direction2 == "reverse":
        reverse(2, overall_speed)
    elif direction2 == "stop":
        stop(2)

while(1):
     message = raw_input("Enter something: ")
     
     if message == "k" and top_pos >= 800:
          global top_pos
          top_pos -= 50
          print "top_servo up"
                     

     elif message == "i" and top_pos <= 2400:
          global top_pos
          top_pos += 50
          print "top_servo down:"
          
            
     elif message == "l":
          if mid_pos > 500:
               global mid_pos
               mid_pos -=50
               print "mid_servo right"     
             
          elif btm_pos > 500:
               global btm_pos
               btm_pos -= 50
               print "btm_servo right"
              
          else:
               print "All the way right"
               

     elif message == "j":
          if mid_pos < 2500:
               global mid_pos
               mid_pos +=50
               print "mid_servo left"
                     
          elif btm_pos < 2500:
               global btm_pos
               btm_pos += 50
               print "btm_servo left"
               
          else:
               print "All the way left"
               

     elif message == "f":
          global btm_pos
          global mid_pos
          global top_pos
          btm_pos = 500
          mid_pos = 2150
          top_pos = 1200
          print "facing forwards"
          
     elif message == "b":
          global btm_pos
          global mid_pos
          global top_pos
          btm_pos = 2050
          mid_pos = 2500
          top_pos = 1200
          print "facing backwards"

     print "btm_pos: "
     print btm_pos
     print "mid_pos: "
     print mid_pos
     print "top_pos: "
     print top_pos


     pi.set_servo_pulsewidth(top_servo, top_pos)
     pi.set_servo_pulsewidth(mid_servo, mid_pos)
     pi.set_servo_pulsewidth(btm_servo, btm_pos)

		
	
 ##Control movement of rover
   
     if message == "w":
          forward(1, overall_speed)
          forward(2, overall_speed)
          print("Both motors forward")

     elif message == "s":
          reverse(1, overall_speed)
          reverse(2, overall_speed)
          print("Both motors reverse" )

     elif message == " ":
          stop(1)
          stop(2)
          
     elif message == "a":
          turn_left(overall_speed)
          print("Turn left")

     elif message == "d":
          turn_right(overall_speed)
          print("Turn right")

     elif message == "q" or message == "e":
          change_speed(message)
          
     elif message == "":
         print("Nothing Entered")

     elif message in "123456789":
          key = int(message)
          global overall_speed
          new_speed = key*10
          change_speed(new_speed)

     ##Control light
           
     elif message == "g":
          pi.write(22,1)
          print ("LED ON")
           
     elif message == "h":
          pi.write(22,0)
          print ("LED OFF")
           

     elif message == "quit":
          print "OK. Fine. I'll stop."
          break
       
     message = "null"

     
        
pi.set_servo_pulsewidth(top_servo, 0)  #detach up/down servo
pi.set_servo_pulsewidth(mid_servo, 0)  #detach left-middle servo
pi.set_servo_pulsewidth(btm_servo, 0)  #detach middle-right servo

pi.write(22,0)   # detach LED 

pi.stop()

print "Stopped"       

conn.close()


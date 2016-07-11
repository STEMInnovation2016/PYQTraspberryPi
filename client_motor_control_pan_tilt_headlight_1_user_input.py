import time
import roboclaw

import socket
from socket import error as SocketError
import errno

import pigpio
 
#Windows comport name
#roboclaw.Open("COM3",115200)
#Linux comport name
#roboclaw.Open("/dev/ttyACM0",115200)

address = 0x80
overall_speed = 10
direction1 = ""
direction2 = ""

pi = pigpio.pi()
pi.set_servo_pulsewidth(17,1200)
pi.set_servo_pulsewidth(5,2150)
pi.set_servo_pulsewidth(6,500)
ud = 17
mr = 5
lm = 6
mrpos = 2150
lmpos = 500
lrpos = 2650
udpos = 1200

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
    else:
        overall_speed -= 5
        print("Go slower")

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

##    conn, addr = s.accept()
    while (1):
##        try:
##            data = conn.recv(1)
##        except SocketError as e:
##            if e.errno != errno.ECONNRESET:
##                raise # Not error we are looking for
##            pass # Handle error here.
##        if not data: break
##        print data
##        message = data
        #conn.send(data)  # echo
        message = raw_input("Enter something: ")
    
        ##Control Pan and Tilt Camera    
        if message == "k" and udpos >= 800:
                global udpos
		udpos -= 50
		print "ud up"
		print "udpos"
		print udpos
		
	elif message == "i" and udpos <= 2400:
                global udpos
		udpos += 50
		print "ud down"
		print "udpos"
		print udpos
		
	elif message == "l" and lrpos <= 3000 and lrpos >= 1050:
                global lrpos
		lrpos -= 50
		global mrpos
		mrpos -=50
		print "mr right"
		print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos
		print "lmpos "
		print lmpos
				
	elif message == "j" and lrpos <= 2950:
                global lrpos
		lrpos += 50
		global mrpos
		mrpos += 50
		print "mr left"
		print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos
		print "lmpos "
		print lmpos
		
	elif message == "l" and lrpos >=3050:
                global lrpos
                lrpos -= 50
                global lmpos
		mrpos -= 50
		print "mr right"
		print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos
		print "lmpos "
		print lmpos
		
	elif message == "j" and lrpos >=3000 and lrpos <=4900:
		global lrpos
		lrpos += 50
		global lmpos
		lmpos += 50
		print "lm left"
		print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos
		print "lmpos "
		print lmpos

	elif message == "f":
                global lrpos
                lrpos = 2650
                global mrpos
                mrpos = 2150
                global lmpos
                lmpos = 500
                print "facing forwards"
                print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos
		print "lmpos "
		print lmpos

	elif message == "b":
                global lrpos
                lrpos = 4550
                global mrpos
                mrpos = 2500
                global mlpos
                lmpos = 2050
                print "facing backwards"
		print "mrpos "
		print mrpos
		print "lrpos "
		print lrpos		
                print "lmpos "
		print lmpos
		
	

        pi.set_servo_pulsewidth(ud, udpos)
        pi.set_servo_pulsewidth(lm, lmpos)
        pi.set_servo_pulsewidth(mr, mrpos)
        


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

pi.set_servo_pulsewidth(ud, 0)  #detach up/down servo
pi.set_servo_pulsewidth(lm, 0)  #detach left-middle servo
pi.set_servo_pulsewidth(mr, 0)  #detach middle-right servo

pi.write(22,0)

pi.stop()

print "Stopped"       

conn.close()


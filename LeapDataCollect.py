################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################
#
#   originally written by Sarah Almeda at The College of New Jersey 2/2018
#   editted by Forum Modi at The College of New Jersey 10/2019
#
################################################################################

from __future__ import with_statement
from datetime import datetime
import Leap, sys, thread, time, msvcrt, os
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


def getch():
    #tty.setcbreak(sys.stdin)
    #ch = (sys.stdin.read(1))
    ch = msvcrt.getch();
    
    return ch

button_delay = 0.2

def getDistance(vector1, vector2):
    x1 = vector1.x
    y1 = vector1.y
    z1 = vector1.z
    x2 = vector2.x
    y2 = vector2.y
    z2 = vector2.z
    result = math.sqrt( ((x1 - x2)**2)+((y1 - y2)**2) + ((z1 - z2)**2) )
    #print "POINT 1: %d %d %d POINT 2:  %d %d %d DISTANCE: %d" % (x1, y1, z1, x2, y2, z2, result)
    return result

def printFrameInfo(frame):
    frame = frame
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['metacarpal', 'proximal', 'intermediate', 'distal']
        
    for hand in frame.hands:
        
        handType = "left_Hand" if hand.is_left else "rightHand"
        
        print "\b%s_position %f %f %f\b" % (
                                      handType, hand.palm_position.x, hand.palm_position.y, hand.palm_position.z )

        # Get fingers
        for finger in hand.fingers:
            
            fingerName = finger_names[finger.type]
            
            # Get bones
            for b in range(0, 4):
                bone = finger.bone(b)
                print "%s_%s %f %f %f" % (
                                    fingerName,          bone_names[bone.type],
                                    bone.next_joint.x, bone.next_joint.y, bone.next_joint.z )
        
        if not (frame.hands.is_empty):
            print ""

class SampleListener(Leap.Listener):
    finger_names = ['T', 'I', 'M', 'R', 'P']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal  ']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    first = False
    firstFrameId = 0
    mostRecentFrameId = 0
    
    
    def on_init(self, controller):
        print "Initialized"
        self.first = True
        self.firstFrameId = 0
        self.mostRecentFrameId = 0
    
    
    
    def on_connect(self, controller):
        print "Controller Connected"
        print "Press d to record a letter"
        
        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
    
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"
    
    #def on_exit(self, controller):
        #print("First  frame: " + str(self.firstFrameId) + "\n")
        #self.printFrameInfo(self.firstFrameId)
        #print("Most recent frame: " + str(self.mostRecentFrameId))
       # self.printFrameInfo(self.mostRecentFrameId)
        #print "PAUSED"
    
    def on_frame(self, controller):
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
        #if this is the first frame in this recording session, save this
        if (self.first):
            print("")
            self.first = False
            self.firstFrameId = frame
        else:
            self.mostRecentFrameId = frame
            #print("Most recent frame: " + str(self.mostRecentFrameId))
            #self.printFrameInfo(self.mostRecentFrameId)


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"
            
        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"
        
        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"
            
        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"



def main():
    paused = False
    recording = False
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    frame1 = 0
    frame2 = 0
    userName = ""
    leftorRight = ""
    viewpoint = ""
       
    # Keep this process running until Enter is pressed
    #frame2 = controller.frame()
    try:
        
        #Information to Make Folders
        userName = raw_input('Enter Name: ')
        leftorRight = raw_input('Left or Right Hand? ')
        viewpoint = raw_input('Is Controller Above or Below? ')
                            
        path = os.getcwd()
        
        #makes LetterData directory if it exists
        try:
            os.mkdir("LetterData")
        except OSError:
            pass
        
        os.chdir(path + "\\LetterData")
        
        print "Press r to begin."
    
        ch = getch()
        while(True):#not(ch == "q")):
           
            if (ch == "r" and not recording):
                print("Hit p to pause. Hit q to quit")
                #letter = raw_input("What letter? ")
                recording = True
            
            if (ch == "p"):
                print("Hit r to resume.")
                paused = True
                controller.remove_listener(listener)
                recording = False
                
            if (ch == "d" and  recording):
                frame1 = frame2;
                letter = raw_input("What letter are you signing?(You must sign the letter as you press Enter) ")
                
                if ('j' in letter or 'J' in letter or 'z' in letter or 'Z' in letter):
                   print("Sorry we don't how to record those letters yet!")
                   letter = letter + "not"
                   
                #checks if directory exists, if not makes it
                if (not(os.path.exists(letter+'\\'+viewpoint+'\\'+leftorRight))): #+'\\'+userName))):
                    os.makedirs(letter+'\\'+viewpoint+'\\'+leftorRight+'\\')
                
                newPath = '\\LetterData\\' + letter +'\\'+viewpoint+'\\'+leftorRight     #+'\\'+userName
                   
                recording = False
                
                #changes directory to save file in correct space
                os.chdir(path + newPath)
                
                #holds time/date
                now = datetime.now()
                dt = now.strftime("%b, %d %Y %I:%M:%S %p")
                 
                #Checks if file exists called userName1 if it does exist, it makes file called userName2 and so on.
                i = 1
                while (True):
                    if (os.path.isfile(userName + str(i) +".txt")):
                        i = i+1
                    else: 
                        fileName = userName + str(i) +".txt"
                        break;
                
                #creates/open filewith that name and writes into it instead of console
                f = open(fileName, "w")
                orig_stdout = sys.stdout 
                sys.stdout = f
                
                print(userName + "\nLeft/Right: " + leftorRight + "\nController View: " + viewpoint + "\n" + dt + "\n")
         
                #takes most recent frame and prints it out
                print("Data for: " + letter)   
                frame2 = controller.frame()
                printFrameInfo(frame2)
                
                #prints out to console and closes file
                sys.stdout = orig_stdout 
                f.close()
                                
                recording = True

                #lets user know data has been printed
                print "Data for " + letter + " recorded to " + newPath + "\\" + fileName +"\n"
                print "Press d to record another letter or q to quit"
                
                #changes os directory to original
                os.chdir(path + "\\LetterData")
            
            if (recording):
                controller.add_listener(listener)
            
            if (ch=='q'):
                print "Goodbye!"
                break;

            ch = getch()
        recording = False

    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)




if __name__ == "__main__":
   main()
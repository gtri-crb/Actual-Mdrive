# File: motorman.py
import tkFont
from Tkinter import *
import time 
#excerpt of code from TCP connection
#imports
import select
from MDrive import *
import socket
import time

#TCP connection

#initialization                                             ##########
mdrive = MDrive()
TCP_IP = "192.168.2.50"
TCP_PORT = 503
BUFFER_SIZE = 20
#motor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#motor.connect((TCP_IP,TCP_PORT))

class App:

#add motor.close() or something
#commands
    L1i = ""
    L1o = ""
    L2i = ""
    L2o = ""
    L3i = ""
    L3o = ""
    nothing = ""
    currentLine = 1
    
    
    def onExit(self):
        sys.exit ()

    def getPosition(self):                                                     ##########
        motor.send(mdrive.getPosition())
        data = motor.recv(1024)
        print data
        
    def getVelocity(self):
        motor.send(mdrive.getVelocity())
        data = motor.recv(1024)
        print data
        
    def getAcceleration(self):                                                     ##########
        motor.send(mdrive.getAcceleration())
        data = motor.recv(4096)
        print data
        
    def makeCredits(self):
        print "Pranav Shenoy\nTejas Khorana"

#note: empty string containers are false

    def getOutput(self): ################################################################################
        motor.send(self.myInputEntry.get())
        motor.send("\r\n")
            
        if (self.currentLine >= 4) :
            self.L1o = self.L2o
            self.L1i = self.L2i
            self.L2o = self.L3o
            self.L2i = self.L3i
            self.currentLine = 3
    
        if (self.currentLine == 1):
            self.L1i = "> " + self.myInputEntry.get()
        elif (self.currentLine == 2):
            self.L2i = "> " + self.myInputEntry.get()
        elif (self.currentLine == 3):
            self.L3i = "> " + self.myInputEntry.get()
        
        
        motor.settimeout(0.5)
        data = " "
        try:                                   # uncertain about da trycatch
            data = motor.recv(4096)
        except Exception:
            pass
            
        if data :
            self.myOutput.configure(text = data)
            if (self.currentLine ==1):                
                    self.L1o = " " + data
            elif (self.currentLine == 2):
                    self.L2o = " " + data
            elif (self.currentLine == 3):
                    self.L3o = " " + data
            
        else :
            self.myOutput.configure(text = self.nothing)

        textToDisplay = self.L1i + "\r\n" + self.L1o + "\r\n" + self.L2i + "\r\n" + self.L2o + "\r\n" + self.L3i + "\r\n" + self.L3o
        self.myPreviousCommands.configure(text = textToDisplay)

        self.currentLine = self.currentLine + 1;

        

    def moveDistance(self):
        if self.accelEntry.get():
            motor.send(mdrive.changeAcceleration())
        if self.decelEntry.get():
            motor.send(mdrive.changeDeceleration())
        if self.ivEntry.get(): 
            motor.send(mdrive.changeInitialVelocity())
        if self.mvEntry.get(): 
            motor.send(mdrive.changeMaximumVelocity())
        time.sleep(1)
        if self.moveEntry.get():
            motor.send(mdrive.moveAmount())
        
    def moveConstSpeed(self):
        if self.accelEntry.get():
            motor.send(mdrive.changeAcceleration())
        if self.decelEntry.get():
            motor.send(mdrive.changeDeceleration())
        if self.ivEntry.get(): 
            motor.send(mdrive.changeInitialVelocity())
        if self.mvEntry.get(): 
            motor.send(mdrive.changeMaximumVelocity())
        if self.constVelocityEntry.get():
            motor.send(mdrive.moveConstantSpeed())
            
#    def changeAccel(self):
#        motor.send(mdrive.changeAcceleration(int(self.accelEntry.get())))
#        
#    def changeDecel(self):
#        motor.send(mdrive.changeDeceleration(int(self.decelEntry.get())))
#
#
#    def changeIV(self):
#        motor.send(mdrive.changeInitialVelocity(int(self.ivEntry.get())))
#
#        
#    def changeMV(self):
#        motor.send(mdrive.changeMaximumVelocity(int(self.mvEntry.get())))
#
#

        
    def stop(self):
        motor.send(mdrive.stop())
        print "stopped"

        
#    def generateUnitChoices(event):
#         try:
#            popup.tk_popup(event.x_root, event.y_root, 0)
#         finally:
#            popup.grab_release()




        
    def makeInstructions(self):
        print "Set the properties:\n\tforward\\backward\n\tacceleration"
        print "\tdeceleration\n\tinitial velocity\n\tmax velocity"
        print "\nIf you do not set property values, the default value will be used."
        print "\nAfter setting the properties, you can use commands."
        print "\nMove Distance moves for a certain amount of rotations."
        print "\nMove Constant moves for a indefinite amount of time."
        print "\nYou can stop either Move Distance or Move Constant at any time with Stop."
        print "\nThe Undo command reverses the last command exactly opposite to how it was executed."
        print "\nProperty Presets are loaded by clicking one of the preset buttons but only if Load is selected."
        print "\nProperty Presets are saved by clicking Save and then clicking on the preset number to save to."


#initialization
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()


        #Fonts
        boldTitle = tkFont.Font(underline=1,size=12,family="Cour+ier")
        font2=tkFont.Font(family="Courier", size=9)
        font3=tkFont.Font(family="Courier", size=30, weight = "bold")

        
        #Menu
        menubar = Menu(frame.master)
        frame.master.config(menu=menubar)

        #File
        filemenu = Menu(menubar)
        filemenu.add_command(label="Exit", command=self.onExit)
        filemenu.add_command(label="Info", command = self.makeCredits)
 #      filemenu.add_command(label="Units", command = self.generateUnitChoices)
        filemenu.add_command(label="Save State")
        filemenu.add_command(label="Open State")
        filemenu.add_command(label="Workbook")
        filemenu.add_command(label="Scale Factor")
        filemenu.add_command(label="Bounds")
        menubar.add_cascade(label="File", menu=filemenu)




        #Help
        helpmenu = Menu(menubar)
        helpmenu.add_command(label="Instructions", command=self.makeInstructions)
        menubar.add_cascade (label="Help", menu=helpmenu)

        #Commands
        self.command = Label(frame, text="Commands", font=boldTitle)
        self.command.grid(row=0, ipady=10)
        

    
        self.moveScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.moveScale.grid(row=1, column=1)

        self.moveEntry = Entry(frame)
        self.moveEntry.grid(row=1, column=2)
        
        #move distance
        self.moveButton = Button(frame, text="Move Distance", fg="blue", font=font2, command=self.moveDistance)
        self.moveButton.grid(row=1)

        self.moveLabel = Label(frame, text="rotations", font=font2)
        self.moveLabel.grid(row=1, column = 3)

        #move at constant speed
        self.constVelocityButton = Button(frame, text="Move Constant", fg="blue", font=font2, command =self.moveConstSpeed)
        self.constVelocityButton.grid(row=3)
    
        self.constVelocityScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.constVelocityScale.grid(row=3, column=1)

        self.constVelocityEntry = Entry(frame)
        self.constVelocityEntry.grid(row=3, column=2)
        
        self.velocityLabel = Label(frame, text="rotations/second", font=font2)
        self.velocityLabel.grid(row =3, column = 3)
        
        #properties
        self.moveLabel = Label(frame, text="Properties",  font=boldTitle)
        self.moveLabel.grid(row=0, column = 4, ipady = 10)

        #forward/backward
        var = IntVar()
        self.forward = Radiobutton(frame, text="Forward", variable = var, var = 1)
        self.forward.grid(row=1,column=4)
        self.forward.select()
        self.backward = Radiobutton(frame, text="Backward", variable = var, var = -1)
        self.backward.grid(row=1,column=5)
        
        #acceleration
        self.accel = Button(frame, text="Acceleration", fg="blue", font=font2, command = self.getAcceleration)
        self.accel.grid(row=2, column=4)
    
        self.accelScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.accelScale.grid(row=2, column=5)

        self.accelEntry = Entry(frame)
        self.accelEntry.grid(row=2, column=6)
        
        self.accelLabel = Label(frame, text="rotations/second^2", font=font2)
        self.accelLabel.grid(row=2, column = 7)

        #move deceleration
        self.decelButton = Button(frame, text="Deceleration", fg="blue", font=font2, activebackground="purple")
        self.decelButton.grid(row=3, column = 4)
#        self.decelButton.config(text="Deceleration")
        self.decelButton.flash()
    
        self.decelScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.decelScale.grid(row=3, column=5)

        self.decelEntry = Entry(frame)
        self.decelEntry.grid(row=3, column=6)
        
        self.decelLabel = Label(frame, text="rotations/second^2", font=font2)
        self.decelLabel.grid(row=3, column = 7)


        #initial velocity
        self.ivButton = Button(frame, text="Initial Velocity", fg="blue", font=font2, command=self.getVelocity)
        self.ivButton.grid(row=4, column = 4)
    
        self.ivScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.ivScale.grid(row=4, column=5)

        self.ivEntry = Entry(frame)
        self.ivEntry.grid(row=4, column=6)
        
        self.ivLabel = Label(frame, text="rotations/second", font=font2)
        self.ivLabel.grid(row=4, column = 7)


        #max velocity
        self.mvButton = Button(frame, text="Max Velocity", fg="blue", font=font2)
        self.mvButton.grid(row=5, column = 4)
    
        self.mvScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        self.mvScale.grid(row=5, column=5)

        self.mvEntry = Entry(frame)
        self.mvEntry.grid(row=5, column=6)
        
        self.mvLabel = Label(frame, text="rotations/second", font=font2)
        self.mvLabel.grid(row =5, column = 7)


        #STOPBUTTON
        self.stopButton = Button(frame, text="STOP", fg="red", font=font3, width = 5, command=self.stop)
        self.stopButton.grid(row = 6, column = 1)

        #input,output, commandprompt esque 

        self.myInput = Label(frame, text="Input: ", font = font2)
        self.myInput.grid(row = 7, column = 4)
        self.myInputEntry = Entry(frame)
        self.myInputEntry.grid(row = 7, column = 5)
        self.enterInputButton = Button(frame, text="Enter", font = font2, command = self.getOutput)
        self.enterInputButton.grid(row = 7, column = 6)
        self.myOutput = Label(frame, text = "output", font = font2)   #### contains output in future
        self.myOutput.grid(row=8, column = 5)
        self.myPreviousCommands = Label(frame, text = "previouscomm", font = font2)  ### PREV COMM WILL CHANGE
        self.myPreviousCommands.grid(row = 6, column = 5)

        

        #get accel,position,velocity
        self.GAButton = Button(frame, text = "Get Acceleration", command = self.getAcceleration)
        self.GAButton.grid(row = 13, column = 5)
        self.GVButton = Button(frame, text = "Get Velocity", command = self.getVelocity)
        self.GVButton.grid(row = 13, column = 6)
        self.GPButton = Button(frame, text = "Get Position", command = self.getPosition)
        self.GPButton.grid(row = 13, column = 7)

        #presets
        self.moveLabel = Label(frame, text="Presets", font=boldTitle)
        self.moveLabel.grid(row=11, ipady=10)

        #save States
        self.oneButton = Button(frame, text="1", fg="darkgreen", width = 10, font=font2)
        self.oneButton.grid(row=12, ipady=5)

        self.twoButton = Button(frame, text="2",fg="darkgreen", width = 10, font=font2)
        self.twoButton.grid(row=12, column = 1, ipady=5)

        self.threeButton = Button(frame, text="3",fg="darkgreen", width = 10, font=font2)
        self.threeButton.grid(row=12, column = 2, ipady=5)

        self.fourButton = Button(frame, text="4",fg="darkgreen", width = 10, font=font2)
        self.fourButton.grid(row=12, column = 3, ipady=5)

        var_two = IntVar()
        self.Load = Radiobutton(frame, text="Load", variable = var_two, value = 1)
        self.Load.grid(row=13,column=1)
        self.Load.select()
        self.Save = Radiobutton(frame, text="Save", variable = var_two, value = 2)
        self.Save.grid(row=13,column=2, pady = 10)
        
root = Tk()

app = App(root)

root.wm_title("Motor Bro v. 2.7")

root.mainloop()

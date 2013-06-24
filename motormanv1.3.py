#File: motorman.py
import tkFont
import Tkinter
from Tkinter import *
import time 
#excerpt of code from TCP connection
#imports
import select
from MDrive import *
import socket

#TCP connection

#initialization                                             ##########
mdrive = MDrive()
TCP_IP = "192.168.2.50"
TCP_PORT = 503
BUFFER_SIZE = 20
#motor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#motor.connect((TCP_IP,TCP_PORT))

class App:

#commands
    L1i = ""
    L1o = ""
    L2i = ""
    L2o = ""
    L3i = ""
    L3o = ""
    nothing = ""
    currentLine = 1
    
    
        
#initialization
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
        self.boldTitleTwo = tkFont.Font(underline=1,size=12,family="Courier")
        self.myvar = StringVar()
        self.dirVar = 1
        self.toStepRatio = 3686500
        self.presetUsed = 0
        self.presetone = []
        self.presettwo = []
        self.presetthree = []
        self.presetfour = []
        self.presetorder = ["<direction>", "<acceleration>", "<deceleration>", "<initialvelocity>","<maximumvelocity>"]
        self.presetendorder = ["</direction>", "</acceleration>", "/deceleration>", "</initialvelocity>","</maximumvelocity>"]


        #Fonts
        self.units = "rotations"
        boldTitle = tkFont.Font(underline=1,size=12,family="Courier")
        font2=tkFont.Font(family="Courier", size=9)
        font3=tkFont.Font(family="Courier", size=30, weight = "bold")

        #make Commands section
        self.makeCommands(master,frame,boldTitle,font2)

        #make Properties section
        self.showProperties(master,frame,boldTitle,font2)
        
        #STOPBUTTON
        self.stopButton = Button(frame, text="STOP", fg="red", font=font3, width = 5, command = self.stop)
        self.stopButton.grid(row = 6, column = 1)

        #make File Menu
        self.makeFileMenu(master,frame,boldTitle,font2)

        #make preset section
        self.showPresets(master,frame,boldTitle,font2)
        
        #input,output, commandprompt esque 

        self.myInput = Label(frame, text="Input: ", font = font2)
        self.myInput.grid(row = 7, column = 3)
        self.myInputEntry = Entry(frame)
        self.myInputEntry.grid(row = 7, column = 4)
        self.enterInputButton = Button(frame, text="Enter", font = font2, command = self.getOutput)
        self.enterInputButton.grid(row = 7, column = 5)
        self.myOutput = Label(frame, text = "output", font = font2)   #### contains output in future
        self.myOutput.grid(row=8, column = 4)
        self.myPreviousCommands = Label(frame, text = "previouscomm", font = font2)  ### PREV COMM WILL CHANGE
        self.myPreviousCommands.grid(row = 6, column = 4)

        #get accel,position,velocity
        self.GAButton = Button(frame, text = "Get Acceleration", command = self.getAcceleration)
        self.GAButton.grid(row = 13, column = 3)
        self.GVButton = Button(frame, text = "Get Velocity", command = self.getVelocity)
        self.GVButton.grid(row = 13, column = 4)
        self.GPButton = Button(frame, text = "Get Position", command = self.getPosition)
        self.GPButton.grid(row = 13, column = 5)


    def makeFileMenu(self,master,frame,boldTitle,font2):
        #Menu
        menubar = Menu(frame.master)
        frame.master.config(menu=menubar)
        #File
        filemenu = Menu(menubar)
        filemenu.add_command(label="Exit", command=self.onExit)
        filemenu.add_command(label="Info", command = self.makeCredits)

        filemenu.add_command(label="Save", command = self.saveFile)
        filemenu.add_command(label="Save State", command = self.saveasFile)
        filemenu.add_command(label="Open State", command = self.openFile)
        filemenu.add_command(label="Workbook")
        menubar.add_cascade(label="File", menu=filemenu)
        #Edit
        editmenu = Menu(menubar)
        units = Menu(editmenu)
        units.add_command(label="Rotations",command=self.setUnitRotation)
        units.add_command(label="Degrees",command=self.setUnitDegrees)
        units.add_command(label="Steps",command=self.setUnitSteps)
        editmenu.add_cascade(label="Units",menu=units)
        editmenu.add_command(label="Properties",command=self.editProperties)
        editmenu.add_command(label="Presets",command=self.editPresets)
        editmenu.add_command(label="Scale Factor",command=self.editScaleFactor)
        editmenu.add_command(label="Bounds",command=self.editBounds)
        menubar.add_cascade(label="Edit", menu=editmenu) 
        #Help
        helpmenu = Menu(menubar)
        helpmenu.add_command(label="Instructions", command=self.makeInstructions)
        menubar.add_cascade (label="Help", menu=helpmenu)



        
    #sets the units as rotations
    def setUnitRotation(self):

        self.units = "rotations"
        self.moveLabel.configure(text=self.units)
        self.Acceleration.configure(text="Acceleration: " + str(float(mdrive.acceleration) / self.toStepRatio) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(float(mdrive.deceleration) / self.toStepRatio) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(float(mdrive.initialVelocity) / self.toStepRatio)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(float(mdrive.maximumVelocity) / self.toStepRatio)+ " " + self.units+"/second^2")
        self.velocityLabel.configure(text=self.units+"/sec")
        #self.accelLabel.configure(text=self.units+"/sec^2")
        #self.decelLabel.configure(text=self.units+"/sec^2")
        #self.ivLabel.configure(text=self.units+"/sec")
        #self.mvLabel.configure(text=self.units+"/sec")

    #sets the units as degrees
    def setUnitDegrees(self):

        self.units = "  degrees"
        self.moveLabel.configure(text=self.units)
        self.Acceleration.configure(text="Acceleration: " + str(float(mdrive.acceleration) / self.toStepRatio * 360) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(float(mdrive.deceleration) / self.toStepRatio * 360) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(float(mdrive.initialVelocity) / self.toStepRatio * 360)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(float(mdrive.maximumVelocity) / self.toStepRatio * 360) + " " + self.units+"/second^2")
        self.velocityLabel.configure(text=self.units+"/sec")
        #self.accelLabel.configure(text=self.units+"/sec^2")
        #self.decelLabel.configure(text=self.units+"/sec^2")
        #self.ivLabel.configure(text=self.units+"/sec")
        #self.mvLabel.configure(text=self.units+"/sec")
        self.updateAllUnits

    #sets the units as steps
    def setUnitSteps(self):

        self.units = "    steps"
        self.moveLabel.configure(text=self.units)
        self.Acceleration.configure(text="Acceleration: " + str(mdrive.acceleration) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(mdrive.deceleration) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(mdrive.initialVelocity)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(mdrive.maximumVelocity)+ " " + self.units+"/second^2")
        self.velocityLabel.configure(text=self.units+"/sec")
        #self.accelLabel.configure(text=self.units+"/sec^2")
        #self.decelLabel.configure(text=self.units+"/sec^2")
        #self.ivLabel.configure(text=self.units+"/sec")
        #self.mvLabel.configure(text=self.units+"/sec")
        self.updateAllUnits

    def updateAllUnits(self):
        self.moveLabel.configure(text=self.units)
        self.velocityLabel.configure(text=self.units+"/sec")
        self.accelLabel.configure(text=self.units+"/sec^2")
        self.decelLabel.configure(text=self.units+"/sec^2")
        self.ivLabel.configure(text=self.units+"/sec")
        self.mvLabel.configure(text=self.units+"/sec")

    #used for converting between units

    def getConversionFactor(self):
        if self.units == "rotations":
            conversionFactor = self.toStepRatio
        if self.units == "  degrees":
            conversionFactor = self.toStepRatio/360
        if self.units == "    steps":
            conversionFactor = 1
        return conversionFactor

    def makeCommands(self,master,frame,boldTitle,font2):
        #Commands
        command = Label(frame, text="Commands", font=boldTitle)
        command.grid(row=0, ipady=10)
        
        #move distance
        moveButton = Button(frame, text="Move Distance", fg="blue", font=font2, command=self.moveDistance)
        moveButton.grid(row=1)

        self.moveValue = IntVar()
        moveScale = Scale(frame, from_=0, to=1800, variable = self.moveValue, orient=HORIZONTAL, length = 130)
        moveScale.grid(row=1, column=1)

        self.moveEntry = Entry(frame, textvariable = self.moveValue) 
        self.moveEntry.grid(row=1, column=2)

        self.moveLabel = Label(frame, text=self.units, font=font2)
        self.moveLabel.grid(row=1, column = 3)

        #move at constant speed

        constVelocityButton = Button(frame, text="Move Constant", fg="blue", font=font2, command =self.moveConstSpeed)
        constVelocityButton.grid(row=3)
    
        self.velValue = IntVar()
        constVelocityScale = Scale(frame, from_=0, to=1800, variable = self.velValue, orient=HORIZONTAL, length = 130)
        constVelocityScale.grid(row=3, column=1)

        self.constVelocityEntry = Entry(frame, textvariable = self.velValue)
        self.constVelocityEntry.grid(row=3, column=2)
        
        self.velocityLabel = Label(frame, text=self.units+"/sec", font=font2)
        self.velocityLabel.grid(row =3, column = 3)

    def editProperties(self):
        self.proptop = Tk()
        self.proptop.title("Edit Properties")
        self.proptop.geometry("500x300")
        #properties
        self.prperties = Label(self.proptop, text="Properties")
        self.prperties.grid(row=0, column = 0, ipady = 10)

        #forward/backward

        forward = Radiobutton(self.proptop, text="Forward", variable = self.dirVar, value = 1, command = lambda: self.setDirVar(1))
        forward.grid(row=1,column=0)
        backward = Radiobutton(self.proptop, text="Backward", variable = self.dirVar, value = 2, command = lambda: self.setDirVar(-1))
        backward.grid(row=1,column=1)

        
        
        self.myvardecel = StringVar()
        self.myvarivelocity = StringVar()
        self.myvarmvelocity = StringVar()
        #acceleration
        accel = Label(self.proptop, text="Acceleration", fg="blue")
        accel.grid(row=2, column=0)
    
        self.accVar = IntVar()        
        self.accelEntry = Entry(self.proptop,textvariable=self.accVar)
        self.accelEntry.grid(row=2, column=2)


        accelScale = Scale(self.proptop, from_=0, to=1800, orient=HORIZONTAL, length = 130,variable=self.accVar)
        accelScale.grid(row=2, column=1)



        self.accelLabel = Label(self.proptop, text=self.units+"/second^2")
        self.accelLabel.grid(row=2, column = 3)

        #move deceleration
        decel = Label(self.proptop, text="Deceleration", fg="blue", activebackground="purple")
        decel.grid(row=3, column = 0)

        self.decVar = IntVar()
        decelScale = Scale(self.proptop, from_=0, to=1800, variable = self.decVar, orient=HORIZONTAL, length = 130)
        decelScale.grid(row=3, column=1)

        self.decelEntry = Entry(self.proptop, textvariable = self.decVar)
        self.decelEntry.grid(row=3, column=2)
        
        self.decelLabel = Label(self.proptop, text=self.units+"/second^2")
        self.decelLabel.grid(row=3, column = 3)


        #initial velocity
        ivButton = Label(self.proptop, text="Initial Velocity", fg="blue")
        ivButton.grid(row=4, column = 0)
    
        self.ivVar = IntVar()
        ivScale = Scale(self.proptop, from_=0, to=1800, variable = self.ivVar, orient=HORIZONTAL, length = 130)
        ivScale.grid(row=4, column=1)


        self.ivEntry = Entry(self.proptop, textvariable = self.ivVar)
        self.ivEntry.grid(row=4, column=2)
        
        self.ivLabel = Label(self.proptop, text=self.units+"/second")
        self.ivLabel.grid(row=4, column = 3)


        #max velocity
        mv = Label(self.proptop, text="Max Velocity", fg="blue")
        mv.grid(row=5, column = 0)

        self.mvVar = IntVar()
        mvScale = Scale(self.proptop, from_=0, to=1800, variable = self.mvVar, orient=HORIZONTAL, length = 130)
        mvScale.grid(row=5, column=1)


        self.mvEntry = Entry(self.proptop, textvariable = self.mvVar)
        self.mvEntry.grid(row=5, column=2)
        
        self.mvLabel = Label(self.proptop, text=self.units+"/second")
        self.mvLabel.grid(row =5, column = 3)

        spacer = Label(self.proptop, text = " ")
        spacer.grid(row=6)
        
        okayButton = Button(self.proptop, text="All done", fg = "blue", command=self.setValues, width = 10)
        okayButton.grid(row=7,column = 1)


    def setValues(self):

        conversionFactor = self.getConversionFactor()

        if self.accelEntry.get():
            mdrive.acceleration = int (float(self.accelEntry.get())*conversionFactor)
        if self.decelEntry.get():
            mdrive.deceleration = int (float(self.decelEntry.get())*conversionFactor)
        if self.ivEntry.get():
            mdrive.initialVelocity = int (float(self.ivEntry.get())*conversionFactor)
        if self.mvEntry.get():
            mdrive.maximumVelocity = int (float(self.mvEntry.get())*conversionFactor)
        self.Acceleration.configure(text="Acceleration: " + str(float(mdrive.acceleration)/conversionFactor) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(float(mdrive.deceleration)/conversionFactor) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(float(mdrive.initialVelocity)/conversionFactor)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(float(mdrive.maximumVelocity)/conversionFactor)+ " " + self.units+"/second^2")
        self.proptop.destroy()


    def setDirVar(self, value):
        self.dirVar = value

    def updateThings(self):

        
        if (self.units == "rotations"):
            self.setUnitRotation()
            print "rot"
        if (self.units == "  degrees"):
            self.setUnitDegrees()
            print "deg"
        if (self.units == "    steps"):
            self.setUnitSteps()
            print "step"

    def editPresets(self):
        self.prestop = Tkinter.Tk()
        self.prestop.title("Edit Presets")
        self.prestop.geometry("350x180")
        #presets
        moveLabel = Label(self.prestop, text="Presets",justify=RIGHT)
        moveLabel.grid(row=10, column = 0,ipady=10)
        #save States
        oneButton = Button(self.prestop, text="1", fg="darkgreen", width = 10,command = self.PresetOneCom)
        oneButton.grid(row=11, ipady=5)

        twoButton = Button(self.prestop, text="2",fg="darkgreen", width = 10,command = self.PresetTwoCom)
        twoButton.grid(row=11, column = 1, ipady=5)

        threeButton = Button(self.prestop, text="3",fg="darkgreen", width = 10,command = self.PresetThreeCom)
        threeButton.grid(row=11, column = 2, ipady=5)

        fourButton = Button(self.prestop, text="4",fg="darkgreen", width = 10,command = self.PresetFourCom)
        fourButton.grid(row=11, column = 3, ipady=5)

        self.var_two = IntVar()
        self.LoadorSave = True
        self.Load = Radiobutton(self.prestop, text="Load", variable=self.var_two, value=1, command=self.setLoad)
        self.Load.grid(row=12,column=1)
        self.Load.select()
        self.Save = Radiobutton(self.prestop, text="Save", variable=self.var_two, value=2, command=self.setSave)
        self.Save.grid(row=12,column=2)
        print self
        okayButton = Button(self.prestop, text="All done", fg = "blue", command=self.closepresets, width = 10)
        okayButton.grid(row=13,column = 1)


    def setLoad(self):
        self.LoadorSave = True

    def setSave(self):
        self.LoadorSave = False

    def PresetOneCom(self):
        if self.LoadorSave == True:
            self.presetUsed = 1
            self.presets.configure(text="preset number: " + str(self.presetUsed))
            mdrive.acceleration = self.presetone[1]
            mdrive.deceleration = self.presetone[2]
            mdrive.initialVelocity = self.presetone[3]
            mdrive.maximumVelocity = self.presetone[4]
        if (self.units == "rotations"):
            self.setUnitRotation()
        if (self.units == "  degrees"):
            self.setUnitDegrees()
        if (self.units == "    steps"):
            self.setUnitSteps()
        if self.LoadorSave == False:
           self.presetone = [self.dirVar,mdrive.acceleration,mdrive.deceleration,mdrive.initialVelocity,mdrive.maximumVelocity]


    
    def PresetTwoCom(self):
        if self.LoadorSave == True:
            self.presetUsed = 2
            self.presets.configure(text="preset number: " + str(self.presetUsed))
            mdrive.acceleration = self.presettwo[1]
            mdrive.deceleration = self.presettwo[2]
            mdrive.initialVelocity = self.presettwo[3]
            mdrive.maximumVelocity = self.presettwo[4]
        if (self.units == "rotations"):
            self.setUnitRotation()
        if (self.units == "  degrees"):
            self.setUnitDegrees()
        if (self.units == "    steps"):
            self.setUnitSteps()
        if self.LoadorSave == False:
            self.presettwo = [self.dirVar,mdrive.acceleration,mdrive.deceleration,mdrive.initialVelocity,mdrive.maximumVelocity]
    

    def PresetThreeCom(self):
        if self.LoadorSave == True:
            self.presetUsed = 3
            self.presets.configure(text="preset number: " + str(self.presetUsed))
            mdrive.acceleration = self.presetthree[1]
            mdrive.deceleration = self.presetthree[2]
            mdrive.initialVelocity = self.presetthree[3]
            mdrive.maximumVelocity = self.presetthree[4]
        if (self.units == "rotations"):
            self.setUnitRotation()
        if (self.units == "  degrees"):
            self.setUnitDegrees()
        if (self.units == "    steps"):
            self.setUnitSteps()
        if self.LoadorSave == False:
            self.presetthree = [self.dirVar,mdrive.acceleration,mdrive.deceleration,mdrive.initialVelocity,mdrive.maximumVelocity]

    
    def PresetFourCom(self):
        if self.LoadorSave == True:
            self.presetUsed = 4
            self.presets.configure(text="preset number: " + str(self.presetUsed))
            mdrive.acceleration = self.presetfour[1]
            mdrive.deceleration = self.presetfour[2]
            mdrive.initialVelocity = self.presetfour[3]
            mdrive.maximumVelocity = self.presetfour[4]
        if (self.units == "rotations"):
            self.setUnitRotation()
        if (self.units == "  degrees"):
            self.setUnitDegrees()
        if (self.units == "    steps"):
            self.setUnitSteps()
        if self.LoadorSave == False:
            self.presetfour = [self.dirVar,mdrive.acceleration,mdrive.deceleration,mdrive.initialVelocity,mdrive.maximumVelocity]

    

    def closepresets(self):
        self.prestop.destroy()

    def editScaleFactor(self):
        self.scaletop = Tkinter.Tk()
        self.scaletop.title("Edit Scale Factor")
        self.scaletop.geometry("400x100")

        #Scale Factor
        moveLabel = Label(self.scaletop, text="Scale Factor", font=self.boldTitleTwo)
        moveLabel.grid(row=1, column=0, ipady=10)

        self.stepsEntry = Entry(self.scaletop)
        self.stepsEntry.grid(row=2, column=0)
        stepsLabel = Label(self.scaletop, text="steps = ")
        stepsLabel.grid(row=2, column=1)
        self.rotationsEntry = Entry(self.scaletop)
        self.rotationsEntry.grid(row=2,column=2)
        rotationsLabel = Label(self.scaletop, text="rotations")
        rotationsLabel.grid(row=2, column=3)

        okayButton = Button(self.scaletop, text="All done", fg = "blue", command=self.closeScale, width = 10)
        okayButton.grid(row=3,column = 1)



    def closeScale(self):
        if self.stepsEntry.get() and self.rotationsEntry.get():
            self.toStepRatio = float (self.stepsEntry.get())/float (self.rotationsEntry.get())
            self.updateThings()

        self.scaletop.destroy()

    def editBounds(self):
        self.boundtop = Tkinter.Tk()
        self.boundtop.title("Edit Bounds")
        self.boundtop.geometry("500x100")

        boundstitle = Label(self.boundtop, text="Bounds",font=self.boldTitleTwo)
        boundstitle.grid(row=1,column=0)
        distanceminLabel = Label(self.boundtop, text="distance minimum = ")
        distanceminLabel.grid(row=2, column=0)
        distanceminEntry = Entry(self.boundtop)
        distanceminEntry.grid(row=2, column=1)
        distancemaxLabel = Label(self.boundtop, text=" distance maximum = ")
        distancemaxLabel.grid(row=2, column=2)
        distancemaxEntry = Entry(self.boundtop)
        distancemaxEntry.grid(row=2,column=3)

        okayButton = Button(self.boundtop, text="All done", fg = "blue", command=self.closebounds, width = 10)
        okayButton.grid(row=3,column = 1)

    def closebounds(self):
        self.boundtop.destroy()

    def showProperties(self,master,frame,boldTitle,font2):
        #properties
        
        self.prperties = Label(frame, text="Properties",  font=boldTitle)
        self.prperties.grid(row=0, column = 4, ipady = 10)
        #forward/backwards
        self.Direction = Label(frame, text="Direction: ",  font=font2, justify=LEFT)
        self.Direction.grid(row=1, column = 4)
        #acceleration
        self.Acceleration = Label(frame, text="Acceleration: " + str(float(mdrive.acceleration)/self.toStepRatio) + " " + self.units + "/second^2",  font=font2,justify=LEFT)
        self.Acceleration.grid(row=2, column = 4)
        #deceleration
        self.Deceleration = Label(frame, text="Deceleration: "+ str(float(mdrive.deceleration)/self.toStepRatio) + " " + self.units+"/second^2",  font=font2,justify=LEFT)
        self.Deceleration.grid(row=3, column = 4)
        #initial velocity
        self.IVelocity = Label(frame, text="Initial velocity: " + str(float(mdrive.initialVelocity)/self.toStepRatio)+ " " + self.units+"/second\n",  font=font2,justify=LEFT)
        self.IVelocity.grid(row=4, column = 4)
        #max velocity
        self.MVelocity = Label(frame, text="Maximum velocity: "+ str(float (mdrive.maximumVelocity) / self.toStepRatio)+ " " + self.units+"/second^2",  font=font2,justify=LEFT)
        self.MVelocity.grid(row=5, column = 4)
        

    def showPresets(self,master,frame,boldTitle,font2):
        #presets
        moveLabel = Label(frame, text="Presets", font=boldTitle)
        moveLabel.grid(row=10, ipady=10)
        #value
        self.presets = Label(frame, text="preset number: " + str(self.presetUsed),  font=font2)
        self.presets.grid(row=11)

    
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

        
    def openFile(self):
        self.opentop = Tkinter.Tk()
        self.opentop.title("Open")
        self.opentop.geometry("200x120")

        orders = Label(self.opentop, text="Enter filename\n")
        orders.pack()

        self.myvar = StringVar(self.opentop)

        text_entry = Entry(self.opentop, textvariable=self.myvar)
        text_entry.pack()

        openButton = Button(self.opentop, text="Open",command=self.getFileCloseWindow)
        openButton.pack()

    def getFileCloseWindow(self,*args):
        print(self.myvar.get())
        self.opentop.destroy()

    def saveasFile(self):
        self.savetop = Tkinter.Tk()
        self.savetop.title("Save as") 
        self.savetop.geometry("200x120")

        orders = Label(self.savetop, text="Enter filepath\n")
        orderstwo = Label (self.savetop, text="starts in C:\\")
        orders.pack()
        orderstwo.pack()

        self.filepath = StringVar(self.savetop)
        
        openEntry = Entry(self.savetop, textvariable = self.filepath)
        openEntry.pack()

        saveButton = Button(self.savetop, text="Save",command=self.saveFileCloseWindow)
        saveButton.pack()

    def saveFileCloseWindow(self,*args):
        savestate = open(self.filepath.get(), 'w')
        print "writing file..... \n\n"
        savestate.write("<filepath>")
        savestate.write(self.filepath.get())
        savestate.write("</filepath>\n")
        #preset one
        i = 0
        savestate.write("<preset_one>\n")
        for i in range(0,len(self.presetone)):
            savestate.write(self.presetorder[i])
            savestate.write(str(self.presetone[i]))
            savestate.write(self.presetendorder[i])
            savestate.write('\n')
        savestate.write("</preset_one>")
        savestate.write("\n")
        #preset two
        i = 0
        savestate.write("<preset_two>\n")
        for i in range(0,len(self.presettwo)):
            savestate.write(self.presetorder[i])
            savestate.write(str(self.presettwo[i]))
            savestate.write(self.presetendorder[i])
            savestate.write('\n')
        savestate.write("</preset_two>")
        savestate.write("\n")
        #preset three
        i=0
        savestate.write("<preset_three>\n")
        for i in range(0,len(self.presetthree)):
            savestate.write(self.presetorder[i])
            savestate.write(str(self.presetthree[i]))
            savestate.write(self.presetorder[i])
            savestate.write('\n')
        savestate.write("</preset_three>")
        savestate.write("\n")
        #preset four
        i=0
        savestate.write("<preset_four>\n")
        for i in range(0,len(self.presetfour)):
            savestate.write(self.presetorder[i])
            savestate.write(str(self.presetfour[i]))
            savestate.write(self.presetorder[i])
            savestate.write('\n')
        savestate.write("</preset_four>")

        print "done"
        self.savetop.destroy()

    def saveFile(self): 
        if(~self.myvar.get()):
            saveasFile()
#        else:

    def onExit(self):
        motor.close()
        sys.exit ()

    def makeCredits(self):
        print "Pranav Shenoy\nTejas Khorana\nKevin Han"

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

    def moveDistance(self):
        motor.send(mdrive.changeAcceleration())
        motor.send(mdrive.changeDeceleration())
        motor.send(mdrive.changeInitialVelocity())
        motor.send(mdrive.changeMaximumVelocity())
        time.sleep(1)
        if self.moveEntry.get():
            motor.send(mdrive.moveAmount(self.dirVar * int(self.moveEntry.get())*self.getConversionFactor()))
            
        
    def moveConstSpeed(self):
        motor.send(mdrive.changeAcceleration())
        motor.send(mdrive.changeDeceleration())
        motor.send(mdrive.changeInitialVelocity())
        motor.send(mdrive.changeMaximumVelocity())
        time.sleep(1)
        if self.constVelocityEntry.get():
            motor.send(mdrive.moveConstantSpeed(self.dirVar * int(self.constVelocityEntry.get())*self.getConversionFactor()))

    def onExit(self):
        sys.exit ()

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

        self.masterReference = master
        frame = Frame(master)
        frame.pack()
        self.boldTitleTwo = tkFont.Font(underline=1,size=12,family="Courier")
        self.myvar = StringVar()
        self.dirVar = 1
        self.toStepRatio = 3686500
        self.presetone = []
        self.presettwo = []
        self.presetthree = []
        self.presetfour = []
        self.presetorder = ["<direction>", "<acceleration>", "<deceleration>", "<initialvelocity>","<maximumvelocity>"]
        self.presetendorder = ["</direction>", "</acceleration>", "/deceleration>", "</initialvelocity>","</maximumvelocity>"]

       
        #Fonts
        self.units = "rotations"
        boldTitle = tkFont.Font(underline=1,size=12,family="Courier")
        font2=tkFont.Font(family="Courier", size=9)
        font3=tkFont.Font(family="Courier", size=30, weight = "bold")

        
    def stop(self):
        motor.send(mdrive.stop())
        print "stopped"


root = Tk()

app = App(root)

root.wm_title("Motor Bro v. 2.7")

root.mainloop()

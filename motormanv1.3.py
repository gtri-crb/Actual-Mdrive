# File: motorman.py
import tkFont
from Tkinter import *
import Tkinter
from MDrive import *
import socket
import array
import time




#TCP connectio

#initialization                                             ##########
mdrive = MDrive()
#TCP_IP = "192.168.2.50"
#TCP_PORT = 503
#BUFFER_SIZE = 20
#motor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#motor.connect((TCP_IP,TCP_PORT))

class App:
    
    #Initialization
    mdrive = MDrive()
#    TCP_IP = "192.168.2.50"
#    TCP_PORT = 503
 #   BUFFER_SIZE = 20
    motor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #  motor.connect((TCP_IP,TCP_PORT))



    def __init__(self, master):

        self.masterReference = master
        self.presetone = []
        self.presettwo = []
        self.presetthree = []
        self.presetfour = []
        frame = Frame(master)
        frame.pack()
        self.boldTitleTwo = tkFont.Font(underline=1,size=12,family="Courier")
        self.myvar = StringVar()
        self.dirVar = 1
        self.toStepRatio = 3686500
        
        #Fonts
        self.units = "rotations"
        boldTitle = tkFont.Font(underline=1,size=12,family="Courier")
        font2=tkFont.Font(family="Courier", size=9)
        font3=tkFont.Font(family="Courier", size=30, weight = "bold")

        #make File Menu
        self.makeFileMenu(master,frame,boldTitle,font2)

        #make Commands section
        self.makeCommands(master,frame,boldTitle,font2)

        #make Properties section
        self.showProperties(master,frame,boldTitle,font2)
        
        #STOPBUTTON
        self.stopButton = Button(frame, text="STOP", fg="red", font=font3, width = 5)
        self.stopButton.grid(row = 6, column = 1)

        #make preset section
        self.showPresets(master,frame,boldTitle,font2)



    def makeFileMenu(self,master,frame,boldTitle,font2):
        #Menu
        menubar = Menu(frame.master)
        frame.master.config(menu=menubar)
        #File
        filemenu = Menu(menubar)
        filemenu.add_command(label="Exit", command=self.onExit)
        filemenu.add_command(label="Info", command = self.makeCredits)

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
        self.Acceleration.configure(text="Acceleration: " + str(float(self.mdrive.acceleration) / self.toStepRatio) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(float(self.mdrive.deceleration) / self.toStepRatio) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(float(self.mdrive.initialVelocity) / self.toStepRatio)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(float(self.mdrive.maximumVelocity) / self.toStepRatio)+ " " + self.units+"/second^2")
        self.velocityLabel.configure(text=self.units+"/sec")
        #self.accelLabel.configure(text=self.units+"/sec^2")
        #self.decelLabel.configure(text=self.units+"/sec^2")
        #self.ivLabel.configure(text=self.units+"/sec")
        #self.mvLabel.configure(text=self.units+"/sec")
        #self.updateAllUnits

    #sets the units as degrees
    def setUnitDegrees(self):
        self.units = "  degrees"
        self.moveLabel.configure(text=self.units)
        self.Acceleration.configure(text="Acceleration: " + str(float(self.mdrive.acceleration) / self.toStepRatio * 360) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(float(self.mdrive.deceleration) / self.toStepRatio * 360) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(float(self.mdrive.initialVelocity) / self.toStepRatio * 360)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(float(self.mdrive.maximumVelocity) / self.toStepRatio * 360) + " " + self.units+"/second^2")
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
        self.Acceleration.configure(text="Acceleration: " + str(self.mdrive.acceleration) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(self.mdrive.deceleration) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(self.mdrive.initialVelocity)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(self.mdrive.maximumVelocity)+ " " + self.units+"/second^2")
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
    
        moveScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        moveScale.grid(row=1, column=1)

        self.moveEntry = Entry(frame) 
        self.moveEntry.grid(row=1, column=2)

        self.moveLabel = Label(frame, text=self.units, font=font2)
        self.moveLabel.grid(row=1, column = 3)

        #move at constant speed
        constVelocityButton = Button(frame, text="Move Constant", fg="blue", font=font2, command =self.moveConstSpeed)
        constVelocityButton.grid(row=3)
    
        constVelocityScale = Scale(frame, from_=0, to=300, orient=HORIZONTAL, length = 130)
        constVelocityScale.grid(row=3, column=1)

        self.constVelocityEntry = Entry(frame)
        self.constVelocityEntry.grid(row=3, column=2)
        
        self.velocityLabel = Label(frame, text=self.units+"/sec", font=font2)
        self.velocityLabel.grid(row =3, column = 3)

    def mywarwritten(*args):
        print "mywarWritten", self.myvar.get()
    
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
        forward.select()
        backward = Radiobutton(self.proptop, text="Backward", variable = self.dirVar, value = 2, command = lambda: self.setDirVar(-1))
        backward.grid(row=1,column=1)

        print self.dirVar
        
        #acceleration
        accel = Label(self.proptop, text="Acceleration", fg="blue")
        accel.grid(row=2, column=0)
    
        self.myvar.trace("w", self.mywarWritten)
        self.myvar.set("20")
        self.accelEntry = Entry(self.proptop,textvariable=self.myvar)
        self.accelEntry.grid(row=2, column=2)

        accelScale = Scale(self.proptop, from_=0, to=300, orient=HORIZONTAL, length = 130,variable=10)
        number = 0
        if (self.myvar.get()):
            number = int(float(self.myvar.get()))
        accelScale.set(number)
        accelScale.grid(row=2, column=1)



        self.accelLabel = Label(self.proptop, text=self.units+"/second^2")
        self.accelLabel.grid(row=2, column = 3)

        #move deceleration
        decel = Label(self.proptop, text="Deceleration", fg="blue", activebackground="purple")
        decel.grid(row=3, column = 0)
    
        decelScale = Scale(self.proptop, from_=0, to=300, orient=HORIZONTAL, length = 130)
        decelScale.grid(row=3, column=1)

        
        self.decelEntry = Entry(self.proptop, textvariable=self.myvar)
        self.decelEntry.grid(row=3, column=2)
        
        self.decelLabel = Label(self.proptop, text=self.units+"/second^2")
        self.decelLabel.grid(row=3, column = 3)


        #initial velocity
        ivButton = Label(self.proptop, text="Initial Velocity", fg="blue")
        ivButton.grid(row=4, column = 0)
    
        ivScale = Scale(self.proptop, from_=0, to=300, orient=HORIZONTAL, length = 130)
        ivScale.grid(row=4, column=1)

        self.ivEntry = Entry(self.proptop)
        self.ivEntry.grid(row=4, column=2)
        
        self.ivLabel = Label(self.proptop, text=self.units+"/second")
        self.ivLabel.grid(row=4, column = 3)


        #max velocity
        mv = Label(self.proptop, text="Max Velocity", fg="blue")
        mv.grid(row=5, column = 0)
    
        mvScale = Scale(self.proptop, from_=0, to=300, orient=HORIZONTAL, length = 130)
        mvScale.grid(row=5, column=1)

        self.mvEntry = Entry(self.proptop)
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
            self.mdrive.acceleration = int (int(self.accelEntry.get())*conversionFactor)
        if self.decelEntry.get():
            self.mdrive.deceleration = int (int(self.decelEntry.get())*conversionFactor)
        if self.ivEntry.get():
            self.mdrive.initialVelocity = int (int(self.ivEntry.get())*conversionFactor)
        if self.mvEntry.get():
            self.mdrive.maximumVelocity = int (int(self.mvEntry.get())*conversionFactor)
        self.Acceleration.configure(text="Acceleration: " + str(self.mdrive.acceleration/conversionFactor) + " " + self.units + "/second^2")
        self.Deceleration.configure(text="Deceleration: "+ str(self.mdrive.deceleration/conversionFactor) + " " + self.units+"/second^2")
        self.IVelocity.configure(text="Initial velocity: " + str(self.mdrive.initialVelocity/conversionFactor)+ " " + self.units+"/second\n")
        self.MVelocity.configure(text="Maximum velocity: "+ str(self.mdrive.maximumVelocity/conversionFactor)+ " " + self.units+"/second^2")
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
        oneButton = Button(self.prestop, text="1", fg="darkgreen", width = 10,command = self.setPresetOne)
        oneButton.grid(row=11, ipady=5)

        twoButton = Button(self.prestop, text="2",fg="darkgreen", width = 10)
        twoButton.grid(row=11, column = 1, ipady=5)

        threeButton = Button(self.prestop, text="3",fg="darkgreen", width = 10)
        threeButton.grid(row=11, column = 2, ipady=5)

        fourButton = Button(self.prestop, text="4",fg="darkgreen", width = 10)
        fourButton.grid(row=11, column = 3, ipady=5)

        self.var_two = IntVar()
        self.Load = Radiobutton(self.prestop, text="Load", variable=self.var_two, value=1, command=setPresetOne)
        self.Load.grid(row=12,column=1)
        self.Load.select()
        self.Save = Radiobutton(self.prestop, text="Save", variable=self.var_two, value=2, command=self.setPresetOne)
        self.Save.grid(row=12,column=2)
        print self
        print var_two.get()
        okayButton = Button(self.prestop, text="All done", fg = "blue", command=self.closepresets, width = 10)
        okayButton.grid(row=13,column = 1)

    def setPresetOne(self):
        if (self.var_two.get() == 1):
            self.presetone = [self.mdrive.acceleration, self.mdrive.deceleration,self.mdrive.initialVelocity,self.mdrive.maximumVelocity]
            print "self.awesome"
        else:
            print "self.other"


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
        self.Acceleration = Label(frame, text="Acceleration: " + str(float(self.mdrive.acceleration)/self.toStepRatio) + " " + self.units + "/second^2",  font=font2,justify=LEFT)
        self.Acceleration.grid(row=2, column = 4)
        #deceleration
        self.Deceleration = Label(frame, text="Deceleration: "+ str(float(self.mdrive.deceleration)/self.toStepRatio) + " " + self.units+"/second^2",  font=font2,justify=LEFT)
        self.Deceleration.grid(row=3, column = 4)
        #initial velocity
        self.IVelocity = Label(frame, text="Initial velocity: " + str(float(self.mdrive.initialVelocity)/self.toStepRatio)+ " " + self.units+"/second\n",  font=font2,justify=LEFT)
        self.IVelocity.grid(row=4, column = 4)
        #max velocity
        self.MVelocity = Label(frame, text="Maximum velocity: "+ str(float (self.mdrive.maximumVelocity) / self.toStepRatio)+ " " + self.units+"/second^2",  font=font2,justify=LEFT)
        self.MVelocity.grid(row=5, column = 4)
        

    def showPresets(self,master,frame,boldTitle,font2):
        #presets
        moveLabel = Label(frame, text="Presets", font=boldTitle)
        moveLabel.grid(row=10, ipady=10)
        #value
        self.presets = Label(frame, text="preset number: ",  font=font2)
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

    def mywarWritten(self,*args):
        print "mywarWritten",self.myvar.get()

    def saveasFile(self):
        self.savetop = Tkinter.Tk()
        self.savetop.title("Save as") 
        self.savetop.geometry("200x120")

        orders = Label(self.savetop, text="Enter filename\n")
        orders.pack()

        self.var = StringVar(self.savetop)
        
        openEntry = Entry(self.savetop, textvariable = self.var)
        openEntry.pack()

        saveButton = Button(self.savetop, text="Save",command=self.saveFileCloseWindow)
        saveButton.pack()

    def saveFileCloseWindow(self,*args):
        print(self.myvar.get())
        self.savetop.destroy()

    def saveFile(self): 
        if(self.myvar.get() == null):
            saveasFile()
#        else:

    def onExit(self):
        self.motor.close()
        sys.exit ()

    def makeCredits(self):
        print "Pranav Shenoy\nTejas Khorana"

    def getPosition(self):
        self.motor.send(mdrive.getPosition())
        print self.motor.listen()
        
    def getVelocity(self):
        self.motor.send(mdrive.getVelocity())
        print self.motor.listen()
        
    def getAcceleration(self):
        self.motor.send(mdrive.getAcceleration())
        print self.motor.listen()

    def moveDistance(self):

        
        self.motor.send(mdrive.changeAcceleration())
        self.motor.send(mdrive.changeDeceleration())
        self.motor.send(mdrive.changeInitialVelocity())
        self.motor.send(mdrive.changeMaximumVelocity())
        time.sleep(1)
        if self.moveEntry.get():
            self.motor.send(mdrive.moveAmount(self.dirVar * int(self.moveEntry.get())*self.getConversionFactor()))
            
        
    def moveConstSpeed(self):
        self.motor.send(mdrive.changeAcceleration())
        self.motor.send(mdrive.changeDeceleration())
        self.motor.send(mdrive.changeInitialVelocity())
        self.motor.send(mdrive.changeMaximumVelocity())
        time.sleep(1)
        if self.constVelocityEntry.get():
            self.motor.send(mdrive.moveConstantSpeed(self.dirVar * int(self.constVelocityEntry.get())*self.getConversionFactor()))
        

def setPresetOne():
    print str(var_two.get())
    print str (var_two)
    if (var_two.get() == 1):
        self.presetone = [self.mdrive.acceleration, self.mdrive.deceleration,self.mdrive.initialVelocity,self.mdrive.maximumVelocity]
        print "awesome"
    else:
        print "other"
        
root = Tk()
#var_two = IntVar()

app = App(root)

root.wm_title("Motor Bro v. 1.3")

root.mainloop()


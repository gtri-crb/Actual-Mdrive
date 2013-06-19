#Pranav Shenoy and Tejas Khorana
#June 6, 2013


#imports



#motor functions


class MDrive:
    acceleration = 0
    deceleration = 0
    microstepResolution = 0
    position = 0
    initialVelocity = 0
    maximumVelocity = 0

    

    def movingTest (self):                     #works!
        return("MR 1000000\r\n")

    def changeAcceleration (self, number):
        self.acceleration = number

    def changeDeceleration (self, number):
        self.deceleration = number
    
    def changeDeccelerationToAcceleration (self):
        return ("D=A\r\n")

    def changeMicrostepResolution(self, number):
        self.microstepResolution = number

    def changeInitialVelocity(self, number):
        self.initialVelocity = number

    def changeMaximumVelocity(self, number):
        self.maximumVelocity = number

    def getAccelerationAndDeceleration (self):
        return ("A=%d\r\nD=%d") % self.acceleration, self.deceleration

    def getAcceleration(self):

        return ("A=%d\r\n") % self.acceleration

    def getMicrostepResolution(self):
        return ("MS=%d\r\n") % self.microstepResolution

    def resetPositionCounter(self):             
        return ("P=0\r\n")
    
    def getInitialVelocity(self):
        global initialVelocity
        stringhere = "VI=%d\r\n" % self.initialVelocity
        return stringhere
#        return ("VI=%s\r\n") % initialVelocity

    def getMaximumVelocity(self, ):
        return ("VM=%d\r\n") % self.maximumVelocity
    
    def moveAmount(self, number):                      #works!
        return("MR %d\r\n") % number

    def moveConstantSpeed(self, number):
        return ("SL %d\r\n") % number

    def stop(self):
        return ("SL\r\n")
    

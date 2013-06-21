#Pranav Shenoy and Tejas Khorana
#June 6, 2013


#imports



#motor functions


class MDrive:
    acceleration = 1000000
    deceleration = 1000000
    microstepResolution = 0
    position = 0
    initialVelocity = 1000
    maximumVelocity = 68000
 

    

    def movingTest (self):                     #works!
        return("MR 1000000\r\n")

    def changeAcceleration (self):
        return ("A %d \r\n") % self.acceleration



    def getAcceleration (self):
        return ("PR A\r\n")

    def getPosition (self):
        return ("PR P")

    def getVelocity (self):
        return ("PR V")
    
    def changeDeceleration (self):
        return ("D %d \r\n") % self.deceleration
    
    def changeDecelerationToAcceleration (self):
        return ("D=A\r\n")

    def changeMicrostepResolution(self, number):
        self.microstepResolution = number
        return ("MS=%d \r\n") % number

    def changeInitialVelocity(self):

        return ("VI %d \r\n") % self.initialVelocity

    def changeMaximumVelocity(self):

        return ("VM=%d \r\n") % self.maximumVelocity

    def getAccelerationAndDeceleration (self):
        return ("A=%d\r\nD=%d") % self.acceleration, self.deceleration

    def resetPositionCounter(self):             
        return ("P=0\r\n")
    
    def moveAmount(self, number):                      #works!
        return("MR %d\r\n") % number

    def moveConstantSpeed(self, number):
        return ("SL %d\r\n") % number

    def stop(self):
        return ("SL\r\n")
    

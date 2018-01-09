import os
clear = lambda: os.system('cls')
 
import math
 
Gravity = 9.80665

class S2Params:
    Name = "S2"
    Drymass = 4500
    PayloadMass = 8000
    PropellantMass = 111500 
    Thrust = 934
    ISP = 348

class S1Params:
    Name = "S1"
    Drymass = 27200 
    PayloadMass = S2Params.Drymass + S2Params.PayloadMass + S2Params.PropellantMass
    PropellantMass = 411000
    Thrust = 845 * 9 
    ISP = 296.5


class Sim:

    def input(self, prompt, defaultVal):
        i = input("%s [%s] " % (prompt, defaultVal))
        if len(i) == 0:
            print("input not specified. Using default ", defaultVal)
            return defaultVal
        else:
            print("input specified. Using ", i, " ...")
            ie = eval(i)
            print("evaluated input: ", ie, " ...")            
            if type(defaultVal) is float:
                return float(ie)
            elif type(defaultVal) is int:
                return int(ie)
            else:
                return ie

    def run(self, stage):
        
        clear()

        stage = S1Params
        stageName = input("stageName (S1|S2) ")
        if (stageName == "S2"):
            stage = S2Params

        print("Stage selected: ", stage.Name)
       
        DryMass = self.input("kg | Dry Mass: ", stage.Drymass)
        PayloadMass = self.input("kg | Payload Mass: ", stage.PayloadMass)
        print("")
       
        PropellantMass = self.input("kg | Propellant Mass: ", stage.PropellantMass)
        print("")
     
        Thrust = self.input("kN | Thrust: ", stage.Thrust)
        ISP = self.input("s | Specific Impulse: ", stage.ISP)
        print("")
     
        exhaustVelocity = ISP * Gravity
     
        initialTotalMass = DryMass + PayloadMass + PropellantMass
        finalTotalMass = DryMass + PayloadMass
        TsiolkovskyDeltaV = exhaustVelocity * math.log(initialTotalMass / finalTotalMass)
        print("Tsiolkovsky Rocket Equation Delta-v: " + str(TsiolkovskyDeltaV) + "m/s.")
     
        print("")
       
        fuelPerSecond = Thrust * 1000 / exhaustVelocity
        print("Burning " + str(fuelPerSecond) + " kg of fuel per second.")
        print("Burn Time: " + str(PropellantMass / fuelPerSecond) + " seconds.")
        fuel = PropellantMass
     
        totalDeltaV = 0
        while fuel >= fuelPerSecond:
            fuel -= fuelPerSecond
            totalMass = DryMass + PayloadMass + fuel
            totalDeltaV += Thrust * 1000 / totalMass
     
        totalDeltaV += (Thrust * 1000 / (DryMass + PayloadMass)) * (fuel / fuelPerSecond)
     
        print("Total Delta-v for specified vehicle: " + str(totalDeltaV) + "~m/s.")
     
        print(input(""))

s = Sim()

while True:
    s.run(S2Params)
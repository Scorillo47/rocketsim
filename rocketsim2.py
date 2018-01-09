import os
clear = lambda: os.system('cls')
 
import math
 
Gravity = 9.80665

class F9_S2:
    def __init__(self, finalPayload):
        self.Name = "S2"
        self.Drymass = 4500
        self.PayloadMass = finalPayload
        self.PropellantMass = 111500 
        self.Thrust = 934
        self.ISP = 348

class F9_S1:
    def __init__(self, s2):
        self.s2 = s2

        self.Name = "S1"
        self.Drymass = 27200 
        self.PayloadMass = s2.Drymass + s2.PayloadMass + s2.PropellantMass
        self.PropellantMass = 411000
        self.Thrust = 845 * 9 
        self.ISP = 296.5


class FH_S15:
    def __init__(self, s2, f9s1, s10propellantFraction):
        self.s2 = s2
        self.f9s1 = f9s1
        self.s10propellantFraction = s10propellantFraction

        self.Name = "FHS15"
        self.Drymass = f9s1.Drymass 
        self.PayloadMass = s2.Drymass + s2.PayloadMass + s2.PropellantMass
        self.PropellantMass = f9s1.PropellantMass * (1 - s10propellantFraction)
        self.Thrust = 845 * 9
        self.ISP = 296.5

class FH_S10:
    def __init__(self, s2, s15, f9s1, s10propellantFraction):
        self.s2 = s2
        self.s15 = s15
        self.f9s1 = f9s1
        self.s10propellantFraction = s10propellantFraction

        self.Name = "FHS10"
        self.Drymass = 3 * f9s1.Drymass  
        self.PayloadMass = s2.Drymass + s2.PayloadMass + s2.PropellantMass + \
                            f9s1.PropellantMass * (1 - s10propellantFraction)
        self.PropellantMass = f9s1.PropellantMass * (2 + s10propellantFraction)
        self.Thrust = 845 * 9 * 3
        self.ISP = 296.5


class Sim:

    def input(self, prompt, defaultVal):
        if self.autorun:
            print("{0} = {1}".format(prompt, defaultVal))
            return defaultVal
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

    def run(self, stage, autorun):
        
        self.autorun = autorun

        print("===================================")

        if stage == None:
            stage = S1
            stageName = input("stageName (S1|S2) ")
            if (stageName == "S2"):
                stage = S2

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

        return totalDeltaV
     

s = Sim()

print("#############################################################")

finalPayload = 8000

print("- testing Falcon 9 with payload %d ... " % finalPayload)

s2 = F9_S2(finalPayload)
s1 = F9_S1(s2)

deltav = s.run(s2, True)
deltav += s.run(s1, True)    
print("Delta V = ", deltav)

print("#############################################################")

finalPayload = 5000

print("- testing Falcon 9 with payload %d ... " % finalPayload)

s2 = F9_S2(finalPayload)
s1 = F9_S1(s2)

deltav = s.run(s2, True)
deltav += s.run(s1, True)    
print("Delta V = ", deltav)


print("#############################################################")

s10propellantFraction = 0.2

finalPayload = 8000

print(("- testing Falcon Heavy with payload %d and center " + 
            " booster fuel fraction %f consumed before" + 
            " side booster separation ") % 
            (finalPayload, s10propellantFraction))

fhs2 = F9_S2(finalPayload)
f9s1 = F9_S1(s2)

fhs15 = FH_S15(s2, f9s1, s10propellantFraction)
fhs10 = FH_S10(s2, fhs15, f9s1, s10propellantFraction)

deltav = s.run(s2, True)
deltav += s.run(fhs15, True)    
deltav += s.run(fhs10, True)    
print("Delta V = ", deltav)


# https://www.reddit.com/r/spacex/comments/7o2e1v/an_analysis_of_falcon_9_falcon_heavy_and_kestrel/ 

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
    def __init__(self, s2, f9s1, 
            fCBS10ThrottleBack, fS15recovery, fS10recovery):
        self.Name = "FH_S15"
        self.s2 = s2
        self.f9s1 = f9s1
        self.fCBS10ThrottleBack = fCBS10ThrottleBack
        self.fS15recovery = fS15recovery
        self.fS10recovery = fS10recovery
        self.Calc()

    def Calc(self):
        self.Drymass = f9s1.Drymass + 5000
        s2Payload = s2.Drymass + s2.PayloadMass + s2.PropellantMass
        self.PayloadMass = s2Payload + \
            f9s1.PropellantMass * self.fS15recovery
        f10CB_FuelFraction = fCBS10ThrottleBack * (1 - self.fS10recovery)
        self.PropellantMass = f9s1.PropellantMass * \
            (1 - f10CB_FuelFraction - self.fS15recovery)
        self.Thrust = 845 * 9  # 100% burn
        self.ISP = 296.5


# Two side boosters
class FH_S10:
    def __init__(self, s2, s15, f9s1, fCBS10ThrottleBack, fS10recovery):
        self.Name = "FH_S10"
        self.s2 = s2
        self.s15 = s15
        self.f9s1 = f9s1
        self.fCBS10ThrottleBack = fCBS10ThrottleBack
        self.fS10recovery = fS10recovery
        self.Calc()

    def Calc(self):
        # 200kg from the booster drymass due to replacement of the
        #   interstage with nosecones which look smaller
        # 5000kg to the center core drymass due to structural
        #   reinforcements and embedded attachment points. 
        self.Drymass = 3 * f9s1.Drymass + 5000 - 400
        self.s2Payload = s2.Drymass + s2.PayloadMass + s2.PropellantMass
        f10CB_FuelFraction = self.fCBS10ThrottleBack * (1 - self.fS10recovery)
        self.PayloadMass =  self.s2Payload + \
            2 * f9s1.PropellantMass * (self.fS10recovery) + \
            f9s1.PropellantMass * (1 - f10CB_FuelFraction)
        self.PropellantMass = \
            2 * f9s1.PropellantMass * (1 - self.fS10recovery) + \
            f9s1.PropellantMass * (f10CB_FuelFraction)
        self.Thrust = 845 * 9 * 2 + 845 * 9 * self.fCBS10ThrottleBack
        self.ISP = 296.5


# More side boosters
class FSH_S10:
    def __init__(self, s2, s15, f9s1, 
            fCBS10ThrottleBack, fS10recovery, numSideBoosters):
        self.Name = "FSH_S10"
        self.s2 = s2
        self.s15 = s15
        self.f9s1 = f9s1
        self.fCBS10ThrottleBack = fCBS10ThrottleBack
        self.fS10recovery = fS10recovery
        self.numSideBoosters = numSideBoosters
        self.Calc()

    def Calc(self):
        # 200kg from the booster drymass due to replacement of the
        #   interstage with nosecones which look smaller
        # 5000kg to the center core drymass due to structural
        #   reinforcements and embedded attachment points. 
        self.Drymass = 5 * f9s1.Drymass + 5000 - self.numSideBoosters * 200
        self.s2Payload = s2.Drymass + s2.PayloadMass + s2.PropellantMass
        f10CB_FuelFraction = self.fCBS10ThrottleBack * (1 - self.fS10recovery)

        self.PayloadMass = self.s2Payload
        self.PayloadMass += self.numSideBoosters * f9s1.PropellantMass * \
                                self.fS10recovery
        self.PayloadMass += f9s1.PropellantMass * (1 - f10CB_FuelFraction)

        self.PropellantMass = f9s1.PropellantMass * \
                self.numSideBoosters * (1 - self.fS10recovery)
        self.PropellantMass += f9s1.PropellantMass * (f10CB_FuelFraction)

        self.Thrust = 845 * 9 * self.numSideBoosters
        self.Thrust += 845 * 9 * self.fCBS10ThrottleBack

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

fCBS10ThrottleBack = 0.7 # 30% consumed prior to side booster separation
f15recovery = 0.08 # 8% left for center booster recovery
f10recovery = 0.20 # 8% left for center booster recovery

finalPayload = 8000

print(("- testing Falcon Heavy with payload %d and center " + 
            " booster fuel fraction %f consumed before" + 
            " side booster separation and %f fraction for center recovery ") % 
            (finalPayload, fCBS10ThrottleBack, f15recovery))

fhs2 = F9_S2(finalPayload)
f9s1 = F9_S1(s2)

fhs15 = FH_S15(fhs2, f9s1, fCBS10ThrottleBack, f15recovery, f10recovery)
fhs10 = FH_S10(fhs2, fhs15, f9s1, fCBS10ThrottleBack, f10recovery)

deltav = s.run(fhs10, True)    
deltav += s.run(fhs15, True)    
print("S1(10 + 15) Delta V = ", deltav)
deltav += s.run(fhs2, True)
print("S1(10 + 15) + S2 Delta V = ", deltav)

print("#############################################################")

fCBS10ThrottleBack = 0.7 # 30% consumed prior to side booster separation
f15recovery = 0.08 # 8% left for center booster recovery
f10recovery = 0.20 # 8% left for center booster recovery

finalPayload = 8000
numSideBoosters = 4

print(("- testing Falcon SuperHeavy with payload %d and center " + 
            " booster fuel fraction %f consumed before" + 
            " side booster separation and %f fraction for center recovery ") % 
            (finalPayload, fCBS10ThrottleBack, f15recovery))

fhs2 = F9_S2(finalPayload)
f9s1 = F9_S1(s2)

fhs15 = FH_S15(fhs2, f9s1, fCBS10ThrottleBack, f15recovery, f10recovery)
fhs10 = FSH_S10(fhs2, fhs15, f9s1, fCBS10ThrottleBack, f10recovery, \
            numSideBoosters)

deltav = s.run(fhs10, True)    
deltav += s.run(fhs15, True)    
print("S1(10 + 15) Delta V = ", deltav)
deltav += s.run(fhs2, True)
print("S1(10 + 15) + S2 Delta V = ", deltav)

print("#############################################################")

fCBS10ThrottleBack = 0.7 # 30% consumed prior to side booster separation
f15recovery = 0.08 # 8% left for center booster recovery
f10recovery = 0.20 # 8% left for center booster recovery

finalPayload = 8000
numSideBoosters = 6

print(("- testing Falcon SuperHeavy with payload %d and center " + 
            " booster fuel fraction %f consumed before" + 
            " side booster separation and %f fraction for center recovery ") % 
            (finalPayload, fCBS10ThrottleBack, f15recovery))

fhs2 = F9_S2(finalPayload)
f9s1 = F9_S1(s2)

fhs15 = FH_S15(fhs2, f9s1, fCBS10ThrottleBack, f15recovery, f10recovery)
fhs10 = FSH_S10(fhs2, fhs15, f9s1, fCBS10ThrottleBack, f10recovery, \
            numSideBoosters)

deltav = s.run(fhs10, True)    
deltav += s.run(fhs15, True)    
print("S1(10 + 15) Delta V = ", deltav)
deltav += s.run(fhs2, True)
print("S1(10 + 15) + S2 Delta V = ", deltav)
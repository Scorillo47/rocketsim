import os
clear = lambda: os.system('cls')
 
import math
 
Gravity = 9.80665
 
 
while True:
    clear()
   
    DryMass = float(input("kg | Dry Mass: "))
    PayloadMass = float(input("kg | Payload Mass: "))
    print ""
   
    FuelCapacity = float(input("kg | Fuel Capacity: "))
    print ""
 
    Thrust = float(input("kN | Thrust: "))
    SpecificImpulse = input("s | Specific Impulse: ")
    print ""
 
    exhaustVelocity = SpecificImpulse * Gravity
 
    initialTotalMass = DryMass + PayloadMass + FuelCapacity
    finalTotalMass = DryMass + PayloadMass
    TsiolkovskyDeltaV = exhaustVelocity * math.log(initialTotalMass / finalTotalMass)
    print "Tsiolkovsky Rocket Equation Delta-v: " + str(TsiolkovskyDeltaV) + "m/s."
 
    print ""
   
    fuelPerSecond = Thrust * 1000 / exhaustVelocity
    print "Burning " + str(fuelPerSecond) + " kg of fuel per second."
    print "Burn Time: " + str(FuelCapacity / fuelPerSecond) + " seconds."
    fuel = FuelCapacity
 
    totalDeltaV = 0
    while fuel >= fuelPerSecond:
        fuel -= fuelPerSecond
        totalMass = DryMass + PayloadMass + fuel
        totalDeltaV += Thrust * 1000 / totalMass
 
    totalDeltaV += (Thrust * 1000 / (DryMass + PayloadMass)) * (fuel / fuelPerSecond)
 
    print "Total Delta-v for specified vehicle: " + str(totalDeltaV) + "~m/s."
 
    print raw_input("")
import pandas as pd
import numpy as np
from scipy import stats
import os
import pyNetLogo
import odepollution
import json
import time


NetLogoPath = '/home/senecaurla/Downloads/NetLogo'
modelPath = '/home/senecaurla/Documents/phd/multilevel-extension-use-cases/pollutants/pollution.nlogo'
steps = 3000
stepsForUpdate=30
population = 200


netlogo = pyNetLogo.NetLogoLink(gui=True, netlogo_home=NetLogoPath, netlogo_version='6.0')  # Linking with NetLogo
netlogo.load_model(modelPath)                                                               # Load the Model

netlogo.command('setup ' + str(population) )       #intial setup of Netlogo (clear-all, reset-ticks)

petroil = population
electric = 0
GPL = 0

for i in range (steps):
    netlogo.command('go')    
    if i % stepsForUpdate == 10: 
        pollution =  netlogo.report ("sum [ pollution ] of patches")
        print ("pollution: " + str(pollution))
        petroil, GPL, electric = odepollution.run (petroil, GPL, electric, pollution/10000)                                          # compartmental model launched
        netlogo.command('update-vehicles ' + str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)) )	# update number of vehicles
        print (str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)))
        
     
    time.sleep(0.001)                                # in order to allow the user to visualize changes through time, otherwise it runs at maximum speed

import pandas as pd
import numpy as np
from scipy import stats
import os
import json
import time
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from MobilityModel import MobilityModel
from ode_model import ODEModel
from checkers import ConsistencyChecker, CallConditionsChecker


class Launcher (GEMMA_Director):

    def __init__ (self, parameters):
        super().__init__()
        update_frequency, population = parameters
        self.parameters["update_frequency"] = update_frequency
        self.parameters["population"] = population
        self.parameters["petroil"] = population
        self.parameters["GPL"] = 0
        self.parameters["electric"] = 0

    def instantiate_sub_models (self, *args):
        modelPath, NetLogoPath, version = args
        mobilityModel = MobilityModel(modelPath, NetLogoPath, version)
        ode_model = ODEModel()
        self.sub_models ["mobility"] = mobilityModel
        self.sub_models ["ode"] = ode_model

    def setup(self):
        self.pollution_over_time=[]
        self.resultFile = "res.txt"

    def advance(self, dt):
        self.sub_models["mobility"].setup(self.parameters["population"])
        for i in range (dt):
            self.sub_models["mobility"].advance()     
            if  self.sub_models["ode"].check_call_conditions(self, i, 10) == True: #director.check_call_conditions (director.check_call_conditions_ODE, i, 10) == True:
                pollution =  self.sub_models["mobility"].getPollution()
                print ("pollution: " + str(pollution))
                self.pollution_over_time.append(pollution)
                petroil, GPL, electric = self.sub_models["ode"].advance(self.parameters["petroil"], self.parameters["GPL"], self.parameters["electric"], pollution/10000)    # compartmental model launched     
                print ("at ", i, " petroil: ", petroil, " GPL: ", GPL, " electric: ", electric)
                self.parameters["petroil"], self.parameters["GPL"], self.parameters["electric"] = self.sub_models["ode"].check_consistency(self, petroil, GPL, electric)         
                #print ("after--> petroil: ", petroil, " GPL: ", GPL, " electric: ", electric)                        
                self.sub_models["mobility"].update_vehicles(self.parameters["petroil"], self.parameters["GPL"], self.parameters["electric"])  # update number of vehicles
                #print (str(int(petroil)) + ' ' + str(int(GPL)) + ' ' + str(int(electric)))
     


    def check_consistency(self, *args):
        pass 

    def check_call_conditions (self, *args):
        pass        

    def retrieve_results (self):
        with open (self.resultFile, "w") as file:
            for index, elem in enumerate (self.pollution_over_time):
                file.write ("At timestep " + str(index * self.parameters["update_frequency"]) + " pollution: " + str(elem))



############################################################################################################################################


NetLogoPath = '/home/luca/Downloads/NetLogo/'
modelPath = '/home/luca/Documents/gemma/pollutants/pollution.nlogo'
steps = 3000
update_frequency=30
population = 200

director = Launcher([update_frequency, population])
director.setup()
director.instantiate_sub_models (modelPath, NetLogoPath, '6.0')

director.advance(steps)
director.retrieve_results()
print ("Simulation Ended")


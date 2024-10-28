#!/bin/python3
import sys
import os
import numpy as np
from scipy.integrate import odeint
from checkers import ConsistencyChecker, CallConditionsChecker
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from mobility_model import MobilityModel
    

#unused here    
def SEIR_model(state : tuple, time : np.ndarray, 
               β : float, σ : float, γ : float) -> tuple:
    S, E, I, R = state
    δS = - β*I*S
    δE = + β*I*S - σ*E
    δI = + σ*E - γ*I
    δR = + γ*I
    return δS, δE, δI, δR 


#like the SEIR model, but describing only transition from E to I and from I to R    
def EIR_model(state : tuple, time : np.ndarray, 
               σ : float, γ : float) -> tuple:
    E, I, R = state
    δE = - σ*E
    δI = + σ*E - γ*I
    δR = + γ*I
    return δE, δI, δR 
        

class Launcher (GEMMA_Director):

    def __init__ (self):#, sub_models):
        super().__init__()
        self.σ, self.γ = 1, 0.1                        #σ = E --> I;  γ = I --> R
        if len(sys.argv) > 2:
            self.σ = float(sys.argv[2])
            self.γ = float(sys.argv[3])
        self.resultFile = "res.txt"                #output file
        if os.path.isfile(self.resultFile):
            os.remove (self.resultFile)
        self.resList = []
            
    
        

    def instantiate_sub_models (self, *args):
        self.sub_models ["mobility"] = MobilityModel()


    def setup(self, total_steps):
        self.parameters["population_size"] = int(sys.argv[1])
        self.parameters["initial_exposed"] = 10                  #individuals that are already exposed at the beginning of the simulation
        self.parameters ["duration"] = 0.15                         #duration of the continuous model execution
        self.parameters["total_steps"] = total_steps
        self.S, self.E, self.I, self.R = self.parameters["population_size"] - self.parameters["initial_exposed"], self.parameters["initial_exposed"], 0, 0  #initial number of individuals for each compartment


    def advance(self, dt):
        step = 0
        while ((self.E > 0 or self.I > 0) and step < self.parameters["total_steps"]):                                                     #repeat until epidemic is over or the assigned number of steps has been executed
            step+=1
            new_infected = -1   #reset at the beginning of the round
            if self.sub_models["mobility"].check_call_conditions(self, self.S, self.E, self.I) == True:         #if there are not susceptible people then it does not make sense to run the mobility-infection model
                #os.system ("python3 mobility_model.py " + str (S) + " " + str (E) + " " + str(I) + " " + str(R))    #run the mobility model
                self.sub_models["mobility"].setup(self.S, self.E, self.I, self.R)
                self.sub_models["mobility"].advance()
                with open('output.txt') as f:                                                                # read the number of new infected people
                    new_infected = int(f.readline())

                self.S, self.E = self.sub_models["mobility"].check_consistency(self, new_infected, self.S, self.E)

                
            time = np.linspace(0, self.parameters["duration"], 1000)                       
            state0 = (self.E, self.I, self.R)

            res = odeint(EIR_model, y0=state0, t=time, args=(self.σ, self.γ))                                          #run EIR model
            E_hat, I_hat, R_hat = zip(*res)
            newE = int(E_hat[-1])
            newI = int(I_hat[-1])
            newR = int(R_hat[-1])
            
            self.S, self.E, self.I, self.R = self.check_consistency(self, self.parameters["population_size"], self.S, newE, newI, newR)

            self.resList.append("at step " + str(step) + " S = " + str(self.S) + "; E = " + str(self.E) + "; I = " + str(self.I) + "; R = " + str(self.R) + "\n")
            print("Step " + str(step) + " has ended") 


    def check_consistency(self, checker, *args):
        return checker.checkConsistencyODE(self,*args) 

    def check_call_conditions (self, checker, *args):
        pass        

    def retrieve_results (self, *args):
        with open (self.resultFile, 'a') as r:                                                                 #output function: write epidemic progress at each step
            for elem in self.resList:
                r.write(self.resList)


if __name__ == "__main__":

    total_steps = 20
    director = Launcher()
    director.instantiate_sub_models ()
    director.setup(total_steps)
    director.advance(total_steps)
    director.retrieve_results()
    print ("Simulation Ended")

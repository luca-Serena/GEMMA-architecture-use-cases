#!/bin/python3
import sys
import os
import numpy as np
from scipy.integrate import odeint


def biggest_variation()
    

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
        


if __name__ == "__main__":

    #######################     parameters and settings #####################################
    population_size = int(sys.argv[1])
    σ, γ = 1, 0.1                        #σ = E --> I;  γ = I --> R
    if len(sys.argv) > 2:
        σ = float(sys.argv[2])
        γ = float(sys.argv[3])
    initial_exposed_fraction = 1/200      #fraction of individuals that are already exposed at the beginning of the simulation
    duration = 0.15                       #duration of the continuous model execution
    total_steps = 20
    resultFile = "res.txt"                #output file
    if os.path.isfile(resultFile):
        os.remove (resultFile)
        
    S,E,I,R = population_size - int(population_size /100), int(population_size * initial_exposed_fraction), 0, 0  #initial number of individuals for each compartment
    

    ############################      run    ##################################
    step = 0
    while ((E > 0 or I > 0) and step < total_steps):                                                     #repeat until epidemic is over or the assigned number of steps has been executed
        step+=1
        new_infected = -1   #reset at the beginning of the round
        if S > 0:           #if there are not susceptible people then it does not make sense to run the mobility-infection model
            os.system ("python3 rndwalk.py " + str (S) + " " + str (E) + " " + str(I) + " " + str(R))    #run the mobility model
            with open('output.txt') as f:                                                                # read the number of new infected people
                new_infected = int(f.readline())
                E+= new_infected                                                                         # update compartments
                S-= new_infected
            
        time = np.linspace(0, duration, 1000)                       
        state0 = (E, I, R)

        res = odeint(EIR_model, y0=state0, t=time, args=(σ, γ))                                          #run EIR model
        E_hat, I_hat, R_hat = zip(*res)
        E = int(E_hat[-1])
        I = int(I_hat[-1])
        R = int(R_hat[-1])
        continuous_loss = population_size - (S + E + I + R)                                              #local consistency control: manages continuous loss
        if continuous_loss > 0:  #add the loss from continuous to discrete to the biggest compartment
            if E > I and E > R:
                I += continuous_loss
            else:
                R += continuous_loss
    
        with open (resultFile, 'a') as r:                                                                 #output function: write epidemic progress at each step
            r.write("at step " + str(step) + " S = " + str(S) + "; E = " + str(E) + "; I = " + str(I) + "; R = " + str(R) + "\n")
            print("step " + str(step)) 




#!/bin/python3
import sys
import os
import numpy as np
from scipy.integrate import odeint


#β change from petroil to GPL
#σ change from petroil to electric
#γ change from GPL to electric

def pollution_model(state : tuple, time : np.ndarray, 
               β : float, σ : float, γ : float) -> tuple:  #β change from petroil to GPL
    petroil, GPL, electric = state
    δpetroil = - β*petroil - σ*petroil
    δGPL =  β*petroil - γ*GPL
    δelectric =  σ*petroil + γ*GPL

    
    return δpetroil, δGPL, δelectric


def run (petroil, GPL, electric): #, duration, beta):
	time = np.linspace(0, 1, 1000)
	state0 = (petroil, GPL, electric)
	β, σ, γ = 0.1, 0.08, 0.02

	res = odeint(pollution_model, y0=state0, t=time, args=(β, σ, γ))
	petroil_hat, GPL_hat, electric_hat = zip(*res)
	
	total_petroil = int(petroil_hat[-1])
	total_GPL = int(GPL_hat[-1])
	total_electric = int(electric_hat[-1])

	#local consistency control to manage loss due to conversion from continuous to discrete values

	continuous_loss = (petroil + GPL + electric) - (total_petroil + total_GPL + total_electric)  

	if continuous_loss > 0:  #add the loss from continuous to discrete to the biggest compartment
	    if total_petroil >= total_GPL and total_petroil >= total_electric:
	        total_petroil += continuous_loss
	    elif total_GPL >= total_electric:
	        total_GPL += continuous_loss
	    else:
	        total_electric += continuous_loss
	return total_petroil, total_GPL, total_electric

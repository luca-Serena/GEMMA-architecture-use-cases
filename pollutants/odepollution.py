#!/bin/python3
import sys
import os
import numpy as np
from scipy.integrate import odeint


#β change from petroil to GPL
#σ change from petroil to electric
#γ change from GPL to electric


def valuesRounding (howMany, valueList):
	returnList = [int(elem) for elem in valueList]         # list of values to return. Continuous values are discretized
	tempList = [elem - int(elem) for elem in valueList]    # temporary list with only the fractional part of the considered values
	for i in range (howMany):				 # howMany depends on the total loss
		max_value = max(tempList)			 # number with the highest fractional part
		max_index = tempList.index(max_value)	         # index with of the number with the highest fractional part
		tempList[max_index] = -1			 # to ignore in the future
		returnList [max_index] += 1			 # element of the list rounded up 

	return returnList



def pollution_model(state : tuple, time : np.ndarray, 
	β : float, σ : float, γ : float) -> tuple: 		 #β change from petroil to GPL
	petroil, GPL, electric = state
	δpetroil = - β*petroil - σ*petroil
	δGPL =  β*petroil - γ*GPL
	δelectric =  σ*petroil + γ*GPL

	    
	return δpetroil, δGPL, δelectric


def run (petroil, GPL, electric, incentive): #, duration, beta):
	time = np.linspace(0, 1, 1000)
	state0 = (petroil, GPL, electric)
	β, σ, γ = 0.1 * incentive, 0.08 * incentive, 0.02 * incentive
	
	
	res = odeint(pollution_model, y0=state0, t=time, args=(β, σ, γ))
	petroil_hat, GPL_hat, electric_hat = zip(*res)
	
	total_petroil = petroil_hat[-1]
	total_GPL = GPL_hat[-1]
	total_electric = electric_hat[-1]

	#local consistency control to manage loss due to conversion from continuous to discrete values

	continuous_loss = (petroil + GPL + electric) - (int(total_petroil) + int(total_GPL) + int(total_electric)) 

	return valuesRounding (continuous_loss, [total_petroil, total_GPL, total_electric])

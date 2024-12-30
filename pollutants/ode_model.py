#!/bin/python3
import sys
import os
import numpy as np
from scipy.integrate import odeint
from GEMMA_Interfaces import GEMMA_Component

#β change from petroil to GPL
#σ change from petroil to electric
#γ change from GPL to electric


class ODEModel(GEMMA_Component):

	def pollution_model(self, state : tuple, time : np.ndarray, 
		β : float, σ : float, γ : float) -> tuple: 
		petroil, GPL, electric = state
		δpetroil = - β*petroil - σ*petroil
		δGPL =  β*petroil - γ*GPL
		δelectric =  σ*petroil + γ*GPL
		    
		return δpetroil, δGPL, δelectric

	def setup():
		pass


	def advance (self, petroil, GPL, electric, incentive): 
		time = np.linspace(0, 1, 1000)
		state0 = (petroil, GPL, electric)
		β, σ, γ = 0.1 * incentive, 0.08 * incentive, 0.02 * incentive	
		res = odeint(self.pollution_model, y0=state0, t=time, args=(β, σ, γ))

		return self.retrieve_results(res)

	def retrieve_results(self, res):
		petroil_hat, GPL_hat, electric_hat = zip(*res)
		total_petroil = petroil_hat[-1]
		total_GPL = GPL_hat[-1]
		total_electric = electric_hat[-1]

		return int(total_petroil), int (total_GPL), int (total_electric)


	def check_call_conditions(self, checker, *args):
		return checker.checkCallConditionsODE(self,*args)

	def check_consistency (self, checker, *args):
		return checker.checkConsistencyODE(self, *args)

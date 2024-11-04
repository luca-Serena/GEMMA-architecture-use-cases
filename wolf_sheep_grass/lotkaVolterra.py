#!/bin/python3
import sys
import os
#sys.path.append("/home/SenecaUrla/Downloads/ARTIS-2.1.2-x86_64/MODELS/LUNES-epidemic")
#sys.path.append("/usr/lib64/python3.10/site-packages")
import numpy as np
import pylab as plt
from scipy.integrate import odeint
from GEMMA_Interfaces import GEMMA_Component



class LotkaVolterra(GEMMA_Component):



    def LotkaVolterra_EEuler(self, R0, F0, alpha, beta, gamma, delta, t):
    # Solves Lotka-Volterra equations for one prey and one predator species using
    # explicit Euler method.
    #
    #  R0 and F0 are inputs and are the initial populations of each species
    #  alpha, beta, gamma, delta are inputs and problem parameters  --> alpha = prey growth rate, beta = predator death rate, gamma = prey death rate, delta = predator growth rate
    #  t is an input and 1D NumPy array of t values where we approximate y values. 
    #    Time step at each iteration is given by t[n+1] - t[n].

     R = np.zeros(len(t)) # Pre-allocate the memory for R
     F = np.zeros(len(t)) # Pre-allocate the memory for F

     R[0] = R0
     F[0] = F0

     for n in range(0,len(t)-1):
      dt = t[n+1] - t[n]
      R[n+1] = R[n]*(1 + alpha*dt - gamma*dt*F[n])
      F[n+1] = F[n]*(1 - beta*dt + delta*dt*R[n])
     return R,F



    def setup():
        pass

    def advance (self, R0, F0): 
        t = np.linspace(0,5,3000) 

        alpha, beta, gamma, delta = 1.2, 2, 0.02, 0.03
         # Actually solve the problem
        R, F = self.LotkaVolterra_EEuler(R0, F0, alpha, beta, gamma, delta, t)
        return self.retrieve_results (R, F)


    def retrieve_results(self, R, F): 
        return R[-1],F[-1]

    def check_call_conditions(self, checker, *args):
        return checker.checkCallConditionsODE(self,*args)

    def check_consistency (self, checker, *args):
        return checker.checkConsistencyODE(self, *args)


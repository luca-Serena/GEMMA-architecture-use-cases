class CallConditionsChecker():

	def checkCallConditionsMobility(self, submodel, *args):
		S, E, I =  args
		if S > 0 and (E + I) > 0:
			return True
		else:
			return False

	def checkCallConditionsODE (self, submodel, *args):   #the ODE model is called every update_frequency steps
		pass
		



class ConsistencyChecker ():


	def checkConsistencyMobility (self, submodel, *args):
		new_infected, S, E =  args
		if new_infected <= 0:
			return S, E

		if new_infected > S:
			new_infected = S

		E+= new_infected                                                                         # update compartments
		S-= new_infected
		return S, E
		

	def checkConsistencyODE (self, submodel, *args):
		population_size, S, E, I, R = args
		continuous_loss = population_size - (S + E + I + R)                                              #local consistency control: manages continuous loss
		if continuous_loss > 0:  #add the loss from continuous to discrete to the biggest compartment
			if E > I and E > R:
				I += continuous_loss
			else:
				R += continuous_loss
		print ("iji  ", S, " ", E, "  ", I, "  ", R)
		return S, E, I, R  

		
class CallConditionsChecker():

	def checkCallConditionsABM(self, submodel, *args):
		pass
		

	def checkCallConditionsODE (self, submodel, *args):   #the ODE model is called every update_frequency steps
		step, frequency = args
		return step % frequency == 0
		



class ConsistencyChecker ():


	def checkConsistencyABM (self, submodel, *args):
		pass
		
		

	def checkConsistencyODE (self, submodel, *args):
		sheep, wolves = args
		return int (sheep), int (wolves)

		 

		

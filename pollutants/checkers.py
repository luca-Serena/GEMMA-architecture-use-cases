class CallConditionsChecker():

	def checkCallConditionsMobility(self, submodel, *args):
		pass


	def checkCallConditionsODE (self, submodel, *args):		#the ODE model is called every update_frequency steps

		step, update_step = args
		if step % self.parameters["update_frequency"] == update_step:
			return True
		else:
			return False		



class ConsistencyChecker ():

	def checkConsistencyMobility (self,  submodel, *args):
		pass

	def checkConsistencyODE (self, submodel, *args):           #the population of vehicles must remain constant over time
		petroil, GPL, electric = args
		loss = self.parameters["population"] - (petroil + GPL + electric)
		if loss == 0:
			return petroil, GPL, electric
		else:
			return self.valuesRounding (loss, [petroil, GPL, electric])
		
	
	def valuesRounding (self, howMany, valueList):
		returnList = [int(elem) for elem in valueList]          # list of values to return. Continuous values are discretized
		tempList = [elem - int(elem) for elem in valueList]     # temporary list with only the fractional part of the considered values
		for i in range (howMany):                               # howMany depends on the total loss
			max_value = max(tempList)                           # number with the highest fractional part
			max_index = tempList.index(max_value)               # index with of the number with the highest fractional part
			tempList[max_index] = -1                            # to ignore in the future
			returnList [max_index] += 1                         # element of the list rounded up 
		return returnList
	
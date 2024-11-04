from abc import ABC, abstractmethod
from checkers import ConsistencyChecker, CallConditionsChecker
from typing import Dict, TypeVar, Any

class GEMMA_Component (ABC):
    def __init__(self):
        self.parameters = {}

    @abstractmethod
    def retrieve_results(self, *args):
        #Retrieve the output from the GEMMA component. If it is the top-level component, then it provides the final results of the simulation. 
        pass

    @abstractmethod
    def setup (self, *args):
        #Set up the model. Not every model needs a setup phase
        pass

    @abstractmethod
    def advance (self, *args):
        #Advance with the simulation
        pass

    @abstractmethod
    def check_call_conditions(self, submodel, *args )-> bool:
        #Check the conditions for calling an underlying sub-model. A function must be passed to identify the specific type of call.
        pass

    @abstractmethod
    def check_consistency(self, submodel, *args ):
        #Check the consistency of the the received data. A function must be passed to identify the specific type of call.
        pass


class GEMMA_Director (GEMMA_Component, CallConditionsChecker, ConsistencyChecker):
    def __init__(self):
        super().__init__()
        self.sub_models: Dict[GEMMA_Component] = {}

    @abstractmethod
    def instantiate_sub_models(self, *args):
        #Create an instance of the underlying sub-models
        pass

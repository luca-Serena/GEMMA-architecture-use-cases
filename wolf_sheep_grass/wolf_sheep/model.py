"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa
from lotkaVolterra import LotkaVolterra

from wolf_sheep.scheduler import RandomActivationByTypeFiltered
#from wolf_sheep.agents import Wolf, Sheep, GrassPatch
from wolf_sheep.agents import Sheep, GrassPatch
from GEMMA_Interfaces import GEMMA_Component, GEMMA_Director
from checkers import ConsistencyChecker, CallConditionsChecker



class WolfSheep(mesa.Model, GEMMA_Director):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 50
    initial_wolves = 50

    sheep_reproduce = 0.04
    #wolf_reproduce = 0.05

    #wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_sheep=50,
        initial_wolves=50,
        sheep_reproduce=0.04,
        lotkaVolterraCallFrequency = 10,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.parameters = {}
        self.parameters["width"] = width
        self.parameters["height"] = height
        self.parameters["initial_sheep"] = initial_sheep
        self.wolves = initial_wolves
        self.parameters["sheep_reproduce"] = sheep_reproduce
        self.grass = grass
        self.parameters["grass_regrowth_time"] = grass_regrowth_time
        self.parameters["sheep_gain_from_food"] = sheep_gain_from_food
        self.parameters["frequencyOfCall"] = lotkaVolterraCallFrequency
        self.parameters["total_steps"] = 200
        self.sub_models = {}
        self.instantiate_sub_models()
        self.setup()


    def instantiate_sub_models (self, *args):
        self.sub_models ["LotkaVolterra"] = LotkaVolterra() 


    def step(self):
        self.advance()
            


    def setup (self):
        self.resultFile = "res.txt"
        self.resList = [] 

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.parameters["width"], self.parameters["height"], torus=True)
        self.datacollector = mesa.DataCollector(
            {
                #"Wolves": lambda m: m.schedule.get_type_count(Wolf),
                "Sheep": lambda m: m.schedule.get_type_count(Sheep),
                "Grass": lambda m: m.schedule.get_type_count(
                    GrassPatch, lambda x: x.fully_grown
                ),
            }
        )         

        self.running = True
        self.datacollector.collect(self)
         # Create sheep:
        for i in range(self.parameters["initial_sheep"]):
            x = self.random.randrange(self.parameters["width"])
            y = self.random.randrange(self.parameters["height"])
            energy = self.random.randrange(2 * self.parameters["sheep_gain_from_food"])
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

       
        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.parameters["grass_regrowth_time"]
                else:
                    countdown = self.random.randrange(self.parameters["grass_regrowth_time"])

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

    def advance(self):
        if self.schedule.time < self.parameters["total_steps"]:
            self.schedule.step()
            # collect data
            self.datacollector.collect(self)

            if  self.sub_models["LotkaVolterra"].check_call_conditions(self, self.schedule.time , self.parameters["frequencyOfCall"]) == True:
                sheeps, wolves = self.sub_models["LotkaVolterra"].advance(self.schedule.get_type_count(Sheep), int(self.wolves))              #calling lotka volterra model for sheep-wolves regulation
                sheeps, wolves = self.sub_models["LotkaVolterra"].check_consistency(self, sheeps, wolves)
                self.resList.append("At " + str(self.schedule.time) + "  there are " + str(sheeps) + " sheeps and " + str(wolves) + " wolves\n")
                self.wolves = wolves                                                                            #number of wolves updated
                sheepsDifferential = sheeps - self.schedule.get_type_count(Sheep)
                if sheepsDifferential > 0:                                                                              #a certain number of sheep must be created
                    for i in range (sheepsDifferential):
                        x = self.random.randrange(self.parameters["width"])
                        y = self.random.randrange(self.parameters["height"])
                        energy = self.random.randrange(2 * self.parameters["sheep_gain_from_food"])
                        sheep = Sheep(self.next_id(), (x, y), self, True, energy)
                        self.grid.place_agent(sheep, (x, y))
                        self.schedule.add(sheep)
                else:                                                                                                   #a certain number of sheep must eliminated from agents' list
                    for i in range (sheepsDifferential):
                        self.schedule.agents().pop(self.random.randrange(len(schedule.agents())))


            if self.verbose:
                print(
                    [
                        self.schedule.time,
                        #self.schedule.get_type_count(Wolf),
                        self.schedule.get_type_count(Sheep),
                        self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
                    ]
                )

        else:
            self.running = False
            self.retrieve_results()


    def retrieve_results(self): 
        print("")
        #print("Final number wolves: ", self.schedule.get_type_count(Wolf))
        print("Final number sheep: ", self.schedule.get_type_count(Sheep))
        print(
            "Final number grass: ",
            self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
        )
        with open (self.resultFile, 'a') as r:                                                                 #output function: write epidemic progress at each step
            for elem in self.resList:
                r.write(elem)
        

    def check_call_conditions(self, checker, *args):
        pass

    def check_consistency (self, checker, *args):
        pass

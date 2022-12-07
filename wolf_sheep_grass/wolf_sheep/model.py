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
import lotkaVolterra

from wolf_sheep.scheduler import RandomActivationByTypeFiltered
#from wolf_sheep.agents import Wolf, Sheep, GrassPatch
from wolf_sheep.agents import Sheep, GrassPatch


class WolfSheep(mesa.Model):
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
        #wolf_reproduce=0.05,
        #wolf_gain_from_food=20,
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
        self.width = width
        self.height = height
        self.initial_sheep = initial_sheep
        self.wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        #self.wolf_reproduce = wolf_reproduce
        #self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.frequencyOfCall = lotkaVolterraCallFrequency

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                #"Wolves": lambda m: m.schedule.get_type_count(Wolf),
                "Sheep": lambda m: m.schedule.get_type_count(Sheep),
                "Grass": lambda m: m.schedule.get_type_count(
                    GrassPatch, lambda x: x.fully_grown
                ),
            }
        )

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        '''
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)
        '''

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.schedule.time % self.frequencyOfCall == 0:                               
            sheeps, wolves = lotkaVolterra.main(self.schedule.get_type_count(Sheep), int(self.wolves))              #calling lotka volterra model for sheep-wolves regulation
            sheeps = int(sheeps)                                                                                    #discretize the number of agents
            wolves = int(wolves)
            with open ('res.txt', 'a') as f:
                print ("At " + str(self.schedule.time) + "  there are " + str(sheeps) + " sheeps and " + str(wolves) + " wolves", file=f)
            self.wolves = wolves                                                                            #number of wolves updated
            sheepsDifferential = sheeps - self.schedule.get_type_count(Sheep)
            if sheepsDifferential > 0:                                                                              #a certain number of sheep must be created
                for i in range (sheepsDifferential):
                    x = self.random.randrange(self.width)
                    y = self.random.randrange(self.height)
                    energy = self.random.randrange(2 * self.sheep_gain_from_food)
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

    def run_model(self, step_count=200):

        if self.verbose:
            #print("Initial number wolves: ", self.schedule.get_type_count(Wolf))
            print("Initial number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Initial number grass: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            #print("Final number wolves: ", self.schedule.get_type_count(Wolf))
            print("Final number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Final number grass: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )

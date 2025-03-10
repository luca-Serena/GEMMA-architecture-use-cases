import os
import sys
from typing import Dict, Tuple
from mpi4py import MPI
import numpy as np
from dataclasses import dataclass

from repast4py import core, random, space, schedule, logging, parameters
from repast4py import context as ctx
import repast4py
from repast4py.space import DiscretePoint as dpt

from GEMMA_Interfaces import GEMMA_Component
from checkers import CallConditionsChecker, ConsistencyChecker


class MobilityModel(GEMMA_Component):

    def __init__(self):
         pass

    def setup (self, *args):
        self.S, self.E, self.I, self.R = args
        if (os.path.exists ("output/meet_log.csv")):
            os.system ("rm output/*")
        

    def advance(self, *args):
        params = parameters.init_params("random_walk.yaml", '{}')
        run(params, self.S, self.E, self.I, self.R)
        self.retrieve_results()

    def retrieve_results (self):
        with open('output.txt', 'w') as f:
            print (counter, file=f)

    def check_call_conditions (self, checker, *args):
        return checker.checkCallConditionsMobility(self,*args)


    def check_consistency(self, checker, *args):
        return checker.checkConsistencyMobility(self, *args)


counter=0

class Walker(core.Agent):

    TYPE = 0
    OFFSETS = np.array([-1, 1])

    def __init__(self, local_id: int, rank: int, pt: dpt, state: str):
        super().__init__(id=local_id, type=Walker.TYPE, rank=rank)
        self.pt = pt
        self.state = state

    def save(self) -> Tuple:
        """Saves the state of this Walker as a Tuple.

        Returns:
            The saved state of this Walker.
        """
        return (self.uid, self.meet_count, self.pt.coordinates)

    def walk(self, grid):
        # choose two elements from the OFFSET array
        # to select the direction to walk in the
        # x and y dimensions
        xy_dirs = random.default_rng.choice(Walker.OFFSETS, size=2)
        self.pt = grid.move(self, dpt(self.pt.x + xy_dirs[0], self.pt.y + xy_dirs[1], 0))

    def count_colocations(self, grid):
        global counter
        ag = grid.get_agents(self.pt)
        for a in ag:
            if a.state == 'S' and a.id != self.id:
                #print (a.state + str(self.pt))
                a.state = 'E'
                counter +=1

walker_cache = {}


def restore_walker(walker_data: Tuple):
    """
    Args:
        walker_data: tuple containing the data returned by Walker.save.
    """
    # uid is a 3 element tuple: 0 is id, 1 is type, 2 is rank
    uid = walker_data[0]
    pt_array = walker_data[2]
    pt = dpt(pt_array[0], pt_array[1], 0)

    if uid in walker_cache:
        walker = walker_cache[uid]
    else:
        walker = Walker(uid[0], uid[2], pt)
        walker_cache[uid] = walker

    walker.meet_count = walker_data[1]
    walker.pt = pt
    return walker


class Model:
    """
    The Model class encapsulates the simulation, and is
    responsible for initialization (scheduling events, creating agents,
    and the grid the agents inhabit), and the overall iterating
    behavior of the model.

    Args:
        comm: the mpi communicator over which the model is distributed.
        params: the simulation input parameters
    """

    def __init__(self, comm: MPI.Intracomm, params: Dict, S, E, I, R):
        S = int(S)
        E = int(E)
        I = int(I)
        R = int(R)
        # create the schedule
        self.runner = schedule.init_schedule_runner(comm)
        self.runner.schedule_repeating_event(1, 1, self.step)
        self.runner.schedule_repeating_event(1.1, 10, self.log_agents)
        self.runner.schedule_stop(params['stop.at'])

        # create the context to hold the agents and manage cross process
        # synchronization
        self.context = ctx.SharedContext(comm)

        # create a bounding box equal to the size of the entire global world grid
        box = space.BoundingBox(0, params['world.width'], 0, params['world.height'], 0, 0)
        # create a SharedGrid of 'box' size with sticky borders that allows multiple agents
        # in each grid location.
        self.grid = space.SharedGrid(name='grid', bounds=box, borders=space.BorderType.Sticky,
                                     occupancy=space.OccupancyType.Multiple, buffer_size=2, comm=comm)
        self.context.add_projection(self.grid)

        rank = comm.Get_rank()
        rng = repast4py.random.default_rng
        for i in range(S + E + I + R):
            # get a random x,y location in the grid
            pt = self.grid.get_random_local_pt(rng)
            # create and add the walker to the context
            if i < S: 
            	walker = Walker(i, rank, pt, 'S')
            elif i < E + S:
            	walker = Walker(i, rank, pt, 'E')
            elif i < S + E + I:
            	walker = Walker(i, rank, pt, 'I')
            else:
            	walker = Walker(i, rank, pt, 'R')
            self.context.add(walker)
            self.grid.move(walker, pt)
        
        # count the initial colocations at time 0 and log
        for walker in self.context.agents():
            if walker.state == 'I':
                walker.count_colocations(self.grid)

    def step(self):
        for walker in self.context.agents():
            walker.walk(self.grid)

        self.context.synchronize(restore_walker)

        for walker in self.context.agents():
            if walker.state == 'I':
                walker.count_colocations(self.grid)

        tick = self.runner.schedule.tick


    def log_agents(self):
        tick = self.runner.schedule.tick


    def start(self):
        self.runner.execute()


def run(params: Dict, S, E, I, R):
    model = Model(MPI.COMM_WORLD, params, S, E, I, R)
    model.start()


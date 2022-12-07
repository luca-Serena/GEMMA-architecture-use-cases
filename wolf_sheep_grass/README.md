# Wolf-Sheep Predation Model

## Models employed
- Lotka-Volterra continuous model
- A semplified version of wolf-sheep-grass model, with grass and sheep only, run by Mesa simulator

## Summary

A simple ecological model, consisting of three agent types: wolves, sheep, and grass. The sheep wander around the grid at random. Wolves are not represented graphically but are present in the environment, and their presence influence the number of sheep
If sheep have enough energy, they reproduce, creating a new sheep (in this simplified model, only one parent is needed for reproduction). The grass on each cell regrows at a constant rate. If any wolves and sheep run out of energy, they die.

## Requirements
The following Python packages are required:
- mesa
- numpy
- scipy 

## Usage
To run just execute `python3 run.py`


## Files

* ``wolf_sheep/random_walk.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the Wolf and Sheep agents will inherit from it.
* ``wolf_sheep/test_random_walk.py``: Defines a simple model and a text-only visualization intended to make sure the RandomWalk class was working as expected. This doesn't actually model anything, but serves as an ad-hoc unit test. To run it, ``cd`` into the ``wolf_sheep`` directory and run ``python test_random_walk.py``. You'll see a series of ASCII grids, one per model step, with each cell showing a count of the number of agents in it.
* ``wolf_sheep/agents.py``: Defines the Wolf, Sheep, and GrassPatch agent classes.
* ``wolf_sheep/scheduler.py``: Defines a custom variant on the RandomActivationByType scheduler, where we can define filters for the `get_type_count` function.
* ``wolf_sheep/model.py``: Defines the Wolf-Sheep Predation model itself
* ``wolf_sheep/server.py``: Sets up the interactive visualization server
* ``run.py``: Launches a model visualization server.

### Output
At step n there are s sheeps and w wolves


## Contacts

Luca Serena <luca.serena2@unibo.it>


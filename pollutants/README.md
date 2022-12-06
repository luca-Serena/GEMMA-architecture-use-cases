# Multilevel Modeling and Simulation. Pollutants Diffusion Use Case

## Models employed
- a compartmental model that describes vehicles' transition through the use of ordinary differential equations
- cellular automaton mobility model, developed with NetLogo

## Important Parameters

- steps = number of netLogo steps
- stepsForUpdate = compartmental model update the number of vehicles with a certain fuel every stepsForUpdate steps
- population = number of agents in the model

## Requirements
The following Python packages are required:
-numpy
-scipy
-pyNetLogo

Furthermore, NetLogo software must be installed


## Usage
The user has to open `pollution-launcher.py` file and then set the path of NetLogo executable and the path of .nlogo model
Then, to run just execute `python3 pollution-launcher.py`


### Outputs

NetLogo plots


## Contacts

Luca Serena <luca.serena2@unibo.it>


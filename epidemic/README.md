# Multilevel Modeling and Simulation. Epidemic Use Case

## Models employed
- a variant of SEIR model, continuous model describing the evolution of epidemic through time by the use of ordinary differential equations
- a cellular automaton mobility model, developed with Repast software

## Important Parameters

- population_size = number of individuals in the model
- σ = parameter to manage transition from exposed to infected in compartmental model
- γ = parameter to manage transition from infected to recovered in compartmental model
- initial_exposed_fraction = fraction of individuals that are already exposed at the beginning of the simulation
- total_steps = number of "rounds" during the execution
- resultFile = file where to write the output of the model

## Requirements
The following python packages are required:
- numpy
- scipy
- mpi4py
- repast4py

## Usage
The file to execute is `seir.py`, and one must indicate the number of individuals through the command line. Other parameters are settable in the file `seir.py`

For example: 
`python3 seir.py 2000`


### Outputs

at step n  S = s; E = e; I = i; R = r


## Contacts

Luca Serena <luca.serena2@unibo.it>


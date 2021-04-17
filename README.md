# Simulation of Highway Calls
This repository provides a simple simulation for testing the amount of dropped or blocked calls given a channel reservation schema.

# Running code
Clone this repository and enter the directory with the following command:
```bash
git clone https://github.com/reubenwong97/highway_calls_simulation.git && cd highway_calls_simulation
```
There are multiple ways for running the simulation. 
First, if you wish to run in serial mode for debugging, run the following:
```bash
python serial.py --reps 16 --num_reserve 1
```
To speed up the process, running in parallel is also possible:
```bash
python parallel.py --reps 16 --num_reserve 1 --workers 6
```

# Analysing results
To analyse and store results in text file, run:
```bash
python analyse.py --reps 16 --num_reserve 1
```
Ensure that the reps and number of reserves when running analysis match those that you want to analyse.
Results are stored in `results/reserve_{num_reserve}/` and text results are stored in `results/text_results/`.

# Results
Results from experiments are stored in this directory. Raw numpy binaries are stored in the `reserve{args.num_reserve}` folders, indicating how many channels were reserved. 

# Text Analysis
Text results come from the automated analysis process in `analyse.py`, giving you information about the mean, variance, standard deviation, and half-width at a 95% confidence interval of the drop and block rates.

To analyse the experiment that you had run, just use the same arguments to `analyse.py`. A concrete example will be provided here:
If we ran the following,
```bash
python parallel.py --reps 32 --num_reserve 2 --workers 8
```
We performed 32 independent experiments with 2 reserve channels. Hence, to analyse that experiment, we would run the following,
```bash
python analyse.py --reps 32 --num_reserve 2
```

Text results come in the following format:
```
------------------- Displaying arrays -------------------
Drop array: [...]
Block array: [...]
---------------------------------------------------------
----------------- Displaying statistics -----------------
|---------------- Drop Rate ----------------------------|
Mean drop rate: {mu}
Variance of drop rate: {var}
Standard deviation of drop rate: {np.sqrt(var)}
Half-width of drop rate: {delta}
---------------------------------------------------------
|---------------- Block Rate ---------------------------|
Mean of block rate: {mu}
Variance of block rate: {var}
Standard deviation of block rate: {np.sqrt(var)}
Half-width of block rate: {delta}
---------------------------------------------------------
```

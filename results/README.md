# Results
Results from experiments are stored in this directory. Raw numpy binaries are stored in the `reserve{args.num_reserve}` folders, indicating how many channels were reserved. 

# Text Analysis
Text results come from the automated analysis process in `analyse.py`, giving you information about the mean, variance, standard deviation, and half-width at a 95% confidence interval of the drop and block rates.

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

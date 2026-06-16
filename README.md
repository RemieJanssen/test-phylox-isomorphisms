# test-phylox-isomorphism

Test execution time of isomorphism and automorphism functions in PhyloX with and without the mu-vector implementation.

## Create run environment
The code is run with pinned versions of packages.
The packages are defined as a conda environment: `./envs/phylox.yaml`.
These packages are pinned for a RedHat system.
If you want to run these experiments in another system, you may want to create the environment again with the less precisely pinned versions in `./envs/phylox.source.yaml`.

 create a conda environment with the remaining dependencies:
```
  mamba env update -f ./envs/phylox.yaml
  conda activate phylox
```

## Generate networks and run tests

The tests are run with the testall.sh script.
By setting USE_BSUB to 1, the tests are run with bsub on an LSF cluster.

```
./testall.sh
```

This will create a number of test networks, which are defined for the automorphism tests and for the isomorphism tests.
The variables `AUTOM_COMBOS` and `ISOM_COMBOS` define the parameters for these networks (leaves, reticulations, number of networks).

Then the tests are run with `python ./src/test_autom.py -i $outdir/` or `python ./src/test.py -i $outdir/` respectively.
These python scripts time the automorphism and isomorphism checks with and without the use of mu-vectors in PhyloX.
Results are written to a csv file in their respective directories.

If an LSF cluster is available, you can set `USE_BSUB=1` to run each combination `leaves,reticulations,number of networks,isom/autom` in a bsub command.

## Figures

Figures are created with jupyter notebooks in the `./notebooks/` directory.
These scripts load all running times from the csv files created with `testall.sh`.
The data is loaded into pandas dataframes, and then plot as figures with seaborn.

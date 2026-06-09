# test-phylox-isomorphism

Test execution time of isomorphism and automorphism functions in PhyloX with and without the mu-vector implementation.


## Code execution
First create a conda environment with the remaining dependencies:
```
  mamba env update -f ./envs/phylox.yaml
  conda activate phylox
```

The tests are run with the testall.sh script.
By setting USE_BSUB to 1, the tests are run with bsub on an LSF cluster.

```
./testall.sh
```

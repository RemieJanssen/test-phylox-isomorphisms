# test-phylox-isomorphism

Test execution time of isomorphism and automorphism functions in PhyloX with and without the mu-vector implementation.

## Tests
autom
repl:
n/k     10      50      100
10      100     100     100
50      100     100     20
100     100     20      10


isom
n,k=10 50 100 500 1000
repl = 50


## Code execution
First create a conda environment with the remaining dependencies:
```
  mamba env update -f ./envs/phylox.yaml
  conda activate phylox
```

Run the script directly with python. For example:

```
python ./var/speed_test_isom/generate.py -n 3 -k 10 -o var/speed_test_isom/networks/3_10 -l 10
```

```
python ./var/speed_test_isom/test.py -i ./var/speed_test_isom/networks/3_10/
```

or run it on an LSF cluster: `bsub -o hpc.out -e hpc.err testall.sh`.

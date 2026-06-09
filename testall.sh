#!/bin/bash

# Set to 1 to use LSF cluster bsub commands
USE_BSUB=1

# ---- Automorphism combinations ----
# Format: n k repl
AUTOM_COMBOS="
10 0 100
10 10 100
10 50 100
10 100 100
50 0 100
50 10 100
50 50 100
50 100 20
100 0 100
100 10 100
100 50 20
100 100 10
"

# ---- Isomorphism combinations ----
# Format: n k repl
ISOM_COMBOS="
10 0 50
10 10 50
10 100 50
10 1000 50
50 0 50
50 10 50
50 100 50
50 1000 50
100 0 50
100 10 50
100 100 50
100 1000 50
500 0 50
500 10 50
500 100 50
500 1000 50
1000 0 50
1000 10 50
1000 100 50
1000 1000 50
"

# ---- Generate and test ----
run_tests() {
    local n=$1
    local k=$2
    local repl=$3
    local test_type=$4  # isom of autom

    outdir="results/${test_type}/${n}_${k}"
    mkdir -p "$outdir"

    echo "n=$n, k=$k, repl=$repl"
    generate_cmd="python ./src/generate.py -n $n -k $k -o $outdir -l $repl"

    if [ "$test_type" = "isom" ]; then
        cmd="python ./src/test.py -i $outdir/"
    else
        cmd="python ./src/test_autom.py -i $outdir/"
    fi

    if [ "$USE_BSUB" -eq 1 ]; then
        echo "Running via bsub"
        bsub -o "$outdir/cluster.out" -e "$outdir/cluster.err" "${generate_cmd} && ${cmd}"
    else
        echo "Running directly"
        $generate_cmd > "$outdir/generate.out" 2> "$outdir/generate.out"
        $cmd > "$outdir/test.out" 2> "$outdir/test.out"
    fi
}

# ---- Automorphism tests ----
while read n k repl; do
    [ -z "$n" ] && continue
    run_tests $n $k $repl "autom"
done <<< "$AUTOM_COMBOS"

# ---- Isomorphism tests ----
while read n k repl; do
    [ -z "$n" ] && continue
    run_tests $n $k $repl "isom"
done <<< "$ISOM_COMBOS"
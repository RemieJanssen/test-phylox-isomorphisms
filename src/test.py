import argparse
import os
import json
import glob

from itertools import combinations_with_replacement
from time import perf_counter


from phylox import DiNetwork
from phylox.isomorphism import is_isomorphic


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Run network isomorphism for each pair of networks in the given folder
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Path of the network folder",
    )
    return parser.parse_args()


def test_isomorphism(input_folder):
    with open(os.path.join(input_folder, "settings.json"), "r") as f:
        network_settings = json.load(f)
    leaves = network_settings["leaves"]
    reticulations = network_settings["reticulations"]
    output_file = os.path.join(input_folder, "output.csv")
    with open(output_file, "w+") as f:
        f.write("n,k,id1,id2,time_no_mu,time_mu\n")
    network_files = glob.glob(f"{input_folder}/*.newick")
    for nw_path_1, nw_path_2 in combinations_with_replacement(network_files,2):
        nw_index_1 = os.path.basename(nw_path_1).split(".")[0]
        nw_index_2 = os.path.basename(nw_path_2).split(".")[0]
        with open(nw_path_1, "r") as f:
            nw_newick_1 = f.read()
        with open(nw_path_2, "r") as f:
            nw_newick_2 = f.read()
        nw_1 = DiNetwork.from_newick(nw_newick_1)
        nw_2 = DiNetwork.from_newick(nw_newick_2)

        start = perf_counter()
        is_isomorphic(nw_1, nw_2, use_mu_vector=False)
        end = perf_counter()
        time_no_mu = end - start

        start = perf_counter()
        is_isomorphic(nw_1, nw_2, use_mu_vector=True)
        end = perf_counter()
        time_mu = end - start

        with open(output_file, "a") as f:
            f.write(f"{leaves},{reticulations},{nw_index_1},{nw_index_2},{time_no_mu},{time_mu}\n")

def main():
    args = parse_args()
    test_isomorphism(args.input)

if __name__ == "__main__":
    main()
import argparse
import os
import json
import glob

from time import perf_counter


from phylox import DiNetwork
from phylox.isomorphism import count_automorphisms


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Run network autom for each network in the given folder
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


def main():
    args = parse_args()
    with open(os.path.join(args.input, "settings.json"), "r") as f:
        network_settings = json.load(f)
    leaves = network_settings["leaves"]
    reticulations = network_settings["reticulations"]
    output_file = os.path.join(args.input, "output_autom_new.csv")
    with open(output_file, "w+") as f:
        f.write("n,k,id,time_no_mu,time_mu,count_no_mu,count_mu\n")
    for nw_path in glob.glob(f"{args.input}/*.newick"):
        nw_index = os.path.basename(nw_path).split(".")[0]
        with open(nw_path, "r") as f:
            nw_newick = f.read()
        nw = DiNetwork.from_newick(nw_newick)

        start = perf_counter()
        count_no_mu = count_automorphisms(nw,use_mu_vector=False)
        end = perf_counter()
        time_no_mu = end - start

        start = perf_counter()
        count_mu = count_automorphisms(nw, use_mu_vector=True)
        end = perf_counter()
        time_mu = end - start

        with open(output_file, "a") as f:
            f.write(f"{leaves},{reticulations},{nw_index},{time_no_mu},{time_mu},{count_no_mu},{count_mu}\n")

if __name__ == "__main__":
    main()
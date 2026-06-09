import argparse
import os
import json

from phylox.rearrangement.movetype import MoveType
from phylox.generators.mcmc import sample_mcmc_networks
from phylox.generators.randomTC import generate_network_random_tree_child_sequence


MOVE_TYPE_PROBABILITIES = {
    MoveType.TAIL: 0.8,
    MoveType.HEAD: 0.2,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Generates networks with phylox MCMC generator and saves them to files.
        """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Path of the output folder",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=89034578,
        help="Random seed",
    )
    parser.add_argument(
        "-n",
        "--leaves",
        type=int,
        required=True,
        help="Number of leaves",
    )
    parser.add_argument(
        "-k",
        "--reticulations",
        type=int,
        required=True,
        help="Number of reticulations",
    )
    parser.add_argument(
        "-l",
        "--samples",
        type=int,
        required=True,
        help="Number of networks sampled",
    )
    parser.add_argument(
        "-c",
        "--correct-for-symmetries",
        action="store_true",
        help="Whether to correct for symmetries while sampling",
    )
    return parser.parse_args()


def generate_networks(leaves, reticulations, samples, output_folder, correct_for_symmetries=False, seed=None):
    starting_network = generate_network_random_tree_child_sequence(leaves, reticulations, seed=seed)
    sample_frequency = (leaves + reticulations) * 50
    for i, network in enumerate(
        sample_mcmc_networks(
            starting_network,
            MOVE_TYPE_PROBABILITIES,
            correct_symmetries=correct_for_symmetries,
            burn_in=sample_frequency,
            number_of_samples=samples,
            add_root_if_necessary=True,
            seed=1,
        )
    ):
        with open(os.path.join(output_folder, f"{i}.newick"), "w") as f:
            f.write(network.newick())


def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    with open(os.path.join(args.output, "settings.json"), "w") as f:
        f.write(json.dumps(args.__dict__))
    generate_networks(args.leaves, args.reticulations, args.samples, args.output, correct_for_symmetries=args.correct_for_symmetries, seed=args.seed)

if __name__ == "__main__":
    main()
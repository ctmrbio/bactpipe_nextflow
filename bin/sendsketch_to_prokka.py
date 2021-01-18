#!/usr/bin/env python3
from sys import argv, exit
import argparse

"""This script identifies the top ranked genus in output from sendsketch.sh from BBMap.

Script was developed for internal use in the Nextflow pipeline BACTpipe.
"""

def parse_args():
    """Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-s", "--sketch",
        required=True,
        help="Path to sendsketch.sh output file (txt)")
    parser.add_argument("-S", "--stain", 
        required=True,
        help="Path to text file containing gram staining classifications in "
            "two-column tab separated format (Genus<TAB>Stain)")
    parser.add_argument("-p", "--profile", 
        required=True,
        help="Path to TSV file with profile information")

    if len(argv) < 2:
        parser.print_help()
        exit(1)

    args = parser.parse_args()

    return args

args = parse_args()

sketch_file = args.sketch
stain_file = args.stain
profile_file = args.profile

output_stain = "Not_in_list"
output_species = "taxa"
genus = "Multiple"

with open(sketch_file, "r") as sketch:
    sketch_lines = sketch.readlines()

    genus_one_line = sketch_lines[3]
    genus_one = genus_one_line.split("\t")[11].split(" ")[0]
    species_one = genus_one_line.split("\t")[11].split(" ")[1]

    genus_two_line = sketch_lines[4]
    genus_two = genus_two_line.split("\t")[11].split(" ")[0]

    if len(genus_two) == 0 or genus_one == genus_two:
        genus = genus_one
        output_species = species_one.rstrip()
        with open(stain_file, "r") as stain:
            for line in stain:
                if line.split("\t")[0] == genus:
                    output_stain = line.rstrip().split("\t")[1]
    else:
        output_stain = "Contaminated"
print(output_stain+"\t"+genus+"\t"+output_species)

with open(profile_file, "w") as f:
    f.writelines(output_stain + "\t" + genus + "\t" + output_species)


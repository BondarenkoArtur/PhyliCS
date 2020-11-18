import sys
import argparse
import numpy as np 

parser = argparse.ArgumentParser(description="For the ground truth bed file that were generated in simulator, separate it into different samples, each with a bed file, with the given prefix.")
parser.add_argument("gt_all_csv", metavar="gt.all.csv", action="store", type=str, help="Merged ground truth file.")
parser.add_argument("leaves_npy", metavar="from_first_step.leaf_index.npy", action="store", type=str, help="File generated by the simulator, containing leaf cells indices.")
parser.add_argument("out_prefix", metavar="gt_sep/cell", action="store", type=str, help="Output prefix for the generated cell beds.")

args = parser.parse_args()

input_f = args.gt_all_csv
output_prefix = args.out_prefix
leaves_npy = args.leaves_npy
# get all the leaf ids out, each leaf id contains all the lines corresponding to it
h={}

leaves = np.load(leaves_npy)

with open(input_f, "r") as f:
    for l in f:
        values = l.rstrip().split()
        key = values[len(values)-1]

        #if cellid is not a leaf node, skip it
        if int(key) not in leaves:
            continue

        l_ = str(values[0])
        for j in range(len(values)-2):
            l_ = l_ + "\t" + str(values[j + 1])
        l_ = l_ + "\n"

        if key in h.keys():
            h[key].append(l_)
        else:
            h[key] = []
            h[key].append(l_)

# write each file
for i in h:
    f_ = output_prefix + str(i) + ".bed"
    f = open(f_, "w")
    for j in range(len(h[i])):
        f.write(h[i][j])
    f.close()

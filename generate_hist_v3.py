#!/usr/bin/env python3
"""
Generate out.hist directly from out.concon.tre and out.node.key.
Uses concordant and conflict counts already embedded in out.concon.tre.
Line 1 = concordant counts, Line 2 = conflict counts.
"""
import sys
import re

def parse_counts_from_tree(tree_str):
    """Extract node_name:count pairs from newick support values."""
    counts = {}
    # Match patterns like )247 or )NODENAME:branch
    matches = re.findall(r'\)(\d+)', tree_str)
    return [int(m) for m in matches]

def generate_hist(phyparts_dir, total_genes):
    concon_file = f"{phyparts_dir}/out.concon.tre"
    node_key_file = f"{phyparts_dir}/out.node.key"
    output_file = f"{phyparts_dir}/out.hist"

    # Read node key to get node numbers
    node_nums = []
    with open(node_key_file) as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                node_nums.append(parts[0])

    # Read concon tree - line 1 = concordant, line 2 = conflict
    with open(concon_file) as f:
        lines = f.readlines()

    concord_tree = lines[0].strip()
    conflict_tree = lines[1].strip()

    concord_counts = parse_counts_from_tree(concord_tree)
    conflict_counts = parse_counts_from_tree(conflict_tree)

    print(f"Nodes in key: {len(node_nums)}")
    print(f"Concordant values: {len(concord_counts)}")
    print(f"Conflict values: {len(conflict_counts)}")

    # Write hist file
    with open(output_file, 'w') as out:
        for i, node in enumerate(node_nums):
            if i < len(concord_counts) and i < len(conflict_counts):
                concord = concord_counts[i]
                conflict = conflict_counts[i]
                # Format: NodeX,concord,conflict,total
                out.write(f"Node{node},{float(concord)},{float(conflict)},{total_genes}\n")
            
    print(f"Written to {output_file}")

if __name__ == '__main__':
    phyparts_dir = sys.argv[1]
    total_genes = int(sys.argv[2])
    generate_hist(phyparts_dir, total_genes)

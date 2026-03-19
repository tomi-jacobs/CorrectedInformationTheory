#!/usr/bin/env python3
"""
Generate out.hist file from individual PhyParts node files.
Needed because this version of PhyParts produces individual
out.concord.node.X and out.conflict.node.X files instead of out.hist.
"""
import os
import sys
import re

def generate_hist(phyparts_dir, output_file, total_genes):
    # Find all node numbers
    node_nums = set()
    for f in os.listdir(phyparts_dir):
        m = re.match(r'out\.concord\.node\.(\d+)$', f)
        if m:
            node_nums.add(int(m.group(1)))

    print(f"Found {len(node_nums)} nodes")

    with open(output_file, 'w') as out:
        for node in sorted(node_nums):
            concord_file = os.path.join(phyparts_dir, f'out.concord.node.{node}')
            conflict_file = os.path.join(phyparts_dir, f'out.conflict.node.{node}')

            # Count concordant trees
            concord_count = 0
            if os.path.exists(concord_file):
                with open(concord_file) as f:
                    concord_count = sum(1 for line in f if line.strip())

            # Count conflict trees per alternative topology
            conflict_counts = {}
            if os.path.exists(conflict_file):
                with open(conflict_file) as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            conflict_counts[line] = conflict_counts.get(line, 0) + 1

            # Build hist line: Node,concord,conflict1,conflict2,...,total
            conflict_values = sorted(conflict_counts.values(), reverse=True)
            parts = [f'Node{node}', str(float(concord_count))]
            parts += [str(float(v)) for v in conflict_values]
            parts.append(str(total_genes))

            out.write(','.join(parts) + '\n')

    print(f"Written to {output_file}")

if __name__ == '__main__':
    phyparts_dir = sys.argv[1]
    output_file = sys.argv[2]
    total_genes = int(sys.argv[3])
    generate_hist(phyparts_dir, output_file, total_genes)

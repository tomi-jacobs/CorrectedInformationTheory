#!/usr/bin/env python3
"""
Generate out.hist from PhyParts individual node files.
Reads conflicting gene tree files, extracts topologies,
and counts occurrences of each unique topology per node.
"""
import os
import sys
import re
from collections import Counter

def get_topology(treefile):
    """Read a newick tree and return topology string (no branch lengths)."""
    try:
        with open(treefile) as f:
            tree = f.read().strip()
        # Remove branch lengths and support values
        tree = re.sub(r':[0-9.eE+-]+', '', tree)
        tree = re.sub(r'\)[0-9.eE+-]+', ')', tree)
        return tree
    except:
        return None

def generate_hist(phyparts_dir, output_file, total_genes):
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

            # Count conflict trees grouped by topology
            topology_counts = Counter()
            if os.path.exists(conflict_file):
                with open(conflict_file) as f:
                    for line in f:
                        treepath = line.strip()
                        if treepath and os.path.exists(treepath):
                            topo = get_topology(treepath)
                            if topo:
                                topology_counts[topo] += 1

            # Build hist line sorted by count descending
            conflict_values = sorted(topology_counts.values(), reverse=True)
            parts = [f'Node{node}', str(float(concord_count))]
            parts += [str(float(v)) for v in conflict_values]
            parts.append(str(total_genes))

            out.write(','.join(parts) + '\n')
            print(f"  Node{node}: {concord_count} concordant, {sum(topology_counts.values())} conflicting, {len(topology_counts)} unique topologies")

    print(f"\nWritten to {output_file}")

if __name__ == '__main__':
    phyparts_dir = sys.argv[1]
    output_file = sys.argv[2]
    total_genes = int(sys.argv[3])
    generate_hist(phyparts_dir, output_file, total_genes)

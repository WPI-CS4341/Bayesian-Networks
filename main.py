import sys
import operator
import os
import random
import networkx as nx

from node import Node
from tabulate import tabulate

DEBUG = False


def prior_sample(bn):
    """
    Generates random sample from prior distribution
    """
    # Collection of random ramples
    randoms = [random.uniform(0, 1) for _ in xrange(len(bn))]
    # Sort the nodes in the order to dependencies
    # (e.g. for every u => v, u comes before v)
    ts = [bn.node[s]['obj'] for s in nx.topological_sort(bn)]
    assignments = {}
    i = 0
    # Iterate through the nodes of the Bayesian network
    for node in ts:
        n = randoms[i]
        # If the node has parents
        if len(node.parents()) > 0:
            parent_n = [n.name for n in node.parents()]  # Parent names
            parent_p = [assignments[p] for p in parent_n if p in assignments]  # Parent probabilities
            p = None
            # Pull out the row of the CPT matching the current parent assignments
            for row in node.cpt:
                match = True
                for i in xrange(0, len(node.parents())):
                    if row[i] != parent_p[i]:
                        match = False
                if match:
                    p = row
            # Create a new assignment with the probability
            assignments[node.name] = True if n < p else False
        else:
            # Just add the singular probability if no
            assignments[node.name] = True if n < node.cpt[0][0] else False
        i += 1
    print assignments
    return assignments


def rejection_sampling(X, e, bn, N):
    n = []
    for j in xrange(1, N):
        x = prior_sample(bn)
        if x is not e:
            n[j] += 1
    return [float(i) / len(e) for i in n]


def assign_status(filename, network):
    # Read each line of status file
    if os.path.isfile(filename):
        with open(filename, "r") as infile:
            # Get first line of input file and split using commas
            line = infile.readline().strip().split(",")
            # Iterate through all nodes/statuses
            nodes = [x[1]['obj'] for x in network.nodes(data=True)]
            sorted_nodes = sorted(nodes, key=operator.attrgetter('index'))
            for i in xrange(0, len(sorted_nodes)):
                node = sorted_nodes[i]
                # Assign the status if it is not null
                if len(line[i].strip()) > 0:
                    node.status = line[i].strip()
                    network.node[node.name]['obj'] = node
    else:
        # Throw error when cannot open file
        print("Input file does not exist.")
        return False


def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 2:
        # Get data filename
        network_file = args[0]
        query_file = args[1]
        num_samples = args[2]
        # Read each line of node file
        if os.path.isfile(network_file):
            with open(network_file, "r") as infile:
                nodes = {}  # Node dictionary
                index = 0
                for line in infile:
                    # Strip the line of newlines and tabs
                    line = line.strip()
                    # Get the node name
                    name = line[:line.index(":")]
                    # Get the node list
                    b1 = line.index("[") + 1
                    b2 = line.index("]", b1)
                    g1 = line[b1:b2]
                    parents = g1.split(" ") if len(g1) > 0 else []
                    # Get the conditional probability table values
                    b3 = line.index("[", b2) + 1
                    b4 = line.index("]", b3)
                    g2 = line[b3:b4]
                    cptv = g2.split(" ") if len(g2) > 0 else []
                    # Convert the CPTVs into a table
                    table = []
                    for i in xrange(0, len(cptv)):
                        row = []
                        for j in xrange(0, len(parents)):
                            # Create a binary mask for isolating the boolean
                            # value
                            mask = pow(2, j)
                            # Apply the mask to the index of the CPTV
                            result = i & mask
                            # Resolve the mask result to a 1 (true) or 0
                            # (false) and add it to the row
                            row.append(bool(result))
                        # Add the CPT value to the end of the row
                        row.append(float(cptv[i]))
                        table.append(row)
                    # Write info to node
                    this_node = nodes[name] if name in nodes else Node(name)
                    this_node.index = index
                    this_node.addCPT(table)
                    # Generate parent nodes if they don't exist
                    for parent in parents:
                        parent_node = nodes[
                            parent] if parent in nodes else Node(parent)
                        # Add current node to the children of parent nodes
                        parent_node.addChild(this_node)
                        nodes[parent] = parent_node
                    nodes[name] = this_node
                    index += 1

                # Convert the dictionary into a sorted array for processing
                network = nx.DiGraph()
                for n in nodes:
                    node = nodes[n]
                    parents = node.parents()
                    network.add_node(node.name, obj=node)
                    for p in parents:
                        network.add_edge(p.name, node.name)
                # Assign statuses in place
                assign_status(query_file, network)

                if DEBUG:
                    # Print out nodes
                    for node in nodes:
                        n = nodes[node]
                        cpt_headers = []
                        print "\nName: " + n.name
                        print "Status " + n.status
                        print "Children: " + ",".join(map(str, n.children()))
                        print "Parents: " + ",".join(map(str, n.parents()))
                        [cpt_headers.append("Parent " + str(x))
                         for x in xrange(1, len(n.parents()) + 1)]
                        cpt_headers.append("P(n)")
                        print "CPT: \n\n" + tabulate(n.cpt, headers=cpt_headers) + "\n\n========================="

                prior_sample(network)
                # print rejection_sampling(network)

        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python main.py <network_file> <query_file> <num_samples>")


if __name__ == '__main__':
    main()

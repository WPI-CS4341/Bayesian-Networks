"""
Written by
Harry Liu (yliu17) and Tyler Nickerson (tjnickerson)
"""
import sys
import operator
import os
import random
import networkx as nx

from node import Node
from tabulate import tabulate

DEBUG = False


def get_p_given_parents(node, assignments):
    """
    Gets table rows matching certain parent values
    (specified in assignments variable)
    """
    parent_n = [n.name for n in node.parents()]  # Parent names
    parent_p = [assignments[p]
                for p in parent_n if p in assignments]  # Parent probabilities
    # Pull out the row of the CPT matching the current parent
    # assignments
    for row in node.cpt:
        match = True
        for i in xrange(0, len(parent_p)):
            if row[i] != parent_p[i]:
                match = False
        if match:
            p = row[-1]
    return p


def weighted_sample(bn, e):
    """
    Generates weighted sample
    """
    # Sort the nodes in the order to dependencies
    # (e.g. for every u => v, u comes before v)
    ts = [bn.node[s]['obj'] for s in nx.topological_sort(bn)]
    assignments = {}
    i = 0
    w = 1
    # Iterate through the nodes of the Bayesian network
    for node in ts:
        r = random.uniform(0, 1)
        # If the node has parents
        if len(node.parents()) > 0:
            # Calculate the probability given parent values
            p = get_p_given_parents(node, assignments)
        else:
            # Just add the singular probability if no
            p = node.cpt[0][0]
        # If node is in the evidence
        if node.name in e:
            w *= (1 - p) if e[node.name] is False else p
        else:
            assignments[node.name] = True if r < p else False
        i += 1
    return assignments, w


def likelihood_weighting(X, e, bn, N):
    W = {True: 0, False: 0}
    for j in xrange(0, N):
        x, w = weighted_sample(bn, e)
        b = x[X]
        W[b] += w
    return normalize(W)


def prior_sample(bn):
    """
    Generates random sample from prior distribution
    """
    # Sort the nodes in the order to dependencies
    # (e.g. for every u => v, u comes before v)
    ts = [bn.node[s]['obj'] for s in nx.topological_sort(bn)]
    assignments = {}
    i = 0
    # Iterate through the nodes of the Bayesian network
    for node in ts:
        r = random.uniform(0, 1)
        p = r
        # If the node has parents
        if len(node.parents()) > 0:
            # Calculate the probability given parent values
            p = get_p_given_parents(node, assignments)
        else:
            # Just add the singular probability if not
            p = node.cpt[0][0]
        assignments[node.name] = True if r < p else False
        i += 1
    return assignments


def is_consistent(x, e):
    """
    Checks for consistency
    (e.g. if e[n] is v, then x[n] must also be v)
    """
    consistent = True
    for n in x:
        if n in e and x[n] != e[n]:
            consistent = False
    return consistent


def get_query_evidence(bn):
    """
    Takes in a network and returns a dictionary of the query variable
    + evidence nodes, mapping their names to their values
    (i.e. {X: <query_var>, e: {<evid_var>: <evid_value})
    """
    a = {}
    e = {}
    for n in bn.nodes():
        node = bn.node[n]['obj']
        if node.status == Node.TRUE:
            e[node.name] = True
        elif node.status == Node.FALSE:
            e[node.name] = False
        elif node.status == Node.QUERY:
            a['X'] = node.name
        a['e'] = e
    return a


def normalize(d):
    return {k: float(v) / sum(d.values()) for k, v in d.iteritems()} if sum(d.values()) > 0 else None


def rejection_sampling(X, e, bn, N):
    """
    Runs rejection sampling
    (i.e. rejects all samples that aren't consistent with the evidence)
    Returns None if a divide-by-zero error is imminent
    """
    n = {True: 0, False: 0}
    # For the number of samples N
    for j in xrange(0, N):
        # Generate a prior sample
        x = prior_sample(bn)
        # Increment boolean count if x is consistent with the evidence
        if is_consistent(x, e):
            b = x[X]
            n[b] += 1
    return normalize(n)


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


def convergence_test():
    """Run sampling method several times until it converge"""

def generate_cond_prob_table():
    """Generate conditional probability table"""
    return []

def main():
    for i in xrange(10):
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
                            [cpt_headers.append(x.name)
                             for x in n.parents()]
                            cpt_headers.append("P(n)")
                            print "CPT: \n\n" + tabulate(n.cpt, headers=cpt_headers) + "\n\n========================="

                    qe = get_query_evidence(network)
                    query = "P(" + qe['X'] + "|" + ','.join(qe['e']) + ")"

                    # Run rejection sampling
                    rs = rejection_sampling(
                        qe['X'], qe['e'], network, int(num_samples))
                    rs = '-' if not rs else rs[True]

                    # Run liklihood weighting
                    lw = likelihood_weighting(qe['X'], qe['e'], network, int(num_samples))
                    lw = '-' if not lw else lw[True]

                    # Print result table
                    print '\n' + tabulate([[query, rs, lw]], ["Query", "RS", "LW"])

            else:
                # Throw error when cannot open file
                print("Input file does not exist.")
        else:
            # Show usage when not providing enough argument
            print("Usage: python main.py <network_file> <query_file> <num_samples>")


if __name__ == '__main__':
    main()

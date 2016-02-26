import sys
import os

from node import Node
from tabulate import tabulate

DEBUG = True

def assignStatus(filename, input_nodes):
    # Read each line of status file
    if os.path.isfile(filename):
        with open(filename, "r") as infile:
            # Get first line of input file and split using commas
            line = infile.readline().strip().split(",")
            # Iterate through all nodes/statuses
            for i in xrange(0, len(input_nodes)):
                # Assign the status if it is not null
                if len(line[i].strip()) > 0:
                    input_nodes[i].status = line[i].strip()
    else:
        # Throw error when cannot open file
        print("Input file does not exist.")
        return False


def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 1:
        # Get data filename
        node_filename = args[0]
        status_filename = args[1]
        # Read each line of node file
        if os.path.isfile(node_filename):
            with open(node_filename, "r") as infile:
                nodes = {}
                names = []
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
                    this_node.addCPT(table)
                    # Generate parent nodes if they don't exist
                    for parent in parents:
                        parent_node = nodes[
                            parent] if parent in nodes else Node(parent)
                        # Add current node to the children of parent nodes
                        parent_node.addChild(this_node)
                        nodes[parent] = parent_node
                    nodes[name] = this_node
                    names.append(name)

                # Convert the dictionary into a sorted array for processing
                network = []
                for name in names:
                    if name in nodes:
                        network.append(nodes[name])

                # Assign statuses in place
                assignStatus(status_filename, network)

                if DEBUG:
                    # Print out nodes
                    for n in network:
                        cpt_headers = []
                        print "\nName: " + n.name
                        print "Status " + n.status
                        print "Children: " + ",".join(map(str, n.children()))
                        print "Parents: " + ",".join(map(str, n.parents()))
                        [cpt_headers.append("Parent " + str(x)) for x in xrange(1, len(n.parents()) + 1)]
                        cpt_headers.append("P(n)")
                        print "CPT: \n\n" + tabulate(n.cpt, headers=cpt_headers) + "\n\n========================="
        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python main.py <filename>")


if __name__ == '__main__':
    main()

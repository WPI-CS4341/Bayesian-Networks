# Bayesian Network in Python
A [Bayesian network](https://en.wikipedia.org/wiki/Bayesian_network) is a network (denoted through a directed graph) which illustrates the relationships between a set of random variables given their conditional probabilistic dependencies. In this program, we create a Bayesian network using Python 2.7 which consists of a set of given variables and their conditional probability tables. The program can then read in query files to compute queries on the network using [rejection sampling](https://en.wikipedia.org/wiki/Rejection_sampling) and likelihood weighting.

## Before Running The Program
This program uses the [tabulate](https://pypi.python.org/pypi/tabulate) and [networkx](https://networkx.github.io) libraries for output formatting and graph creation/sorting. But don't worry! It's simple to get these libraries installed (in one command too!). Just `cd` into the source directory and run:

`pip install -r requirements.txt`

## Running The Program
As always, it is extremely simple to run the program. Simply `cd` into the source directory and run:

```bash
python main.py <network_file> <query_file> <num_samples>
```

where `<network_file>` is a file containing the nodes of the network and their probability tables, `<query_file>` is a file containing a single line assigning "states" to the nodes that will be used to compute the query, and `<num_samples>` is the number of samples to use in the computation. For more information on the specifications of these files, [see here](https://sites.google.com/site/cs4341aiatwpi/projects/project---6-bayes-net-implementation). An example of the above command might look like the following:

```bash
python main.py network_option_b.txt query1.txt 2500
```

## More information
If you've started to wonder at this point if we've actually crunched data with this thing, we sure have! Read the report [here](REPORT.md).

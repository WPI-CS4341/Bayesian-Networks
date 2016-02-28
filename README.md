# TODO:

### Implementation

- [x] (10 points) In your chosen language, implement a data structure(s) that represents a Bayesian Network. This structure(s) will need to represent the nodes, edges, and the CPTs for each node.  You will need a way to represent whether each node is a query variable, evidence variable, or unknown.
- [x] 2. Option B (20 points and 5 points of extra credit)

- [x] 3.  (5 points) Write a function that filename as an argument and assigns the status of each node in your network

- [ ] 4. (10 Points) Write a function that takes in the number of samples as an argument and performs rejection sampling on your bayesian network and returns the value.

- [ ] 5. (10 Points) Write a function that takes in the number of samples as an argument and performs likelihood-weighting sampling on your bayesian network and returns the value.

- [x] 6. (5 Points) Write a main method that parses the two filenames and the number of samples to use from the command line, constructs a bayesian network data structure based on the first file, assigns the status of each node based on the second file, and reports the calculated probability of both rejection and likelihood weighted sampling given the provided number of samples (by printing each probability out).  You may assume that the program will be run in the following manner (for Python).  Java, C, or C++ will follow the same general pattern.
python your_program.py network_file query_file num_samples


### Write-up (30 points)

- [ ] 1. (15 points) Run both of your functions on the provided network file (that corresponds to the option you chose in part 2 of the implementation) and two querying files. Perform trials for each query file and sampling method with the following sequence of total samples: 200, 400, 600, 800 and 1000.  Run each sampling method 10 times for each trial (make sure you seed your random number generator differently for every trial!), and report the mean and variance of each trial.  Plot the means of each sampling method against each other for each query file. Plot the variances of each sampling method against each other for each query file.

- [ ] 2. (10 points) Did either method converge to a probability?  Was there any difference in the convergence rate? If so, for each case, state which algorithm converged faster and explain why.

- [ ] 3. (5 points) Write a readme file that documents any external libraries or design choices you made in your project, as well as the language you used and compilation instructions if necessary.  Include any information that may be helpful for the TA while grading.  Make sure you document whether you chose option A or option B for part 2 of the implementation!


Extra Credit

(10 points)  In the write-up portion above, we asked you to determine the probability of each query with a predetermined amount of samples.  This will not always guarantee that the query probability will converge to the true value with the number of samples used.  Come up with a convergence test for each sampling method (the convergence test could be the same for both).  Re-run the experiments for part 1 of the write-up until each sampling method converges, and generate a plot of the mean probability for each number of samples.  Identify another query (separate from query 2) that leads to likelihood weighting significantly faster.  Plot these results as well.

(15 points) For this portion of the extra credit, you should use the provided network to try and determine the conditional probability tables.  You will have to write a function that takes in a number and produces that number of samples of the network using prior-sampling.  Using these samples, perform MLE (maximum likelihood estimation) to estimate the conditional probability table for each node.  Warning! This is not trivial in the general case.  You only have to do this for network file corresponding to the option you chose for part 2 of the implementation.  Pick a sequence of samples (similar to part 1 of the write-up).  For these numbers of samples, estimate the conditional probability tables for every node in the network.   For every number of samples you tried, plot the percent error versus the true probability for every value in the conditional probability table corresponding to the given node being true for every node in the network.  Include these reports in your write-up.   A starting resource for MLE is http://www.cse.ust.hk/bnbook/pdf/l06.h.pdf  .  Keep in mind that this is a very technical resource.  Slides 30-38 describe MLE for a general Bayesian network, slides 8-16 talk about what MLE is.

#!/usr/bin/env python3

import argparse
import re
import itertools as it
from scipy.stats import norm

def calculate_maximum_probability(mean: float, stddev: float, lines: int, text: str):
    """Calculates the maximum probability over all partitions of a given text into a given number of lines
    (along with the maximum-probability partition itself)
    when the number of letters per line is approximated by a normal distribution.

    Args:
        mean: The mean line length in letters assumed for the current portion of the manuscript.
        stddev: The standard deviation of the line length in letters assumed for the current portion of the manuscript.
        lines: The number of lines into which the text should be segmented.
        text: The text itself, where spaces and hyphens indicate valid breakpoints for new lines.

    Returns:
        The probability of the maximum-probability partition of the given text into the given number of lines.
        A list containing the maximum-probability partition of the given text, with an entry for each line of text.
    """
    # Initialize the normal distribution with the given parameters:
    normal_dist = norm(mean, stddev)
    # Split the text on all breakpoints (i.e., spaces and hyphens) and calculate the cumulative word counts up to each breakpoint:
    break_pattern = re.compile(r"[ \-]")
    tokens = break_pattern.split(text)
    cumulative_lengths = [0] + list(it.accumulate([len(t) for t in tokens])) # add a zero at the start to represent the break before the text
    tokens = ["*"] + tokens # add a placeholder token at the start to represent the break before the text
    # Define a function to return the probability of a line starting at index i (where i=0 represents the start of the text) 
    # and ending at index j:
    def get_p(i, j):
        letters = cumulative_lengths[j] - cumulative_lengths[i]
        p = normal_dist.cdf(letters + 0.5) - normal_dist.cdf(letters - 0.5) # apply continuity correction to approximate a discrete distribution
        return p
    # Now calculate the probability for all possible segmentations of the text across the given number of lines using dynamic programming:
    dp_table = [] # a dynamic programming table to store the probability of starting breakpoint i on line k
    path_table = [] # list of maximum-probability edges to each node for each path length
    for i in range(len(cumulative_lengths)):
        dp_table.append([])
        path_table.append([])
        for k in range(lines+1):
            dp_table[i].append(0)
            path_table[i].append(None)
    # Now loop through all possible line breaks and pass their probabilities forward:
    dp_table[0][0] = 1.0 # starting value
    path_table[0][0] = (0,0) # starting edge
    for i in range(len(cumulative_lengths)-1): # starting breakpoint
        for j in range(i+1,len(cumulative_lengths)): # ending breakpoint
            edge = (i, j)
            for k in range(lines): # index of line occupied by these breakpoints
                edge_weight = get_p(i, j)*dp_table[i][k]
                # Is the path containing this edge more likely than the current best path to the destination node?
                if edge_weight > dp_table[j][k+1]:
                    # If so, then update the dynamic programming table entry and the maximum-probability edge array:
                    dp_table[j][k+1] = edge_weight
                    path_table[j][k+1] = edge
    # To get the maximum-probability path, work backwards from the end of the dynamic programming table:
    path = []
    k = lines
    j = len(cumulative_lengths)-1
    while k > 0:
        edge = path_table[j][k]
        path.insert(0, edge) # add it earlier in the path
        j = edge[0]
        k -= 1
    print(path)
    # Then reconstruct the most likely partition from this path:
    partition = []
    for edge in path:
        partition.append("-".join(tokens[edge[0]+1:edge[1]+1]))
    return (dp_table[len(cumulative_lengths)-1][lines], partition)

def calculate_total_probability(mean, stddev, lines, text):
    """Calculates the total probability of finding a given text in a given number of lines
    when the number of letters per line is approximated by a normal distribution.

    Args:
        mean: The mean line length in letters assumed for the current portion of the manuscript.
        stddev: The standard deviation of the line length in letters assumed for the current portion of the manuscript.
        lines: The number of lines into which the text should be segmented.
        text: The text itself, where spaces and hyphens indicate valid breakpoints for new lines.

    Returns:
        The total probability of all partitions of the given text into the given number of lines.
    """
    # Initialize the normal distribution with the given parameters:
    normal_dist = norm(mean, stddev)
    # Split the text on all breakpoints (i.e., spaces and hyphens) and calculate the cumulative word counts up to each breakpoint:
    break_pattern = re.compile(r"[ \-]")
    cumulative_lengths = [0] + list(it.accumulate([len(t) for t in break_pattern.split(text)])) # add a zero at the start to represent the break before the text
    # Define a function to return the probability of a line starting at index i (where i=0 represents the start of the text) 
    # and ending at index j:
    def get_p(i, j):
        letters = cumulative_lengths[j] - cumulative_lengths[i]
        p = normal_dist.cdf(letters + 0.5) - normal_dist.cdf(letters - 0.5) # apply continuity correction to approximate a discrete distribution
        return p
    # Now calculate the probability for all possible segmentations of the text across the given number of lines using dynamic programming:
    dp_table = [] # a dynamic programming table to store the probability of starting breakpoint i on line k
    for i in range(len(cumulative_lengths)):
        dp_table.append([])
        for k in range(lines+1):
            dp_table[i].append(0)
    # Now loop through all possible line breaks and pass their probabilities forward:
    dp_table[0][0] = 1.0 # starting value
    for i in range(len(cumulative_lengths)-1): # starting breakpoint
        for j in range(i+1,len(cumulative_lengths)): # ending breakpoint
            for k in range(lines): # index of line occupied by these breakpoints
                dp_table[j][k+1] += get_p(i, j)*dp_table[i][k]
    return dp_table[len(cumulative_lengths)-1][lines]

def main():
    parser = argparse.ArgumentParser(description="Calculates the probability of a given number of lines containing a given text, assuming a normal distribution with specified parameters on the number of letters per line.")
    parser.add_argument("--max", action="store_true", help="Return the maximum probability over all partitions (and the maximum-probability partition) instead of the total probability.")
    parser.add_argument("mean", type=float, help="Mean of the normal distribution.")
    parser.add_argument("stddev", type=float, help="Standard deviation of the normal distribution.")
    parser.add_argument("lines", type=int, help="Number of lacunose lines.")
    parser.add_argument("text", type=str, help="The text (where spaces and hyphens indicate potential line breaks) to divide over the lines. This should be specified between quotation marks. (Example: \"υ-περ ε-μου ι-να μοι δο-θη λο-γος εν α-νοι-ξει του στο-μα-τος μου εν παρ-ρη-σι-α γνω-ρι-σαι το μυ-στη-ρι-ον υ-περ ου πρε-σβευ-ω εν α-λυ-σει\")")
    args = parser.parse_args()
    # Parse the positional arguments:
    mean = args.mean
    stddev = args.stddev
    lines = args.lines
    text = args.text
    # If the max flag is not set, then calculate the total probability and print it:
    if not args.max:
        p = calculate_total_probability(mean, stddev, lines, text)
        print("Probability of input text distributed over %d lines, assuming a normal distribution with mean %f and standard deviation %f: %.4E." % (lines, mean, stddev, p))
    else:
        p, partition = calculate_maximum_probability(mean, stddev, lines, text)
        print("Maximum probability of input text distributed over %d lines, assuming a normal distribution with mean %f and standard deviation %f: %.4E." % (lines, mean, stddev, p))
        print("Maximum-probability partition:\n%s." % "\n".join(partition))
    exit(0)

if __name__=="__main__":
    main()
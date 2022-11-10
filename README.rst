.. start-badges

|license badge|

.. |license badge| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://choosealicense.com/licenses/mit/

.. end-badges

.. start-about

A Python script for calculating the likelihood of reconstructed texts in lacunae.

When a manuscript is missing one or more lines due to illegible material or damage to the page, philologists will often offer a reconstruction of the missing text, but their reconstructions may differ.
If the text of the manuscript in question is copied in lines according to a desired length (as opposed to being copied in sense-units, in which case each line is only as long as the sense-unit requires), then we can assume a probability distribution (e.g., a normal distribution) on the line lengths and calculate the probability that a line is a given length according to this distribution.
This gives us a basic way to evaluate the probabilities of different authors' reconstructions of lacunose text, but we can be even more precise.
We can efficiently calculate the total probability of *all* divisions of a given text over a given number of lines (even restricting the possible break-points according to language-specific rules about how words should be broken over lines) using the well-known computational technique of dynamic programming.
The ``calclac`` program was designed as a lightweight implementation of this approach. 

.. end-about

.. start-quickstart

Installation
============

To use this script, you must have `Python <https://www.python.org/>`_ and `Poetry <https://python-poetry.org/>`_ installed on your computer.

To clone this repository, you can download it as a .zip archive by the clicking the "Code" button on the repository page and selecting the download option in the dropdown menu, or, if you have `Git <https://git-scm.com/>`_ installed, you can copy the clone command under the "Code" button.
In the latter case, you can install ``calclac`` entirely on the command-line as follows:

.. code-block:: bash

    git clone https://github.com/jjmccollum/calclac.git
    cd calclac
    poetry install

Usage
============

To use the software, you can run the ``calclac.py`` script with Python via the following command (assuming that you are executing the command from the directory containing the script):

.. code-block:: bash

    python calclac.py <mean line length> <standard deviation of line length> <number of lines> <text>

For the examples from P46's text of Ephesians in the paper, we know that the average line length of P46 in Ephesians is 31.5576 letters, with a standard deviation of 2.9011.
In P46, Eph 6:19-20 are lacunose, as three lines are missing at the bottom of the page.
If we wanted to evaluate the probability that a text with the longer reading in Eph 6:19 was fit into the space of these three lines, we would enter the following command, including hyphens at breakpoints within words to accommodate Greek line-breaking conventions:

.. code-block:: bash

    python calclac.py 31.5576 2.9011 3 "υ-περ ε-μου ι-να μοι δο-θη λο-γος εν α-νοι-ξει του στο-μα-τος μου εν παρ-ρη-σι-α γνω-ρι-σαι το μυ-στη-ρι-ον του ευ-αγ-γε-λι-ου υ-περ ου πρε-σβευ-ω εν α-λυ-σει"

If we wanted to do the same for a text with the shorter reading in 6:19, the corresponding command would be

.. code-block:: bash

    python calclac.py 31.5576 2.9011 3 "υ-περ ε-μου ι-να μοι δο-θη λο-γος εν α-νοι-ξει του στο-μα-τος μου εν παρ-ρη-σι-α γνω-ρι-σαι το μυ-στη-ρι-ον υ-περ ου πρε-σβευ-ω εν α-λυ-σει"

Credits
============

``calclac`` was designed by Joey McCollum (Australian Catholic University).

If you use this software, please cite the following paper: Joey McCollum, "Likelihood Calculations for Reconstructed Lacunae and Papyrus 46's Text of Ephesians 6:19," *DSH* (forthcoming), DOI: TBA.
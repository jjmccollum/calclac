.. start-badges

|license badge|

.. |license badge| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://choosealicense.com/licenses/mit/

.. end-badges

.. start-about

A Python script for calculating the likelihood of reconstructed texts in lacunae.

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

For the examples from Eph 6:19 in the paper, the command for the text containing the longer reading would be

.. code-block:: bash

    python calclac.py 31.5576 2.9011 3 "υ-περ ε-μου ι-να μοι δο-θη λο-γος εν α-νοι-ξει του στο-μα-τος μου εν παρ-ρη-σι-α γνω-ρι-σαι το μυ-στη-ρι-ον του ευ-αγ-γε-λι-ου υ-περ ου πρε-σβευ-ω εν α-λυ-σει"

and the corresponding command for the text containing the shorter reading would be

.. code-block:: bash

    python calclac.py 31.5576 2.9011 3 "υ-περ ε-μου ι-να μοι δο-θη λο-γος εν α-νοι-ξει του στο-μα-τος μου εν παρ-ρη-σι-α γνω-ρι-σαι το μυ-στη-ρι-ον υ-περ ου πρε-σβευ-ω εν α-λυ-σει"

Credits
============

``calclac`` was designed by Joey McCollum (Australian Catholic University).

If you use this software, please cite the following paper: Joey McCollum, "Likelihood Calculations for Reconstructed Lacunae and Papyrus 46's Text of Ephesians 6:19," *DSH* (forthcoming), DOI: TBA.
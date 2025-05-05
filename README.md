# core.planner
A framework to optimize FA in reactor core utilizing GA &amp; HPC

# Evolutionary Core Planner

## Overview

This repository contains a Python framework for optimizing nuclear reactor cores using genetic algorithms and high-performance computing. The framework includes three main modules:

1. **evolution.py**: Handles the initialization, crossover, mutation, and survival of the population.
2. **planner.py**: Manages the main execution flow, including argument parsing, environment setup, and iterative optimization.
3. **argsandvars.py**: Defines static and user-provided variables, checks argument validity, and merges variables for the optimization process.

## Installation

To use this framework, ensure you have Python installed along with the necessary dependencies. You can install the required packages using:

```bash
 follow the conda install file in the repository
```

## Usage

### Running the Planner

To run the planner, execute the following command:

```bash
python planner.py [options]
```

### Options

- `-m`, `--map`: Path to reactor core map configuration file. Default is `./default.map`.
- `-fa`, `--fa-types`: Percentage concentrations of U235 in fuel assemblies. Example: `1.6%2.4%3.1%`.
- `-nfa`, `--fa-amounts`: Number of fuel assemblies per type. Example: `86-86-85`.
- `-ps`, `--population-size`: Population size for evolution. Default is `100`.
- `-pl`, `--population-logic`: Population logic: `static` or `growing`. Default is `static`.
- `-bc`, `--boundary-conditions`: Neutron boundary conditions: `void` or `reflective`. Default is `void`.
- `-ml`, `--mutation-logic`: Mutation logic. Choices: `constant`, `assured`, `proportional`, `none`, `progressing`, `min1proportional`, `min1progressing`. Default is `constant`.
- `-mt`, `--mutation-type`: Type of mutation. Choices: `switch`, `shift`, `switchORshift`, `switchANDshift`, `switchORDIMshift`. Default is `switch`.
- `-ma`, `--mating-algorithm`: Mating algorithm. Choices: `random`, `weighted-random`, `alpha-fe-male-by-generation`. Default is `weighted-random`.
- `-mcl`, `--mated-couple-logic`: Mated couple logic. Choices: `inclusive`, `exclusive`, `combination`. Default is `exclusive`.
- `-os`, `--offspring-algorithm`: Offspring algorithm. Choices: `single-slice`, `random`, `double-slice`, `vertical-double-slice`, `2-double-random`, `3random`, `quadrad`, `weighted-quadrat`, `square321`, `square321byG`, `square1x1`. Default is `square321`.
- `-i`, `--iterations`, `-g`, `--generations`: Max number of generations/iterations. Default is `100`.
- `-p`, `--parallel`: Max number of parallel threads. Default is `10`.
- `-sv`, `--save-results`: Save results: `only_the_best` or `all`. Default is `only_the_best`.
- `-ot`, `--optimization-type`: Optimization type: `keff`, `ppf`, or `alpha`. Default is `keff`.
- `-v`, `--verbose`: Verbose output: `y` or `n`. Default is `n`.
- `-alpha`: Combination ratio for Keff & PPF. Default is `0.5`.

### Example

```bash
python planner 1.py -m ./core.map -fa 1.6%2.4%3.1% -nfa 86-86-85 -ps 100 -pl static -bc void -ml constant -mt switch -ma weighted-random -mcl exclusive -os square321 -i 100 -p 10 -sv only_the_best -ot keff -v n -alpha 0.5
```

## Modules

### evolution.py

- **Initialization**: Generates the initial population based on the genetic template and distribution of coding bases.
- **Crossover**: Implements various crossover algorithms to generate offspring.
- **Mutation**: Applies different mutation strategies to evolve the population.
- **Survival**: Ensures the best chromosomes survive to the next generation.

### planner.py

- **Main Execution Flow**: Parses arguments, sets up the environment, and runs the optimization iterations.
- **Environment Setup**: Prepares directories and files for the experiment.
- **Optimization Loop**: Iteratively generates, scores, and evolves the population.

### argsandvars.py

- **Static Variables**: Defines static variables used throughout the framework.
- **Argument Parsing**: Parses user-provided arguments and checks their validity.
- **Variable Merging**: Merges static and user-provided variables for the optimization process.

---

Let me know if you need any further modifications or additional information!

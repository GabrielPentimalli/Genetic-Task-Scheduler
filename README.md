# Genetic Task Scheduler

## Project Description
Genetic Task Scheduler is a Python application that uses genetic algorithms to solve single-machine scheduling problems. The system optimizes the execution order of tasks to maximize the minimum benefit among all clients, ensuring a fair allocation of resources.

## Problem Statement
The scheduling problem addressed can be defined as follows:

- There is a single machine used by $N$ clients
- For each client, a single task must be executed on the machine
- The benefit that client $j$ obtains from task execution is defined as: $u_j = b_j - a_j * c_j$
- Each task has a release time $r_j$ before which it cannot start
- The goal is to find an execution sequence that maximizes the minimum benefit among all clients: $max{min_j(u_j)}$

## Requirements
- Python 3.8+
- Required libraries:
  - numpy
  - matplotlib
  - pandas
  - deap (Distributed Evolutionary Algorithms in Python)
  - seaborn
  - tqdm

You can install dependencies with:
```bash
pip install numpy matplotlib pandas deap seaborn tqdm
```

## Project Structure
The project is implemented as a Jupyter notebook and organized into the following main components:

1. **SchedulingProblem Class**: Defines the problem and contains methods for:
   - Calculating start and completion times of tasks
   - Computing utilities for each client
   - Calculating the objective function
   - Visualizing the optimal schedule

2. **Genetic Algorithm**: Configured using the DEAP library with:
   - Solution representation as a permutation of tasks
   - Genetic operators specific for permutation problems
   - Evaluation functions based on the objective of maximizing the minimum benefit

3. **Support Functions**:
   - `run_example()`: Runs an example with random parameters
   - `parameter_tuning()`: Optimizes the genetic algorithm parameters
   - `run_custom_problem()`: Runs the algorithm with custom parameters

## How to Use

### Running the Pre-configured Example
```python
problem, best_sequence, schedule_df, logbook = run_example()
```

### Running with Custom Parameters
```python
n_clients = 10
release_times = [0, 5, 10, 2, 8, 15, 7, 12, 4, 9]
durations = [7, 10, 5, 8, 12, 6, 9, 11, 8, 7]
a_values = [0.3, 0.5, 0.2, 0.4, 0.6, 0.25, 0.35, 0.45, 0.55, 0.3]
b_values = [50, 70, 40, 60, 80, 45, 55, 65, 75, 50]

problem, best_sequence, schedule_df, logbook = run_custom_problem(
    n_clients, release_times, durations, a_values, b_values,
    population_size=100, crossover_prob=0.7, mutation_prob=0.2, n_generations=100
)
```

### Optimizing Genetic Algorithm Parameters
```python
results_df = parameter_tuning(problem)
```

## Visualizations
The system generates several visualizations to better understand the results:

1. **Gantt Chart**: Shows the execution order of tasks, with indication of release times
2. **Utility Chart**: Displays the benefit obtained by each client
3. **Evolution Graph**: Shows the progress of the genetic algorithm across generations
4. **Parameter Heatmap**: Helps identify the best configuration of genetic algorithm parameters

## Key Features
- **Max-Min Optimization**: Ensures that the client with the minimum benefit gets the maximum possible
- **Constraint Respect**: Considers task release times
- **Comprehensive Visualization**: Provides visual tools to understand the solution
- **Flexibility**: Allows easy configuration of problems with different sizes and characteristics
- **Parameter Optimization**: Includes tools to find the best genetic algorithm parameters

## Possible Extensions
- Implementation of additional constraints (deadlines, priorities, etc.)
- Support for multi-machine scheduling problems
- Integration with real scheduling systems
- Graphical interface for parameter input and result visualization
- Export of scheduling in standard formats

## Author
Gabriel Pentimalli (GabrielPentimalli)[https://github.com/GabrielPentimalli]- gab.pentimalli@stud.uniroma3.it

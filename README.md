# Genetic Task Scheduler

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A genetic algorithm implementation for a single-machine scheduling problem with a fairness objective: maximize the minimum client utility.

## Problem statement

We have a single machine shared by $N$ clients. Each client $j$ submits one task with:

- release time $r_j$ (the task cannot start earlier)
- processing time $d_j$
- benefit coefficient $b_j$
- time-penalty coefficient $a_j$

If a task completes at time $C_j$, client utility is:

$$u_j = b_j - a_j \cdot C_j$$

Goal (max-min fairness):

$$\max \; \min_j(u_j)$$

## Approach

The solution is encoded as a permutation of task IDs. The genetic algorithm uses:

- tournament selection
- order crossover (OX) to preserve valid permutations
- swap mutation
- elitism (best individuals are carried over)

## Requirements

- Python 3.8+
- NumPy
- Optional: Matplotlib (only required for `--visualize`)

Install dependencies:

```bash
python -m pip install -U pip
python -m pip install numpy matplotlib
```

## Usage

Show available options:

```bash
python scheduler.py --help
```

Run the optimizer:

```bash
python scheduler.py --n-tasks 20 --generations 200
```

Choose an instance generator:

```bash
python scheduler.py --mode balanced --n-tasks 30
python scheduler.py --mode high-contention --n-tasks 25
```

Compare against simple baselines (random best-of-100, EDF, highest benefit):

```bash
python scheduler.py --compare
```

Generate plots (Gantt chart and strategy comparison). This saves `scheduling_results.png` and opens a window when supported:

```bash
python scheduler.py --visualize --compare
```

Reduce console output:

```bash
python scheduler.py --quiet
```

## Output

The program prints:

- runtime
- best fitness (minimum utility)
- mean utility
- bottleneck task (the one with minimum utility)
- best found execution sequence


## Author

Gabriel Pentimalli

- Email: gab.pentimalli@stud.uniroma3.it
- LinkedIn: https://www.linkedin.com/in/gabriel-pentimalli-54180625a/
- GitHub: https://github.com/GabrielPentimalli
```

"""
Genetic Task Scheduler
======================
Genetic algorithm to solve a scheduling problem
aiming to maximize the minimum customer benefit (utility).
"""

import argparse
import numpy as np
import random
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional


# =============================================================================
# MAIN CLASSES
# =============================================================================

@dataclass
class Task:
    """Represents a task with its parameters."""
    id: int
    release_time: float
    duration: float
    benefit_coeff: float
    penalty_coeff: float

    def calculate_utility(self, completion_time: float) -> float:
        """Calculates utility: u = b - a * c"""
        return self.benefit_coeff - self.penalty_coeff * completion_time


class SchedulingProblem:
    """Manages the evaluation of a task sequence."""
    
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks
        self.n_tasks = len(tasks)

    def evaluate_solution(self, sequence: List[int]) -> Tuple[float, List[float], List[float], List[float]]:
        """Evaluates a solution (task sequence)."""
        current_time = 0.0
        start_times = [0.0] * self.n_tasks
        completion_times = [0.0] * self.n_tasks
        utilities = [0.0] * self.n_tasks

        for task_id in sequence:
            task = self.tasks[task_id]
            start_time = max(current_time, task.release_time)
            completion_time = start_time + task.duration
            start_times[task_id] = start_time
            completion_times[task_id] = completion_time
            utilities[task_id] = task.calculate_utility(completion_time)
            current_time = completion_time

        return min(utilities), utilities, start_times, completion_times


class GeneticAlgorithm:
    """Genetic algorithm for scheduling with OX crossover and swap mutation."""
    
    def __init__(self, problem: SchedulingProblem, 
                 population_size: int = 100,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8,
                 elite_size: int = 20,
                 verbose: bool = True):
        self.problem = problem
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = min(elite_size, population_size // 2)
        self.n_tasks = problem.n_tasks
        self.verbose = verbose
        self.history = {'best_fitness': [], 'avg_fitness': [], 'generation': []}
    
    def create_individual(self) -> List[int]:
        return list(np.random.permutation(self.n_tasks))
    
    def create_population(self) -> List[List[int]]:
        return [self.create_individual() for _ in range(self.population_size)]
    
    def fitness(self, individual: List[int]) -> float:
        return self.problem.evaluate_solution(individual)[0]
    
    def tournament_selection(self, population: List[List[int]], fitnesses: List[float], k: int = 5) -> List[int]:
        indices = random.sample(range(len(population)), k)
        winner = indices[np.argmax([fitnesses[i] for i in indices])]
        return population[winner].copy()
    
    def order_crossover(self, p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
        size = len(p1)
        start, end = sorted(random.sample(range(size), 2))
        
        def make_child(parent1, parent2):
            child = [-1] * size
            child[start:end] = parent1[start:end]
            ptr = end
            for gene in parent2[end:] + parent2[:end]:
                if gene not in child:
                    child[ptr % size] = gene
                    ptr += 1
            return child
        
        return make_child(p1, p2), make_child(p2, p1)
    
    def swap_mutation(self, individual: List[int]) -> List[int]:
        mutated = individual.copy()
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(mutated)), 2)
            mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated
    
    def evolve(self, generations: int = 200) -> Tuple[List[int], float]:
        population = self.create_population()
        best_individual, best_fitness = None, float('-inf')
        
        if self.verbose:
            print(f"{'Gen':>5}  {'Best':>10}  {'Avg':>10}")
            print("-" * 30)
        
        for gen in range(generations):
            fitnesses = [self.fitness(ind) for ind in population]
            best_idx = np.argmax(fitnesses)
            
            if fitnesses[best_idx] > best_fitness:
                best_fitness = fitnesses[best_idx]
                best_individual = population[best_idx].copy()
            
            self.history['generation'].append(gen)
            self.history['best_fitness'].append(fitnesses[best_idx])
            self.history['avg_fitness'].append(np.mean(fitnesses))
            
            if self.verbose and gen % max(1, generations // 5) == 0:
                print(f"{gen:5d}  {fitnesses[best_idx]:10.3f}  {np.mean(fitnesses):10.3f}")
            
            # New population
            new_pop = [population[i].copy() for i in np.argsort(fitnesses)[-self.elite_size:]]
            
            while len(new_pop) < self.population_size:
                if random.random() < self.crossover_rate:
                    p1 = self.tournament_selection(population, fitnesses)
                    p2 = self.tournament_selection(population, fitnesses)
                    c1, c2 = self.order_crossover(p1, p2)
                    new_pop.extend([self.swap_mutation(c1), self.swap_mutation(c2)])
                else:
                    new_pop.append(self.swap_mutation(self.tournament_selection(population, fitnesses)))
            
            population = new_pop[:self.population_size]
        
        if self.verbose:
            print(f"\n- Final Fitness: {best_fitness:.4f}")
        
        return best_individual, best_fitness


# =============================================================================
# PROBLEM GENERATORS
# =============================================================================

def generate_random_problem(n_tasks: int = 10, seed: Optional[int] = None) -> SchedulingProblem:
    """Generates problem with realistic random parameters."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
    
    tasks = []
    for i in range(n_tasks):
        priority = int(np.random.choice([1, 2, 3], p=[0.55, 0.3, 0.15]))
        tasks.append(Task(
            id=i,
            release_time=float(np.random.uniform(0.0, 9.0)),
            duration=float(np.random.choice([0.5, 1.0, 1.5, 2.0, 3.0])),
            benefit_coeff=max(40.0, float(np.random.normal(80 + priority * 25, 8))),
            penalty_coeff=float(np.clip(np.random.normal(1.1 + 0.3 * priority, 0.25), 0.4, 2.5))
        ))
    return SchedulingProblem(tasks)


def generate_balanced_problem(n_tasks: int = 10, seed: Optional[int] = None) -> SchedulingProblem:
    """Generates problem with balanced parameters (more stable utilities)."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
    
    tasks = [Task(
        id=i,
        release_time=np.random.exponential(3.0),
        duration=np.random.uniform(1.0, 5.0),
        benefit_coeff=np.random.uniform(50.0, 150.0),
        penalty_coeff=np.random.uniform(0.1, 1.0)
    ) for i in range(n_tasks)]
    return SchedulingProblem(tasks)


def generate_high_contention_problem(n_tasks: int = 10, seed: Optional[int] = None) -> SchedulingProblem:
    """Generates problem with high contention (simultaneous tasks, high penalties)."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
    
    tasks = [Task(
        id=i,
        release_time=np.random.uniform(0.0, 2.0),
        duration=np.random.uniform(1.0, 3.0),
        benefit_coeff=np.random.uniform(100.0, 200.0),
        penalty_coeff=np.random.uniform(1.0, 3.0)
    ) for i in range(n_tasks)]
    return SchedulingProblem(tasks)


# =============================================================================
# STRATEGY COMPARISON
# =============================================================================

def compare_strategies(problem: SchedulingProblem, ga_fitness: float) -> dict:
    """Compares GA with classic heuristics."""
    results = {'Genetic Algorithm': ga_fitness}
    
    # Random (best of 100)
    random_best = max(problem.evaluate_solution(list(np.random.permutation(problem.n_tasks)))[0] 
                      for _ in range(100))
    results['Random (best/100)'] = random_best
    
    # EDF - Earliest Release First
    edf = sorted(range(problem.n_tasks), key=lambda i: problem.tasks[i].release_time)
    results['EDF'], _, _, _ = problem.evaluate_solution(edf)
    
    # Highest Benefit First
    hbf = sorted(range(problem.n_tasks), key=lambda i: -problem.tasks[i].benefit_coeff)
    results['Highest Benefit'], _, _, _ = problem.evaluate_solution(hbf)
    
    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def visualize_results(problem: SchedulingProblem, solution: List[int], 
                     ga: GeneticAlgorithm, utilities: List[float],
                     start_times: List[float], comparison: dict):
    """Generates 2 essential charts for presentation."""
    try:
        import matplotlib.pyplot as plt
        plt.style.use('seaborn-v0_8-whitegrid')
    except:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib not available.")
            return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Gantt Chart
    ax1 = axes[0]
    colors = plt.cm.Set3(np.linspace(0, 1, len(solution)))
    for i, tid in enumerate(solution):
        task = problem.tasks[tid]
        ax1.barh(i, task.duration, left=start_times[tid], color=colors[tid], 
                 edgecolor='black', linewidth=0.5)
        ax1.text(start_times[tid] + task.duration/2, i, f'T{tid}', 
                 ha='center', va='center', fontsize=9, fontweight='bold')
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('Execution Order', fontsize=11)
    ax1.set_title('Gantt Chart - Optimal Scheduling', fontsize=12, fontweight='bold')
    ax1.set_yticks(range(len(solution)))
    ax1.set_yticklabels([f'{i+1}' for i in range(len(solution))])
    
    # 2. Strategy Comparison
    ax2 = axes[1]
    strategies = list(comparison.keys())
    values = list(comparison.values())
    colors = ['green' if s == 'Genetic Algorithm' else 'steelblue' for s in strategies]
    bars = ax2.barh(strategies, values, color=colors, edgecolor='black')
    ax2.set_xlabel('Fitness (Min Utility)', fontsize=11)
    ax2.set_title('Strategy Comparison', fontsize=12, fontweight='bold')
    for bar, v in zip(bars, values):
        ax2.text(v + 1, bar.get_y() + bar.get_height()/2, f'{v:.1f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('scheduling_results.png', dpi=150, bbox_inches='tight')
    print("\nCharts saved to 'scheduling_results.png'")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Genetic Task Scheduler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scheduler.py --n-tasks 20 --generations 200
  python scheduler.py --n-tasks 30 --mode balanced --visualize
  python scheduler.py --mode high-contention --n-tasks 25 --compare
        """
    )
    
    # Problem parameters
    parser.add_argument('--n-tasks', type=int, default=10, help='Number of tasks (default: 10)')
    parser.add_argument('--seed', type=int, default=None, help='Seed for reproducibility')
    parser.add_argument('--mode', type=str, default='random',
                        choices=['random', 'balanced', 'high-contention'],
                        help='Mode: random, balanced, high-contention')
    
    # GA parameters
    parser.add_argument('--generations', type=int, default=200, help='Generations (default: 200)')
    parser.add_argument('--population-size', type=int, default=100, help='Population size (default: 100)')
    parser.add_argument('--mutation-rate', type=float, default=0.1, help='Mutation rate (default: 0.1)')
    
    # Output options
    parser.add_argument('--visualize', action='store_true', help='Show charts')
    parser.add_argument('--compare', action='store_true', help='Compare strategies')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    args = parser.parse_args()
    
    # Header
    print(f"\n{'='*50}")
    print("   GENETIC TASK SCHEDULER")
    print(f"{'='*50}")
    
    # Generate problem
    generators = {
        'random': generate_random_problem,
        'balanced': generate_balanced_problem,
        'high-contention': generate_high_contention_problem
    }
    problem = generators[args.mode](n_tasks=args.n_tasks, seed=args.seed)
    
    print(f"\nProblem: {args.n_tasks} tasks, mode '{args.mode}'")
    if args.seed:
        print(f"   Seed: {args.seed}")
    
    # Run GA
    print(f"\nGenetic Algorithm ({args.generations} gen, pop={args.population_size})\n")
    
    start = time.time()
    ga = GeneticAlgorithm(problem, args.population_size, args.mutation_rate, verbose=not args.quiet)
    best_solution, best_fitness = ga.evolve(args.generations)
    elapsed = time.time() - start
    
    solution = [int(x) for x in best_solution]
    _, utilities, start_times, completion_times = problem.evaluate_solution(solution)
    
    # Results
    print(f"\n{'='*50}")
    print("   RESULTS")
    print(f"{'='*50}")
    print(f"\nTime: {elapsed:.2f}s")
    print(f"Fitness (min utility): {best_fitness:.3f}")
    print(f"Average utility: {np.mean(utilities):.3f}")
    print(f"Bottleneck task: T{np.argmin(utilities)}")
    print(f"\nOptimal sequence: {solution}")
    
    # Comparison
    comparison = None
    if args.compare:
        comparison = compare_strategies(problem, best_fitness)
        print(f"\n{'='*50}")
        print("   STRATEGY COMPARISON")
        print(f"{'='*50}")
        for s, f in sorted(comparison.items(), key=lambda x: -x[1]):
            marker = " ★" if s == 'Genetic Algorithm' else ""
            print(f"  {s:20s}: {f:8.2f}{marker}")
    
    # Visualization
    if args.visualize:
        if comparison is None:
            comparison = compare_strategies(problem, best_fitness)
        visualize_results(problem, solution, ga, utilities, start_times, comparison)
    
    print(f"\n{'='*50}\n")
    return best_solution, best_fitness


if __name__ == "__main__":
    main()

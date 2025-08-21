# Genetic Task Scheduler

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Un'implementazione di algoritmi genetici per la risoluzione di problemi di scheduling single-machine con l'obiettivo di massimizzare il minimo beneficio tra tutti i clienti.


## 🎯 Descrizione del Problema

Il progetto risolve un problema di scheduling di **una singola macchina** utilizzata da **N clienti**, dove:

- Ogni cliente **j** ha un unico task da eseguire
- Ogni task ha un **release time** r_j (non può iniziare prima)
- La **utilità** del cliente j è: **u_j = b_j - a_j × c_j**
  - **b_j**: coefficiente di beneficio
  - **a_j**: coefficiente di penalità temporale
  - **c_j**: istante di completamento del task

### Obiettivo
Trovare la sequenza di esecuzione che **massimizza il minimo** delle utilità, ovvero che garantisce equità tra tutti i clienti:

```
max { min_j (u_j) }
```

## ✨ Caratteristiche

- 🧬 **Algoritmo Genetico Ottimizzato**
  - Order Crossover (OX) per permutazioni valide
  - Tournament Selection robusto
  - Strategia elitaria per convergenza rapida
  
- 📊 **Analisi Completa**
  - Tracking evolutivo in tempo reale
  - 9+ visualizzazioni dettagliate
  - Statistiche comprehensive
  
- 🔧 **Configurazione Flessibile**
  - Parametri dell'AG facilmente modificabili
  - Confronto automatico di configurazioni
  - Generazione problemi casuali
  
- 📈 **Visualizzazioni Avanzate**
  - Diagrammi di Gantt interattivi
  - Analisi convergenza algoritmica
  - Distribuzione utilità e performance


## 📖 Documentazione

### Classi Principali

#### `Task`
Rappresenta un singolo task con i suoi parametri.
```python
task = Task(
    id=0,
    release_time=2.5,    # r_j
    duration=3.0,        # d_j  
    benefit_coeff=50.0,  # b_j
    penalty_coeff=1.2    # a_j
)
```

#### `SchedulingProblem`
Gestisce la valutazione delle soluzioni.
```python
problem = SchedulingProblem(tasks_list)
objective, utilities, starts, completions = problem.evaluate_solution(sequence)
```

#### `GeneticAlgorithm`
Implementa l'algoritmo genetico ottimizzato.
```python
ga = GeneticAlgorithm(
    problem=problem,
    population_size=100,
    mutation_rate=0.1,
    crossover_rate=0.8,
    elite_size=20
)
```

### Metodi Chiave

| Metodo | Descrizione |
|--------|-------------|
| `create_individual()` | Genera permutazione casuale |
| `fitness(individual)` | Calcola fitness (min utility) |
| `tournament_selection()` | Selezione tramite torneo |
| `order_crossover()` | Crossover preservando permutazioni |
| `swap_mutation()` | Mutazione scambio posizioni |
| `evolve(generations)` | Esecuzione algoritmo completo |


## 🧬 Algoritmo

### Rappresentazione
- **Individuo**: Lista di interi rappresentante la permutazione dei task
- **Esempio**: `[2, 0, 4, 1, 3]` = Task 2 → Task 0 → Task 4 → Task 1 → Task 3

### Operatori Genetici

#### Order Crossover (OX)
```
Parent 1: [1|2 3 4|5 6 7]     Parent 2: [4|7 1 6|2 3 5]
             ↓                            ↓
Child 1:  [7|2 3 4|1 6 5]     Child 2:  [3|7 1 6|4 2 5]
```

#### Tournament Selection
- Seleziona k individui casuali
- Restituisce il migliore del torneo
- Bilanciamento pressione selettiva/diversità

#### Swap Mutation
- Scambia due posizioni casuali con probabilità `mutation_rate`
- Preserva validità permutazione

### Strategia Elitaria
- Conserva i migliori `elite_size` individui
- Garantisce non regressione
- Accelera convergenza

## ⚙️ Configurazione

### Parametri Algoritmo Genetico
```python
ga = GeneticAlgorithm(
    problem=problem,
    population_size=100,     # Dimensione popolazione
    mutation_rate=0.1,       # Probabilità mutazione
    crossover_rate=0.8,      # Probabilità crossover  
    elite_size=20            # Individui elitari conservati
)
```

### Parametri Problema
```python
problem = generate_random_problem(
    n_tasks=15,              # Numero task
    seed=42                  # Seed per riproducibilità
)
```

### Configurazioni Consigliate

| Scenario | Population | Mutation | Crossover | Elite |
|----------|------------|----------|-----------|-------|
| **Rapido** | 50 | 0.15 | 0.7 | 10 |
| **Standard** | 100 | 0.1 | 0.8 | 20 |
| **Accurato** | 200 | 0.05 | 0.85 | 30 |
| **Esplorativo** | 150 | 0.25 | 0.6 | 15 |



## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

---

## 📞 Contatti

**Autore**: [Gabriel Pentimalli]
- 📧 Email: gab.pentimalli@stud.uniroma3.it
- 💼 LinkedIn: [Gabriel Pentimalli](https://www.linkedin.com/in/gabriel-pentimalli-54180625a/)
- 🐙 GitHub: [@GabrielPentimalli](https://github.com/GabrielPentimalli)

---


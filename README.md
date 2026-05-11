*This project has been created as part of the 42 curriculum by hel-hamo.*

# Fly-In

## Description

Fly-In is a drone routing and flow simulation project. The goal is to transport a configurable number of drones from a start hub to an end hub through a network of hubs and connections while respecting zone rules and capacity constraints.

The project parses a custom map file, builds an internal graph, searches for feasible paths, computes the amount of flow that can travel on each path, and then simulates the movement of drones turn by turn until every drone reaches the destination.

## Instructions

### Requirements

- Python 3
- A virtual environment is recommended

### Installation

Use the provided Makefile to install the Python dependencies:

```bash
make install
```

This installs the packages listed in `requirements.txt` into the local virtual environment.

### Execution

Run the simulator by passing a map file as the single argument:

```bash
python3 main.py maps/easy/01_linear_path.txt
```

You can replace the sample map with any other file from the `maps/` directory or with your own compatible input file.

### Debugging

To inspect the program with Python's debugger:

```bash
python3 -m pdb main.py maps/easy/01_linear_path.txt
```

### Cleaning

Remove local cache and temporary Python files with:

```bash
make clean
```

## Algorithm Choices and Implementation Strategy

The implementation follows a graph-based strategy with a flow-oriented simulation layer.

1. The parser reads the input file, validates its syntax, and extracts the number of drones, the start hub, the end hub, regular hubs, and connections.
2. Each hub and connection stores metadata such as zone type, color, and capacity.
3. The graph builder assembles the parsed data into an adjacency structure and keeps hubs ordered by zone priority. Priority hubs are explored first, followed by normal hubs, then restricted hubs. Blocked hubs are ignored during path search.
4. The path search uses a breadth-first search to find a valid route from the start hub to the end hub while respecting current capacities.
5. The main algorithm is Edmonds-Karp inspired: it repeatedly searches for a path, computes the bottleneck flow along that path, stores the path-flow pair, and updates residual capacities on hubs and connections.
6. Paths are sorted by the number of turns before the simulation begins, so the engine can prefer efficient routes when distributing drones across multiple available paths.
7. During simulation, drones move turn by turn through the selected paths until the end hub contains all drones.

This strategy was chosen because it is simple to reason about, handles capacity-limited graphs naturally, and gives deterministic results for the provided maps.

## Visual Representation

The project includes a terminal visualizer that makes the simulation easier to follow.

- Each drone move is printed as it happens, so the progression of the swarm is visible in real time.
- Hub colors are taken from hub metadata and rendered with ANSI escape sequences.
- Connections are displayed with a blinking effect to distinguish edge traversal from hub arrival.
- A small per-character delay is used to make the movement feel animated rather than instant.

These visual cues improve the user experience by making route changes, bottlenecks, and drone progression easier to read during execution.

## Resources

### References

- Breadth-first search and shortest-path basics: https://www.tutorialspoint.com/data_structures_algorithms/breadth_first_traversal.htm
- Edmonds-Karp algorithm: https://www.tutorialspoint.com/graph_theory/graph_theory_edmonds_karp_algorithm.htm
- Python `pdb` debugger: https://docs.python.org/3/library/pdb.html
- Python `re` regular expressions: https://docs.python.org/3/library/re.html
- ANSI escape codes for terminal color: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- ANSI escape codes for terminal color: https://cis106.com/bash/ANSI_escape_sequences/

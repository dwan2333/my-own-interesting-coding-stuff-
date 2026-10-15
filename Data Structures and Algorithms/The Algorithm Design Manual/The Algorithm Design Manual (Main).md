# The Algorithm Design Manual

_Steven S. Skiena · 3rd edition (Springer, 2020)_

A manual on **designing** algorithms for problems that come up in practice, for students and working programmers. It has two parts:
- **Part I, Practical Algorithm Design**, teaches the techniques.
- **Part II, The Hitchhiker's Guide to Algorithms**, is a catalog of the 75 most important algorithmic problems, to look up when one comes up.

Throughout Part I, **war stories** show the techniques used on real problems Skiena worked on. Each chapter ends with exercises, including interview problems. Sections marked (*) are advanced.

---

## Part I — Practical Algorithm Design

| Chapter | What it covers |
|---|---|
| **1. Introduction to Algorithm Design** | Algorithms vs. heuristics (robot tour optimization, selecting jobs); reasoning about correctness: counterexamples, induction and recursion, proof by contradiction; modeling a problem with standard structures (permutations, subsets, trees, graphs, points, polygons, strings); estimation. **My notes:** [The closest-pair heuristic](<2026-10-15 - The closest-pair heuristic.md>) (§1.1) |
| **2. Algorithm Analysis** | The RAM model of computation; Big Oh notation; growth rates and dominance relations; working with Big Oh; reasoning about efficiency; summations; logarithms and their uses; advanced analysis (*) |
| **3. Data Structures** | Contiguous vs. linked structures; stacks and queues; dictionaries; binary search trees; priority queues; hashing; specialized data structures |
| **4. Sorting** | Applications and pragmatics of sorting; heapsort; mergesort (divide and conquer); quicksort (randomization); distribution sort (bucketing) |
| **5. Divide and Conquer** | Binary search and related algorithms; recurrence relations and how to solve them; fast multiplication; largest subrange and closest pair; parallel algorithms; convolution (*) |
| **6. Hashing and Randomized Algorithms** | Probability review; balls and bins; why hashing is randomized; Bloom filters; the birthday paradox and perfect hashing; minwise hashing; efficient string matching; primality testing; where random numbers come from |
| **7. Graph Traversal** | Kinds of graphs; data structures for graphs; breadth-first search and its applications; depth-first search and its applications; DFS on directed graphs |
| **8. Weighted Graph Algorithms** | Minimum spanning trees; shortest paths; network flows and bipartite matching; randomized min-cut; "design graphs, not algorithms" |
| **9. Combinatorial Search** | Backtracking and examples; search pruning; Sudoku; best-first search; the A* heuristic |
| **10. Dynamic Programming** | Caching vs. computation; approximate string matching (edit distance); longest increasing subsequence; subset sum; the ordered partition problem; parsing context-free grammars; where dynamic programming fails (TSP) |
| **11. NP-Completeness** | Problems and reductions; reductions for algorithms; elementary hardness reductions; satisfiability; creative reductions from SAT; the art of proving hardness; **P vs. NP** (§11.9: the classes P and NP, NP-hard vs. NP-complete) |
| **12. Dealing with Hard Problems** | Approximation algorithms (vertex cover, Euclidean TSP, set cover); when average is good enough; heuristic search (random sampling, local search, simulated annealing); genetic algorithms; quantum computing |
| **13. How to Design Algorithms** | A step-by-step checklist of questions for attacking a new problem; preparing for tech company interviews |

---

## Part II — The Hitchhiker's Guide to Algorithms

Each entry gives the problem's input and output, what is known about it, and where to find implementations.

| Chapter | Problems in the catalog |
|---|---|
| **14. A Catalog of Algorithmic Problems** | How to use the catalog |
| **15. Data Structures** | Dictionaries · priority queues · suffix trees and arrays · graph data structures · set data structures · kd-trees |
| **16. Numerical Problems** | Linear equations · bandwidth reduction · matrix multiplication · determinants and permanents · optimization · linear programming · random number generation · factoring and primality testing · arbitrary-precision arithmetic · knapsack · discrete Fourier transform |
| **17. Combinatorial Problems** | Sorting · searching · median and selection · generating permutations, subsets, partitions and graphs · calendrical calculations · job scheduling · satisfiability |
| **18. Graph Problems: Polynomial Time** | Connected components · topological sorting · minimum spanning tree · shortest path · transitive closure and reduction · matching · Eulerian cycle / Chinese postman · edge and vertex connectivity · network flow · drawing graphs and trees · planarity |
| **19. Graph Problems: NP-Hard** | Clique · independent set · vertex cover · traveling salesman · Hamiltonian cycle · graph partition · vertex and edge coloring · graph isomorphism · Steiner tree · feedback edge/vertex set |
| **20. Computational Geometry** | Geometric primitives · convex hull · triangulation · Voronoi diagrams · nearest-neighbor search · range search · point location · intersection detection · bin packing · medial-axis transform · polygon partitioning and simplification · shape similarity · motion planning · line arrangements · Minkowski sum |
| **21. Set and String Problems** | Set cover · set packing · string matching · approximate string matching · text compression · cryptography · finite-state machine minimization · longest common substring/subsequence · shortest common superstring |
| **22. Algorithmic Resources** | Algorithm libraries · data sources · online bibliographic resources · consulting services |

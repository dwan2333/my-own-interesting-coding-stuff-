# `ClosestPair` — Connecting the Closest Endpoints of Different Chains

_Question I had while studying · The Algorithm Design Manual (Skiena), §1.1 Robot Tour Optimization · asked 2026-10-15_

What does "for each pair of endpoints $(s, t)$ from distinct vertex chains" mean, how does it fit with the `if` line under it, and why is this a reasonable way to plan a robot's tour?

> [!info] Question Essence
> The robot must visit every point and come back to the start along the shortest closed tour. ClosestPair builds that tour from small pieces called **chains** (paths of points joined by edges). Every point starts as its own chain. In each round, the two lines work together: the `for` line lists every **allowed** connection (one chain's endpoint to another chain's endpoint), and the `if` line keeps the **shortest** of them, the usual "find the minimum" pattern. After $n-1$ rounds everything is one chain, and joining its two ends closes the tour. The "endpoints" and "distinct chains" rules guarantee the result is a single loop through every point. It's a **heuristic**: it fixes nearest-neighbour's zigzag on Skiena's line of points, but it can still be about 20% longer than the best tour.

---

## The Question

![ClosestPair pseudocode, ADM §1.1](<2026-10-15 - The closest-pair heuristic.png>)

---

## What a Chain and an Endpoint Are

| Term             | Meaning                                                                        | Example                         |
| ---------------- | ------------------------------------------------------------------------------ | ------------------------------- |
| **Vertex chain** | A path: points joined one after another by edges, with no branches and no loop | $-1 - 0 - 1$                    |
| **Endpoint**     | A point at either end of a chain, with 0 or 1 edges so far                     | $-1$ and $1$ in the chain above |
| **Middle point** | A point with 2 edges already                                                   | $0$ above                       |
| **Single point** | A chain of length 0, so it is **both** of its own endpoints                    | Every point at the start        |

The goal is one chain through all $n$ points (a path), then one last edge to turn it into a loop (the tour).

---

## How the Two Lines Work Together

Each round of the outer loop adds exactly one edge. Inside a round:

```
d = ∞                                    # best distance found so far: nothing yet
for each pair of endpoints (s, t) from distinct vertex chains:   # every ALLOWED connection
    if dist(s, t) ≤ d:                   # at least as close as the best so far?
        s_m, t_m, d = s, t, dist(s, t)   # remember it
connect (s_m, t_m)                       # add the closest allowed edge
```

- **The `for` line decides *which* pairs are allowed.** It's a filter, not a calculation.
- **The `if` line picks the *shortest* allowed pair.** It's the standard "find the minimum" scan: start with $d = \infty$, and every time you see something closer, remember it. After the scan, $(s_m, t_m)$ is the closest allowed pair. With `≤`, a later pair of equal distance replaces an earlier one, which only matters for ties.

**Why both rules are needed:**
- **Only endpoints.** A middle point already has two edges. A third edge would make a branch, and a robot can't follow a branching path in one pass.
- **Only distinct chains.** If $s$ and $t$ were the two ends of the *same* chain, connecting them would close a small loop early, and the points outside it could never be joined.

So every edge joins two separate chains end to end. The number of chains drops by exactly one per round: $n$ single points, then $n-1$ rounds, then one chain.

---

## Walking Through Skiena's Line of Points (Figure 1.3)

Points at $-21, -5, -1, 0, 1, 3, 11$ on a line. Nearest-neighbour fails here, hopping left-right-left over 0. ClosestPair grows one chain outward from the middle:

| Round | Closest allowed pair | Distance | Chain(s) afterwards |
|---|---|---|---|
| 1 | $0 - 1$ | 1 | $0-1$ |
| 2 | $-1 - 0$ | 1 | $-1-0-1$ |
| 3 | $1 - 3$ | 2 | $-1 \dots 3$ |
| 4 | $-5 - (-1)$ | 4 | $-5 \dots 3$ |
| 5 | $3 - 11$ | 8 | $-5 \dots 11$ |
| 6 | $-21 - (-5)$ | 16 | $-21 \dots 11$ (one chain) |
| close | $-21 - 11$ | 32 | the tour |

Total $1+1+2+4+8+16+32 = 64$, which is the **optimal** tour here: walk right, then come straight back.

---

## Why It's Still Not a Correct Algorithm (Figure 1.4)

Two rows of 3 points: the rows are $1-e$ apart, and points within a row are $1+e$ apart. The closest pairs are therefore the vertical ones *across* the gap, so ClosestPair joins those first, then links them in a zigzag. The final closing edge has to run diagonally across the whole board. The best tour simply goes around the outside.

With $e = 0.01$: ClosestPair gives **7.240**, while the best tour is **6.020**, about **20% longer**. Skiena notes that other examples are much worse.

> [!warning] Heuristic vs. algorithm
> Skiena's take-home lesson: an **algorithm** always produces a correct result, while a **heuristic** usually does a good job, with no guarantee. The only sure way he gives in §1.1 is to try all $n!$ orderings (`OptimalTSP`), which is hopeless beyond about 20 points ($20! \approx 2.4\times10^{18}$). This is the **traveling salesman problem**, and the book returns to it many times.

---

## Run It Yourself

```python
from itertools import permutations
from math import dist, inf


def closest_pair_tour(points):
    """Skiena's ClosestPair heuristic. Returns the tour as a list of edges (index pairs)."""
    n = len(points)
    chain = list(range(n))   # chain[i]: which chain point i is in (each point starts alone)
    degree = [0] * n         # 0 or 1 edges: an endpoint; 2 edges: a middle point
    edges = []
    for _ in range(n - 1):                         # For i = 1 to n - 1
        d, best = inf, None                        #   d = infinity
        for s in range(n):                         #   every pair of endpoints...
            for t in range(s + 1, n):
                if degree[s] < 2 and degree[t] < 2 and chain[s] != chain[t]:   # ...from distinct chains
                    if dist(points[s], points[t]) <= d:                       # closest so far?
                        d, best = dist(points[s], points[t]), (s, t)
        s, t = best
        edges.append(best)                         #   connect (s_m, t_m)
        degree[s] += 1
        degree[t] += 1
        old = chain[t]
        chain = [chain[s] if c == old else c for c in chain]   # merge the two chains
    s, t = [i for i in range(n) if degree[i] < 2]  # the last chain's two ends
    edges.append((s, t))                           # close the tour
    return edges


def length(points, edges):
    return sum(dist(points[a], points[b]) for a, b in edges)


line = [(x, 0) for x in (-21, -5, -1, 0, 1, 3, 11)]
print(length(line, closest_pair_tour(line)))      # 64.0
```

**Cost:** each of the $n-1$ rounds checks about $n^2/2$ pairs, so this direct version takes about $n^3$ steps. Fine for a robot arm with a few hundred points; slow for millions.

> [!tip] Spotting the pattern
> "Set $d = \infty$, scan, keep the best" appears all over the book (OptimalTSP and ExhaustiveScheduling in §1.1–1.2 use it too). When you see it, read it as one line: *pick the best candidate*.

---

> [!tip] Key Takeaway
> The `for` line lists the allowed moves (join one chain's end to another chain's end), and the `if` line picks the shortest of them. Repeating that $n-1$ times and closing the loop always gives a valid tour, often a good one, but not always the best, which makes it a heuristic, not an algorithm.

---

## Related Documents

- **[The Algorithm Design Manual](<The Algorithm Design Manual (Main).md>)** — the book's overview: structure, level, and how to practise alongside it.
- **[Data Structures and Algorithms Using Python](<Data Structures and Algorithms Using Python (Main).md>)** — notes from the Necaise Python book, for implementing the basic data structures.

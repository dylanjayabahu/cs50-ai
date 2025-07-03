**Frontier** = the nodes u are able to search

- If frontier is a **stack**, u get **DFS** (hence recursive approaches often give DFS)
- If frontier is a **queue**, u get **BFS**
- If u select from frontier based on lowest **h(n)** (heuristic) alone, u get **Greedy Best First Search (GBFS)**
- If u select from frontier based on lowest **g(n)** (cost to reach node) alone, u get **Dijkstra's Algo** (hehe Mr. Schattman)
  - note that dijkstra's always solves optimally, because it doesn't stop when u reach the goal, but rather when the frontier is empty
- Instead, if u select from frontier based on lowest **g(n) + h(n)** [g(n) is cost to get to the node], u get **A\***
  - will find optimal assuming:
    - an **admissible heuristic**; admissible = never overestimates, only underestimates
    - a **consistent heuristic**; h(n) ≤ cost(n→n') + h(n')  
      → "You shouldn’t think you're closer at n than you'd think you are after taking one step to a neighbor."  
      → all consistent heuristics are also admissible, but not vice versa
  - note: if the range of **g(n)** is much higher than **h(n)**, g(n) will dominate and it is closer to Dijkstra's.  
    similarly, if **h(n)**'s range is much higher than **g(n)**, h(n) will dominate and it is closer to GBFS.  
    To avoid this, a **properly scaled heuristic** is important.

---

### Search Algorithm Comparison

| Algorithm                      | Frontier Priority (f(n)) | Uses Heuristic? | Guaranteed Optimal?              |
| ----------------------------- | ------------------------ | ----------------| -------------------------------- |
| **DFS (Depth-First Search)**   | LIFO (stack)             | ❌ No           | ❌ No                             |
| **BFS (Breadth-First Search)** | FIFO (queue)             | ❌ No           | ✅ Yes (if all edge costs equal) |
| **Dijkstra's Algorithm**       | `g(n)`                   | ❌ No           | ✅ Yes                            |
| **Greedy Best-First Search**   | `h(n)`                   | ✅ Yes          | ❌ No                             |
| **A\* Search**                 | `g(n) + h(n)`            | ✅ Yes          | ✅ Yes (if `h` is admissible)     |

---

## Adversarial Search

**Minimax** – 2 players, each tries to make the other lose:
- each state is assigned a score  
  - if terminal, just use utility function (e.g. 1 = win, 0 = draw, -1 = lose for p1)  
  - else, recursively see what max/min player would do  
- p1 **maximizes** score, p2 **minimizes** score

**Minimax is computationally intense** – have to search every possible outcome

**Alpha-beta pruning** = optimization to skip some recursive branches if they are useless anyways  
(e.g. we already have a better option)  
→ still isn't great tho

**Depth-limited minimax**
- stop after a certain depth
- instead of assigning score based on terminal state, use an **evaluation function** to estimate the utility of a game state
- better eval function gives better AI

---

**CS50's more comprehensive notes:**  
👉 [https://cs50.harvard.edu/ai/2024/notes/0/](https://cs50.harvard.edu/ai/2024/notes/0/)

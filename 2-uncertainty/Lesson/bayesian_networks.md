## Full cs50 notes: https://cs50.harvard.edu/ai/notes/2/

---

## Bayesian Net

= data structure that represents the dependencies among random variables.

---

## Bayesian networks have the following properties:

- They are directed graphs.  
- Each node on the graph represent a random variable.  
- An arrow from X to Y represents that X is a parent of Y. That is, the probability distribution of Y depends on the value of X.  
- Each node X has probability distribution P(X | Parents(X)).  
    => with the exception that the root node's distribution is not conditoinal  
    => (there are no parents that influence it)

---

The bayesian network encodes direct relationships as edges between nodes

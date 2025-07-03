**CS50 notes**: https://cs50.harvard.edu/ai/2024/notes/1/

---

## Knowledge-Based Agents
- Operate on representations of logic

---

## Propositional Logic
Based on true/false statements about the world.

- **Propositional symbols** = P, Q, R, etc. representing a statement  
- **Logical connectives** connect the symbols (e.g. not / and / or / implication etc)

### Logical Connectives

#### Not / And / Or  
Same as with Boolean logic.

#### Implications (`->`)
- `p -> q`: If `p` is true, `q` is also true (p implies q)
    - But not necessarily the other way around
    - There is no claim regarding `p` being false, so `p -> q` is always true if `p` was false

**Truth Table:**

| p | q | p → q |
|---|---|--------|
| T | T | T      |
| T | F | F      |
| F | T | T      |
| F | F | T      |

#### Biconditional (`<->`)
- `p <-> q`: q is true **if and only if** p is true.
- Equivalent to implication both ways:  
  `p ↔ q ≡ (p → q) ∧ (q → p)`

**Truth Table:**

| p | q | p ↔ q |
|---|---|--------|
| T | T | T      |
| T | F | F      |
| F | T | F      |
| F | F | T      |

#### Entailment (`|=`)
- `a |= b`: In every model where `a` is true, `b` is true
- Kinda like implication but not really  
- **Tautology** = true in every situation  
- So, if `a |= b`, then `a -> b` is a tautology; it's true in every situation

---

## Inference
Deriving new logical sentences from given ones.  
→ Does `KB |= a`? (does the knowledge base entail some statement a?)

---

## Model Checking
- Enumerate all possible models  
  (2ⁿ models with n propositional symbols)  
- If every model where KB is true, a is true, then `KB |= a`  
- Quite inefficient for more variables

---


## Inference Rules - take knowledge that exists and translate into new knowledge

- Many inference rules take a logical connection and transform it into other logical connections
- illustrated in the form  
  GIVEN  
  \_\_\_\_\_\_\_\_\_\_  
  CONCLUSION

### 1. Modus Ponens: (Latin for "method of affirming")  
a -> b  
a  
\_\_\_\_  
b

### 2. And Elimination:  
a and b  
\_\_\_\_  
a  
(and similarly, b)

### 3. Double Negation Elimination:  
! (!a)  
\_\_\_\_\_\_\_\_\_  
a

### 4. Implication Elimination  
a -> b  
\_\_\_\_\_\_  
!a or b

### 5. Biconditional Elimination  
a <-> b  
\_\_\_\_  
a -> b  
b -> a

### 6. De Morgan's Laws  

!(a and b)  
\_\_\_\_\_\_\_\_\_\_  
!a or !b

!(a or b)  
\_\_\_\_\_\_\_\_\_  
!a and !b

### 7. Distributive Law  

a and (b or c)  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
(a and b) or (a and c)

a or (b and c)  
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
(a or b) and (a or c)

---

## Theorem proving is a form of search problem:

- initial state is knowledge base;  
- actions is inference rules  
- goal test is checking the statement we wanna prove  
- path cose is number of steps taken

^ this is another way, typically more efficient than model checking, to determine entailement

---

## Resolution = yet another way to determine entailment

- complimentary literals = two statements that are opposites (e.g. a and !a)  
- based on the Unit Resolution Rule:

p or q
!p
\_\_\_\_\_\_\_\_
q

> the p and the !p kinda cancel out

can be extended:

p or (q1 or q2 or q3 ...)
!p
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
q1 or q2 or q3 ...

we can further generalize:

p or q
!p or r
\_\_\_\_\_\_\_\_\_\_
q or r

which can also be extended:

p or q1 or q2 or q3 ...
!p or r1 or r2 or r3 ...
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
q1 or q2 or q3 ... or r1 or r2 or r3 ...



---

## Clause = a disjunction of literals

- disjunction = things connected with ors  
    -> clause = an "or-only" sentence  
- conjunction = things connected with and

---

## Conjunctive Normal Form (CNF) = logical sentence that is a conjunction of clauses

- a bunch of or-sentences connected with ands  
- basically, represented using only ands/ors  
    -> any sentence can be converted to this w/ infernence rules  
    -> very easy to work when when in (CNF)

---

### Converting to CNF:

1. eliminate biconditionals (a<->b into a->b and b->a); biconditional elimination  
2. eliminate implicaitons (a->b into !a or b); implication elimination  
3. move nots inwards (!(a and b) into !a or !b); demorgans laws  
4. Use distributive law to distribute ors wherever possible  

Once we have CNF, we can easily put each clause into the Unit Resolution Rule

---

### Factoring: removing duplicate variables

- e.g. (a or b or c or a) into (a or b or c)

---

### Empty clause = always false

-> if I try to resolve contradicotry terms, I will get the empty clause

---

## Inference by Resolution

- Goal is to prove that KB |= a  
    - We can use proof by contradiction  
    - If (KB and !a) is a contradiction, then KB |= a  
        else, if no contradiction, KB does not entail a

1. convert (KB and !a) to CNF  
2. Use Unit Resolution wherever possible to make a new clause (loop)  
    - If we produce the empty clause, there is a contradiction ==> yay, KB |= a  
    - If we cannot make any new clauses with Unit Resolution, there is no entailment

---

## First-order logic

- more powerful than propositional logic (true/false)

### Constnat Symbols and Predicate Symbols

- constant symbol = objects  
    e.g. Minerva, Horace, Griffindor, etc.  
- predicate symbol = relation/function that takes an argument and returns true and false  
    e.g. House, Person, BelongsTO  
    - House(griffindor) means griffindor is a house  
    - Person(minerva) means minerva is a person  
    - BelongsTo(minerva, griffindor) means minerva belongs to griffindor

---

### Quantification = representing sentences without using a specific constant symbol

#### Universal Quantification

- uses the "∀", for all  
- ∀x. BelongsTo(x, Gryffindor) → ¬BelongsTo(x, Hufflepuff)  
- ^ means that for all x that belong to griffindor, they dont belong to Hufflepuff

#### Existential Quantification

- uses the "∃", there exists  
- ∃x. House(x) ∧ BelongsTo(Minerva, x)  
- ^ means that there exists an x that is a house and that minerve belongs to

- U can make much more complicated statements with these quantifications

---

There are lots of other higher order logics out there as well

## Conditional Probability:

P(a | b) = P(a n b) / P(b)
= alpha * P(a n b)

- conditional probability is proportional to joint probability  
- alpha = 1 / P(b)

> Rearranged:

P(a ∩ b) = P(b) P(a | b) (1)

> Swap a and b:

P(b ∩ a) = P(a) P(b | a) = P(a ∩ b) (2)

> set (1) = (2)

P(a) P(b|a) = P(b) P(a|b)

> rearrange for P(b|a)

P(b|a) = P(b) P(a|b) / P(a)

> this is bayes rule

### Bayes Rule:

P(b|a) = P(b) P(a|b) / P(a)

---

### Independence:

P(a ∩ b) = P(a) P(b) if and only if a, b are independent

---

### Negation:

P(not a) = 1 - P(a)

---

### Inclusion-Exclusion:

P(a ∪ b) = P(a) + P(b) - P(a ∩ b)


---

## Marginalization:

P(a) = P(a, b) + P(a, not b)

More generally, if b (and a) are not binary:

P(A = a) = SUM_j [ P(A = a, B = b_j) ]

---

## Conditioning:

P(a) = P(a | b) P(b) + P(a | ¬b) P(¬b)

Again, if b (and a) are not binary:

P(A = a) = SUM_j [ P(A = a | B = b_j) * P(B = b_j) ]
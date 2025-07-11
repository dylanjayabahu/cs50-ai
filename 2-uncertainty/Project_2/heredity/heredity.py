import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    p = 1

    for name in people.keys():
        gene = 1 if name in one_gene else 2 if name in two_genes else 0
        trait = name in have_trait
        
        person = people[name]

        if person["mother"]:
            # has parents 
            mom = person["mother"]
            dad = person["father"]

            # M and D is the chance that the parent gave the gene to the child (M for mom, D for dad)
                # if a parent has one gene, prob = 0.5 for them giving child the gene 
                # if a parent has two genes, prob = 1-mutation_chance for them giving child the gene 
                # if a parent has no genes, prob = mutation_chance for them giving child the gene 

            M = 0.5 if mom in one_gene else (1-PROBS["mutation"]) if mom in two_genes else PROBS["mutation"]
            D = 0.5 if dad in one_gene else (1-PROBS["mutation"]) if dad in two_genes else PROBS["mutation"]

            if gene == 0:
                pgene = (1-M)*(1-D) # chance of 0 from mom and 0 from dad
            elif gene == 1:
                pgene = (M)*(1-D) + (D)*(1-M) # chance of 1 from mom and 0 from dad OR 1 from dad and 0 from mom
            else:
                pgene = M*D # chance of 1 from mom and 1 from dad
        
        else:
            # doesn't specify parents
            pgene = PROBS["gene"][gene]     
       
            
        ptrait = PROBS["trait"][gene][trait] # probability of them being in their trait group (unreliant on parents)
        p *= pgene * ptrait # probability of the person being in both the gene group and trait group:

    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        probabilities[person]["gene"][2] += p if person in two_genes else 0 
        probabilities[person]["gene"][1] += p if person in one_gene else 0 
        probabilities[person]["gene"][0] += p if person not in two_genes and person not in one_gene else 0

        probabilities[person]["trait"][True] += p if person in have_trait else 0 
        probabilities[person]["trait"][False] += p if person not in have_trait else 0 


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"].keys():
            probabilities[person]["gene"][gene] /= gene_total
        
        trait_total = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"].keys():
            probabilities[person]["trait"][trait] /= trait_total


if __name__ == "__main__":
    main()

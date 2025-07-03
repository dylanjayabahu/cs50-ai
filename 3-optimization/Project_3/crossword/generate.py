import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.crossword.variables:
            removed_domain_values = set()
            for domain_value in self.domains[variable]:
                if len(domain_value) != variable.length:
                    removed_domain_values.add(domain_value)
            
            self.domains[variable] -= removed_domain_values


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        
        i, j = overlap # (i, j), where x's ith character overlaps y's jth character

        to_remove = set()
        revised = False

        for x_value in self.domains[x]:
            if not any([x_value[i]==y_value[j] for y_value in self.domains[y]]):
                to_remove.add(x_value)
                revised = True
                
        self.domains[x] -= to_remove 
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = list(self.crossword.overlaps.keys())
        
        while len(arcs) > 0:
            x, y = arcs.pop() # we want to make x consistent with y

            if self.revise(x, y):
                # we made a change

                # first check if the we found the problem to be unsolveable
                if len(self.domains[x]) == 0:
                    return False

                # We need to re-add (Z, X) to the queue for any Z that is a neighbour of X, Z!=Y
                for z in self.crossword.neighbors(x) - {y}:
                    arcs = [(z, x)] + arcs
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        seen_values = set()
        
        for var in assignment.keys():
            
            if var.length != len(assignment[var]) or assignment[var] in seen_values:
                return False

            for var2 in self.crossword.neighbors(var):
                if var2 not in assignment.keys():
                    continue
                    
                i, j = self.crossword.overlaps[var, var2]
                if assignment[var][i] != assignment[var2][j]:
                    return False

            seen_values.add(assignment[var])

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        var_domain = list(self.domains[var]) # domain of var as a list

        def num_rules_out(x_value):
            n = 0
            # returns how many values would be ruled out if var had a value of var_value
            for var2 in self.crossword.neighbors(var):
                if var2 in assignment.keys():
                    continue 
                    
                i, j = self.crossword.overlaps[var, var2]
                for y_value in self.domains[var2]:
                    n += 1 if x_value[i] != y_value[j] else 0

            return n

        return sorted(var_domain, key=num_rules_out)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # we don't need to sort (O(nlogn)), we can just traverse the list of vars once to find the min (O(n))

        mrv = float('inf')
        degree = 0
        best_var = None

        for variable in self.crossword.variables:
            if variable in assignment:
                continue
            
            if len(self.domains[variable]) < mrv:
                mrv = len(self.domains[variable])
                degree = len(self.crossword.neighbors(variable))
                best_var = variable

            elif len(self.domains[variable]) == mrv:
                new_degree = len(self.crossword.neighbors(variable))
                if new_degree > degree:
                    # mrv doesn't change 
                    degree = new_degree 
                    best_var = variable


        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value 

            if self.consistent(assignment):
                # run ac3 here
                ac3_success =  self.ac3(arcs = [(y, var) for y in self.crossword.neighbors(var)])
                if ac3_success:
                    # add any new ac3 inferences to the assignment
                    for var in self.domains.keys():
                        if len(self.domains[var]) == 1:
                            assignment[var] = list(self.domains[var])[0]

                    # backtrack now 
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                    
                # if ac3 wasn't a success, or the result of backtrack is None, this option didn't work
                del assignment[var]

        # if we went through all the options and none worked, this is a dead end 
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

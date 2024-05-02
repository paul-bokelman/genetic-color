from random import randint
import math

# genome -> collection of genes
# gene -> function

class Organism:
    def __init__(self) -> None:
        r = self.random_gene(8)
        g = self.random_gene(8)
        b = self.random_gene(8)
        self.genome = (r, g, b)
        pass

    def fitness(self, target_color): # distance from target color
        # treat colors as vectors and minimize distance
        distance = math.sqrt(
            math.pow(target_color[0] - self.phenotype(self.genome[0]), 2) + math.pow(target_color[1] - self.phenotype(self.genome[1]), 2) + math.pow(target_color[2] - self.phenotype(self.genome[2]), 2)
        )

        return distance
    
    # convert binary gene to decimal (color value)
    def phenotype(self, gene): 
        value = 0
        for (i, n) in enumerate(reversed(list(gene))):
            if(int(n) == 1):
                value += int(math.pow(2, i))
        return value
    
    def random_gene(self, length):
        gene = []
        # 8 bit gene (0-255)
        for _ in range(length):
            gene.append(randint(0, 1))
        # return as binary string 
        return ''.join(map(str, gene))
    def full_phenotype(self):
        return (self.phenotype(self.genome[0]), self.phenotype(self.genome[1]), self.phenotype(self.genome[2]))
    def mutate(self):
        char_mutation_chance = 0.3
        for gene in self.genome:
            lg = list(gene)
            if(randint(0, 10) <= char_mutation_chance * 10):
                index = randint(0, len(gene) - 1)
                lg[index] = str((1 if int(lg[index]) == 0 else 0))
                gene = "".join(lg)

    

class Species:
    # initialize organisms to start evolving
    def __init__(self, n_total, target_color) -> None:
        self.n_total = n_total
        self.organisms = []
        self.generations = 0
        self.target_color = target_color

        for _ in range(n_total):
            self.organisms.append(Organism())

    # progress to next generation
    def evolve(self):
        # remove out 50% worst, replace with 50% best (with random mutations)
        next_gen = self.organisms

        for i in range(len(next_gen)):
            for j in range(0, len(next_gen) - i - 1):
                if next_gen[j].fitness(self.target_color) > next_gen[j + 1].fitness(self.target_color):
                    temp = next_gen[j]
                    next_gen[j] = next_gen[j+1]
                    next_gen[j+1] = temp


        # remove lower half of organisms
        proceeding_organisms = next_gen[0:int(len(next_gen) /  2)]
        new_organisms = []
        self.organisms = proceeding_organisms

        # add new organisms with chance of mutation
        mutation_chance = 0.4
        for proceeding_organism in proceeding_organisms:
            if(randint(0, 10) <= mutation_chance * 10):
                proceeding_organism.mutate()
                new_organisms.append(proceeding_organism)
            else:
                new_organisms.append(proceeding_organism)

        self.organisms = [*proceeding_organisms, *new_organisms]
    
    def reached_solution(self):
        return self.organisms[0].fitness(self.target_color) == 0
    
    def set_target_color(self, target_color):
        self.target_color = target_color

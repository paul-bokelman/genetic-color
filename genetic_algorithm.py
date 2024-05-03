from typing import Optional, Dict
from random import randint
import math
from utils import chance, random_exclude

class Organism:
    def __init__(self, genome: Optional[tuple[str, str, str] ] = None) -> None:
        self.internal_mutation_probability = 0.3 # mutation probability for gene in genome (should be in config)

        if genome != None:
            self.genome = genome
        else:
            r = self.random_gene(8)
            g = self.random_gene(8)
            b = self.random_gene(8)
            self.genome = (r, g, b)

    # calculate how well an organism is doing (the lower the best)
    def fitness(self, target_color):

        # treat colors as vectors and minimize distance (that's why it's lower)
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
    
    # create random gene with n bits (8 for this)
    def random_gene(self, length):
        gene = []
        for _ in range(length):
            gene.append(randint(0, 1))
        return ''.join(map(str, gene))
    
    # return full phenotype (rgb color)
    def full_phenotype(self):
        return (self.phenotype(self.genome[0]), self.phenotype(self.genome[1]), self.phenotype(self.genome[2]))
    
    # mutate genome by randomly changing bits in genome
    def mutate(self):
        new_genome = []

        for gene in self.genome: # less computation but still lot's of variety
            if(chance(self.internal_mutation_probability)):
                # choose a random bit and flip it's value
                gene_str = list(gene)
                bit_index = randint(0, 7)
                gene_str[bit_index] = str((1 if int(gene_str[bit_index]) == 0 else 0))
                new_genome.append("".join(gene_str))
            else:
                new_genome.append(gene)

        self.genome = (new_genome[0], new_genome[1], new_genome[2])

class Species:
    # initialize organisms to start evolving
    def __init__(self, genetic_config: Dict[str, int], target_color: tuple[int, int, int]) -> None:
        self.n_organisms = genetic_config['n_organisms']
        self.organisms: list[Organism] = []
        self.generation = 0
        self.target_color = target_color
        self.tournament_proportion = genetic_config['tournament_proportion']
        self.mutation_probability = genetic_config['mutation_probability']
        self.genesis()

    # progress to next generation
    def evolve(self):
        # tournament selection -> crossover -> mutation
        self.generation += 1
        # select % of population to duel, winners crossover, losers removed from pool
        candidates: list[Organism] = []

        # tournament selection for crossover candidates
        for _ in range(math.floor((self.n_organisms * self.tournament_proportion) / 2)):
            p1_index = randint(0, len(self.organisms) - 1)
            participant1 = self.organisms[p1_index] 
            p2_index = random_exclude(p1_index)
            participant2 = self.organisms[p2_index]

            # whoever has better fitness is added to candidate pool, loser is removed from species
            if(participant1.fitness(self.target_color) < participant2.fitness(self.target_color)):
                candidates.append(participant1)
                self.organisms.pop(p2_index)
            else:
                candidates.append(participant2)
                self.organisms.pop(p1_index)

        # uneven number of candidates, add 1 
        if(len(candidates) % 2 != 0):
            candidates.append(self.organisms[randint(0, len(self.organisms) - 1)])

        candidate_middle_index = int(len(candidates) / 2)

        # crossover for all pairs of candidates
        for (parent1, parent2) in zip(candidates[:candidate_middle_index], candidates[candidate_middle_index:]):
            self.crossover(parent1, parent2)

    
    # split genome in random place and combine with chance of mutation 
    def crossover(self, parent1: Organism, parent2: Organism):
        position = randint(0, 23) # choose position between 1-24 (3 genes of length 8)

        parent1_genome_str = "".join(parent1.genome)
        parent2_genome_str = "".join(parent2.genome)
        (parent1_l_genome,parent1_r_genome) = (parent1_genome_str[:position], parent1_genome_str[position:])
        (parent2_l_genome,parent2_r_genome) = (parent2_genome_str[:position], parent2_genome_str[position:])

        # created 2 children (with chance of mutation) from spliced genome
        for combined_genome in ([parent1_l_genome + parent2_r_genome, parent2_l_genome + parent1_r_genome]):
            child = Organism((combined_genome[:8], combined_genome[8:16], combined_genome[16:]))
            if chance(self.mutation_probability):
                child.mutate()
            self.organisms.append(child)

    # find the most fit organism from pool
    def best(self):
        best = self.organisms[0]
        for organism in self.organisms:
            if organism.fitness(self.target_color) < best.fitness(self.target_color):
                best = organism

        return best

    # check if the best organism's phenotype matches the target color
    def reached_solution(self):
        return self.best().fitness(self.target_color) == 0
    
    # initiate a new set of generations
    def genesis(self):
        self.generation = 0
        self.organisms = []
        for _ in range(self.n_organisms):
            self.organisms.append(Organism())
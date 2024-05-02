import pygame
from genetic_algorithm import Species
from random import randint

# genetic algorithm
# - generate population, score population, sort and remove bad, mutate randomly
# - store generations
# show generations visually


pygame.init()

(width, height) = (800, 800)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

base_square = pygame.Rect(40,40,9,9)
target_color= (randint(0, 255), randint(0, 255), randint(0, 255))

species = Species(300, target_color)

organisms = species.organisms
time_passed = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(target_color)

    col = -1
    row = 0
    for organism in organisms:

        if(col * 20 >= width - 100): 
            row += 1
            col = 0
        else:
            col +=1

        genome = organism.full_phenotype()
        square = pygame.Rect(base_square.left + col * 20, base_square.top + row * 20, 18, 18)
        pygame.draw.rect(screen, genome, square)

    
    if(species.reached_solution()):
        print("Solution found in generation: ", species.generations)
        running = False

    pygame.display.flip()

    dt = clock.tick(60) / 1000

    time_passed += dt

    if time_passed > 0.5:
        print('evolving')
        species.evolve()
        organisms = species.organisms
        time_passed = 0
        


pygame.quit()
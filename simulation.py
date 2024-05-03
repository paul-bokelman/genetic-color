import math
from random import randint
from tkinter import ttk as tk, Tk, Canvas
from genetic_algorithm import Species
from utils import chance, _from_rgb


config = {
    "target_color": (randint(0, 255), randint(0, 255), randint(0, 255)),
    "random_color_change_probability": 0, # probability that target color changes randomly on each cycle
    "organism_size": 20, # size for organisms (squares)
    "padding": 10, # window padding
    "evo_delay": 100, #ms
    "genetics": {
        "n_organisms": 1296, # max organisms
        "tournament_proportion": 0.8, # proportion of organisms that must compete to survive and breed
        "mutation_probability": 0.4, # the chance that an offspring receives a mutation
    }
}

dimensions = 2 * config['padding'] + int(math.sqrt(config['genetics']['n_organisms'])) * config['organism_size']
species = Species(config['genetics'], config["target_color"])

root = Tk()
root.title('Genetic Colors')

canvas = Canvas(root, bg=_from_rgb(species.target_color), width=dimensions, height=dimensions)
generation_label = tk.Label(root, text=f"Generation 0 Target: {species.target_color}, Best: {species.best().full_phenotype()}")
generation_label.pack()


def simulate_organisms():
    global current_after_id
    canvas.delete('all')
    generation_label.config(text=f"Generation {species.generation}, Target: {species.target_color}, Best: {species.best().full_phenotype()}")
    row, col = 0, 0
    for organism in species.organisms:
        organism_phenotype = _from_rgb(organism.full_phenotype())

        x = config['padding'] + (config['organism_size']) * col
        y = config['padding'] + (config['organism_size']) * row

        canvas.create_rectangle(x, y, x + config['organism_size'], y + config['organism_size'], fill=organism_phenotype, outline=organism_phenotype)

        if((config['padding'] + (config['organism_size']) * (col + 1)) + config['organism_size'] >= dimensions):
            row += 1
            col = 0
        else: 
            col += 1
    
    # randomly change color
    if(chance(config['random_color_change_probability'])): 
        species.target_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        canvas.configure(bg=_from_rgb(species.target_color))


    # if a solution has been reached, stop the sim and display in console
    if not species.reached_solution():
        id = canvas.after(config['evo_delay'], simulate_organisms)
        current_after_id = id
        species.evolve() 
    else:
        print(f'Solution reached after {species.generation} generation(s)')


simulate_organisms() 
canvas.pack()

# change target color command
def change_target_color():
    species.target_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    canvas.configure(bg=_from_rgb(species.target_color))

# restart sim command
def restart_simulation():
    species.genesis()
    canvas.delete("all")
    canvas.after_cancel(current_after_id)
    simulate_organisms()


tk.Button(text="Change Color", command=change_target_color).pack()
tk.Button(text="Restart", command=restart_simulation).pack()


root.mainloop()


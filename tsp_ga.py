import random
import math

def dist(p1, p2):
    return float(math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2))

def fitness(route): # calculate the total distance in a route
    total_distance = 0
    for i in range(1, len(route)):
        total_distance += dist(route[i-1], route[i])
    return total_distance

def crossover(parent1, parent2):
    mid = len(parent1)//2
    start = random.randint(0, mid)
    end = random.randint(start + 1, len(parent1))
    child = parent1[start:end]
    child_half2 = [city for city in parent2 if city not in parent1[start:end]]
    child.extend(child_half2)

    return child

def mutate(route): # swap mutation between 2 indexes
    index1, index2 = random.sample(range(len(route)), 2) # choose 2 different elements using .sample
    route[index1], route[index2] = route[index2], route[index1]
    return route

def randChrom(points):
    curr_points = points.copy()
    li = []
    while len(curr_points) > 0:
        point = random.choice(curr_points)
        li.append(point)
        curr_points.remove(point) # to make sure i don't coose the same point twice
    return li    


def initPop(size, points):
    li = []
    for i in range(size):
        li.append(randChrom(points))
    return li    




def ga(points, population_size, generations, p):
    
    unchanged_generations = 0
    max_unchanged_generations = 600 # make a limit to keep checking
    population = initPop(population_size, points)
    best_solution = population[0]
    best_solution_fitness = fitness(best_solution)

    for g in range(generations):
        parents = random.sample(population, k=2) # choose 2 random parents that won't be the same using random.sample
        child = crossover(parents[0], parents[1]) # create a new child from 2 possible soloutions

        if random.random() < p:         
            child = mutate(child)
        else:
            unchanged_generations += 1

        child_fitness = fitness(child)

        if child_fitness < best_solution_fitness: # means we found a better route according to the courrent child
            best_solution = child
            best_solution_fitness = fitness(child)
            index_to_replace = random.randint(0, population_size-1)
            population[index_to_replace] = child
            population.sort(key=fitness) 

        if unchanged_generations > max_unchanged_generations:
            break

    return best_solution



def solve(points):
    population_size = len(points)
    generations = 5000
    prop = 0.3

    return ga(points, population_size, generations, prop)




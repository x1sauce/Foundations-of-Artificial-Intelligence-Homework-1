import random
import math

def read_file(filename="input.txt"):
    f = open(filename, "r")
    lines = f.readlines()

    size = 200 if int(lines[0].strip()) <= 5 else 10000
    locations = []
    for line in lines[1:]:
        x, y, z = map(int, line.strip().split())
        locations.append((x, y, z))

    print("Size:", size)
    print("Locations:", locations)
    return size, locations


# Initialization
def create_gene_pool(size, locations):
    gene_pool = []

    for i in range(0, size):
        shuffled = random.sample(locations, len(locations))
        home_location = shuffled[0]
        other_locations = shuffled[1:]
        new_gene = [home_location] + other_locations + [home_location]
        gene_pool.append(new_gene)

    return gene_pool

# Parent Selection
def fitness(gene_pool):
    rank_list = []
    for idx, gene in enumerate(gene_pool):
        total_distance = 0
        for i in range(len(gene) - 1):
            current = gene[i]
            next = gene[i + 1]
            total_distance += calculate_total_distance(current, next)
        fitness_score = 1 / (total_distance + 1e-6)
        rank_list.append((gene, total_distance, fitness_score))
    rank_list = sorted(rank_list, key=lambda x: x[2], reverse=True)

    return rank_list

def create_mating_pool(rank_list, parents_num = 2):
    fitness_scores = [fitness_score for (gene, total_distance, fitness_score) in rank_list]
    fitness_total = sum(fitness_scores)
    mating_pool = []
    cumulative_prob = []
    current_sum = 0

    for fitness in fitness_scores:
        current_sum += fitness / fitness_total
        cumulative_prob.append(current_sum)

    for parent in range(parents_num):
        random_num = random.random()
        for i, prob in enumerate(cumulative_prob):
            if random_num <= prob:
                selected_parent = rank_list[i][0]  
                mating_pool.append(selected_parent)
                break

    return mating_pool

def crossover(parent1, parent2, start_idx, end_idx):
    child = []
    subarray = parent1[start_idx:end_idx + 2]
    child += subarray
    leftover_locations = [location for location in parent2 if location not in subarray]
    return child, leftover_locations


def calculate_total_distance(current, next):
    distance = math.sqrt((next[0] - current[0])**2 + (next[1] - current[1])**2 + (next[2] - current[2])**2)
    # print(f"Distance from {current} to {next}: {distance:.2f}")
    return distance

# Main function
if __name__ == "__main__":
    size, locations = read_file()  
    gene_pool = create_gene_pool(size, locations)
    rank_list = fitness(gene_pool)
    mating_pool = create_mating_pool(rank_list, 2)
    parent1, parent2 = mating_pool[0], mating_pool[1]
    start_idx, end_idx = math.ceil(len(parent1)/3), math.floor(len(parent1)/2)
    print(start_idx, end_idx)
    child, leftover_locations = crossover(parent1, parent2, start_idx, end_idx)
    
    print("\nChild1 current has: ", child)
    print("\nLeftover current has: ", leftover_locations)


# All initial population
    # print("Initial Population:")
    # print(len(gene_pool))
    # for i, gene in enumerate(gene_pool):
    #     print(f"Gene #{i+1}: {gene}")
# All fitness scores
    # for i, (gene, total_distance, fitness_score) in enumerate(rank_list):
    #     print(f"Gene #{i+1}: {gene}, Total Distance = {total_distance}, Fitness Score = {fitness_score}")

    print("\nMating Pool Size:", len(mating_pool))
    for i, gene in enumerate(mating_pool[:3]):
        print(f"Parent #{i+1}: {gene}")
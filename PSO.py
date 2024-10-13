import numpy as np
import random
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from TwoThreshodscode import twoThreshodsPolicy


def standardize_data(EC, Wbar, max_energy, max_delay):
    EC_standardized = EC / max_energy
    Wbar_standardized = Wbar / max_delay
    return EC_standardized, Wbar_standardized

def objective_function(params, ECmax, WbarMax, poid):
    lambda_val, N1, N2, mu1, mu2, K = params

    EC, Wbar = twoThreshodsPolicy(int(K), int(N1), int(N2), mu1, mu2, lambda_val)

    EC_standardized, Wbar_standardized = standardize_data(EC, Wbar, ECmax, WbarMax)

    # Calcul de la fonction objective
    a1 = poid[0]  
    a2 = poid[1] 
    F_s = a1 * Wbar_standardized + a2 * EC_standardized

    return EC, Wbar, EC_standardized, Wbar_standardized, F_s

def initialize_particle_position(espaces_recherche):
    
    def random_choice_with_step(min_val, max_val, step):
        num_values = int((max_val - min_val) / step) + 1
        random_value = random.uniform(0, 1)  # Générer une valeur entre 0 et 1
        random_index = int(random_value * num_values)  # Mapper la valeur sur les indices
        return round(min_val + random_index * step, 2)
    '''
    def random_choice_with_step(min_val, max_val, step):
        num_steps = int((max_val - min_val) / step)
        random_step = random.randint(0, num_steps - 1)
        return round(min_val + random_step * step, 2)
    '''
    def find_closest_valid_value(target, min_val, max_val, step):
        closest_valid_value = min_val + int((target - min_val) / step) * step
        return closest_valid_value if closest_valid_value <= max_val else max_val

    lambda_min, lambda_max, lambda_pas = espaces_recherche[0]
    mu2_min, mu2_max, mu2_pas = espaces_recherche[4]

    λ = random_choice_with_step(lambda_min, lambda_max, lambda_pas)
    mu2 = random_choice_with_step(mu2_min, mu2_max, mu2_pas)

    N2_min, N2_max, N2_step = espaces_recherche[2]
    N2 = random_choice_with_step(N2_min, N2_max, N2_step)

    N1_min = max(N2 + 1, espaces_recherche[1][0])
    N1_max = espaces_recherche[1][1]
    N1 = random_choice_with_step(N1_min, N1_max, espaces_recherche[1][2])

    k_min = max(N1 + 1, espaces_recherche[5][0])
    k_max = espaces_recherche[5][1]
    k = random_choice_with_step(k_min, k_max, espaces_recherche[5][2])
    
    mu1_min = mu2 + espaces_recherche[3][2]
    mu1_max = espaces_recherche[3][1]
    mu1_step = espaces_recherche[3][2]
    mu1_min_valid = find_closest_valid_value(mu1_min, mu1_min, mu1_max, mu1_step)
    mu1 = random_choice_with_step(mu1_min_valid, mu1_max, mu1_step)

    return np.array([λ, N1, N2, mu1, mu2, k])


def initialize_swarm(M, espaces_recherche, Vmax):
    particles = np.array([initialize_particle_position(espaces_recherche) for _ in range(M)])
    velocities = np.random.uniform(-Vmax, Vmax, (M, len(particles[0])))
    return particles, velocities

def update_swarm(particles, velocities, Pbest, Gbest, W, C1, C2, Xmax, Vmax, espaces_recherche):
    # Génération de nombres aléatoires pour les coefficients de vitesse
    r1 = np.random.rand(*particles.shape)
    r2 = np.random.rand(*particles.shape)
    
    # Calcul des nouvelles vitesses des particules
    velocities = W * velocities + C1 * r1 * (Pbest - particles) + C2 * r2 * (Gbest - particles)
    
    # Limitation des vitesses pour éviter qu'elles ne deviennent trop grandes
    velocities = np.clip(velocities, -Vmax, Vmax)
    
    # Calcul des nouvelles positions des particules en fonction des vitesses
    new_particles = particles + velocities
    
    for i in range(len(new_particles)):
        # Limiter les positions des particules aux bornes maximales spécifiées
        new_particles[i] = np.minimum(new_particles[i], Xmax)

        # Arrondir à la valeur la plus proche pour lambda
        lambda_min, lambda_max, lambda_step = espaces_recherche[0]
        if new_particles[i][0] < lambda_min:
            new_particles[i][0] = lambda_min
        elif new_particles[i][0] > lambda_max:
            new_particles[i][0] = lambda_max
        else:
            steps = round((new_particles[i][0] - lambda_min) / lambda_step)
            new_particles[i][0] = lambda_min + steps * lambda_step

        # Arrondir à la valeur la plus proche pour mu2
        mu2_min, mu2_max, mu2_step = espaces_recherche[4]
        if new_particles[i][4] < mu2_min:
            new_particles[i][4] = mu2_min
        elif new_particles[i][4] > mu2_max:
            new_particles[i][4] = mu2_max
        else:
            steps = round((new_particles[i][4] - mu2_min) / mu2_step)
            new_particles[i][4] = mu2_min + steps * mu2_step

        # Appliquer les contraintes spécifiques pour N1, N2, et k
        # Contrainte pour N2 : N2 doit être un entier
        new_particles[i][2] = round(new_particles[i][2])

        # Contrainte pour N1 : N1 doit être un entier
        new_particles[i][1] = round(new_particles[i][1])

        # Contrainte pour k : k doit être un entier
        new_particles[i][5] = round(new_particles[i][5])

        # Contrainte pour N2 : N2 doit être supérieur ou égal au minimum spécifié dans l'espace de recherche pour N2
        new_particles[i][2] = max(new_particles[i][2], espaces_recherche[2][0])

        # Contrainte pour N2 : N2 doit être inférieur ou égal au maximum spécifié dans l'espace de recherche pour N2
        new_particles[i][2] = min(new_particles[i][2], espaces_recherche[2][1])

        # Contrainte pour N1 : N1 doit être supérieur ou égal à N2 + 1
        new_particles[i][1] = max(new_particles[i][1], new_particles[i][2] + 1)

        # Contrainte pour N1 : N1 doit être inférieur ou égal à k - 1
        new_particles[i][1] = min(new_particles[i][1], new_particles[i][5] - 1)

        # Contrainte pour k : k doit être supérieur ou égal à N1 + 1
        new_particles[i][5] = max(new_particles[i][5], new_particles[i][1] + 1)

        # Contrainte pour k : k doit être inférieur ou égal à Xmax[5]
        new_particles[i][5] = min(new_particles[i][5], Xmax[5])
        
        # Appliquer les contraintes pour mu1 en respectant les bornes spécifiées dans l'espace de recherche
        # Récupérer la valeur actuelle de mu2
        mu2 = new_particles[i][4]
        mu2_step = espaces_recherche[4][2]
        mu1_min, mu1_max, mu1_step = espaces_recherche[3]
        if(mu1_step == mu2_step):
            # Déterminer la valeur minimale de mu1 en ajoutant le pas spécifié dans l'espace de recherche pour mu1 à mu2
            min_mu1 = mu2 + mu1_step
        else:
            min_mu1 = mu2 + mu1_step
            min_mu1 = find_closest_valid_value(mu1_min, mu1_min, mu1_max, mu1_step)

        # Déterminer la valeur maximale de mu1 en ajoutant le pas spécifié dans l'espace de recherche pour mu1 à mu2, en limitant à Xmax[3]
        max_mu1 =  Xmax[3]

        # Vérifier si la valeur de mu1 est inférieure à la valeur minimale autorisée
        if new_particles[i][3] < min_mu1:
            new_particles[i][3] = min_mu1

            # Vérifier si la valeur de mu1 est supérieure à la valeur maximale autorisée
        elif new_particles[i][3] > max_mu1:
            new_particles[i][3] = max_mu1

            # Si la valeur de mu1 est dans la plage autorisée, arrondir à la valeur la plus proche en respectant le pas spécifié dans l'espace de recherche pour mu1
        else:
            steps = round((new_particles[i][3] - min_mu1) / mu1_step)
            new_particles[i][3] = min_mu1 + steps * mu1_step
    
    # Retourner les nouvelles positions et vitesses des particules
    return new_particles, velocities

def round_to_nearest(value, candidates):
    return min(candidates, key=lambda x: abs(x - value))

def evaluate_fitness(particles, ECmax, WbarMax, poid):
    fitness_values = []
    for p in particles:
        results = objective_function(p, ECmax, WbarMax, poid)
        fitness_values.append(results)
    return np.array(fitness_values)

def initialize_parameters(M, W, C1, C2, Vmax, Xmin, Xmax):
    return M, W, C1, C2, Xmax, Vmax, Xmin

def particle_swarm_optimization(espaces_recherches, ECmax, WbarMax, poid, num_iterations, M, file_pathBest, file_pathCurrent, W, C1, C2, Vmax, Xmin, Xmax):
    M, W, C1, C2, Xmax, Vmax, Xmin = initialize_parameters(M, W, C1, C2, Vmax, Xmin, Xmax)
    particles, velocities = initialize_swarm(M, espaces_recherches, Vmax)
    Pbest = particles.copy()
    pbest_fitness = [float('inf')] * M

    # Évaluation initiale pour définir Pbest et Gbest
    evaluation = evaluate_fitness(particles, ECmax, WbarMax, poid)
    fitness = [result[4] for result in evaluation]
    for i in range(len(particles)):
        Pbest[i] = particles[i].copy()
        pbest_fitness[i] = fitness[i]

    Gbest_idx = np.argmin(fitness)
    Gbest = particles[Gbest_idx].copy()
    gbest_fitness = fitness[Gbest_idx]

    start_time = time.time()
    elapsed_time = 0

    update_excel_data(file_pathBest, elapsed_time, Gbest, fitness[Gbest_idx], evaluation[Gbest_idx, 0], evaluation[Gbest_idx, 1], evaluation[Gbest_idx, 2], evaluation[Gbest_idx, 3])
    for i, particle in enumerate(particles):
        update_excel_data(file_pathCurrent, elapsed_time, particle, fitness[i], evaluation[i, 0], evaluation[i, 1], evaluation[i, 2], evaluation[i, 3])

    for _ in range(num_iterations):
 
        particles, velocities = update_swarm(particles, velocities, Pbest, Gbest, W, C1, C2, Xmax, Vmax, espaces_recherches)
        
        evaluation = evaluate_fitness(particles, ECmax, WbarMax, poid)
        fitness = [result[4] for result in evaluation]
        
        for i in range(len(particles)):
            if fitness[i] < pbest_fitness[i]:
                Pbest[i] = particles[i].copy()
                pbest_fitness[i] = fitness[i]

        elapsed_time = time.time() - start_time

        Gbest_idx = np.argmin(fitness)
        if fitness[Gbest_idx] < gbest_fitness:
            Gbest = particles[Gbest_idx].copy()
            gbest_fitness = fitness[Gbest_idx]
            update_excel_data(file_pathBest, elapsed_time, Gbest, gbest_fitness, 
                            evaluation[Gbest_idx, 0], evaluation[Gbest_idx, 1], 
                            evaluation[Gbest_idx, 2], evaluation[Gbest_idx, 3])
        
        for i, particle in enumerate(particles):
            update_excel_data(file_pathCurrent, elapsed_time, particle, fitness[i], 
                            evaluation[i, 0], evaluation[i, 1], 
                            evaluation[i, 2], evaluation[i, 3])

    best_idx = np.argmin(fitness)
    best_particle = particles[best_idx]
    best_objective_value = fitness[best_idx]
    best_EC = evaluation[best_idx, 0]
    best_Wbar = evaluation[best_idx, 1]
    return best_particle, best_objective_value, best_EC, best_Wbar

def update_excel_data(file_path, elapsed_time, particle, fitness, EC, Wbar, EC_standardized, Wbar_standardized):
    data = {
        "Time": [elapsed_time],
        "Lambda": [particle[0]],
        "N1": [particle[1]],
        "N2": [particle[2]],
        "mu1": [particle[3]],
        "mu2": [particle[4]],
        "K": [particle[5]],
        "energy": [EC],
        "delay": [Wbar],
        "energy_stand": [EC_standardized],
        "delay_stand": [Wbar_standardized],
        "Fitness": [fitness]
    }
    df = pd.DataFrame(data)
    if os.path.exists(file_path):
        current_data = pd.read_excel(file_path)
        df = pd.concat([current_data, df], ignore_index=True)
    df.to_excel(file_path, index=False)

def plot_objective_function_over_time(file_path, file_path1):

    df = pd.read_excel(file_path)
    df1 = pd.read_excel(file_path1)

    elapsed_times = df['Time']
    objective_values = df['energy']

    elapsed_times1 = df['Time']
    objective_values1 = df['delay']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(elapsed_times, objective_values)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Energy Value')
    ax1.set_title('Energy Value over Time ')
    ax1.grid(True)

    ax2.plot(elapsed_times1, objective_values1)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Delay Value')
    ax2.set_title('Delay Value over Time ')
    ax2.grid(True)

    plt.tight_layout()

    figure_canvas = FigureCanvas(fig)
    figure_canvas.print_figure("energy_delay.png", bbox_inches='tight')

    elapsed_times = df['Time']
    objective_values = df['Fitness']
    
    fig1, (ax3) = plt.subplots(1, 1, figsize=(14, 6))

    ax3.plot(elapsed_times, objective_values)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Best Objective Function Value')
    ax3.set_title('Best Objective Function Value over Time ')
    ax3.grid(True)

    plt.tight_layout()
    
    figure_canvas = FigureCanvas(fig1)
    figure_canvas.print_figure("best.png", bbox_inches='tight')

    return "best.png","energy_delay.png"

def write_execution_time(duration_seconds, filename):
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        milliseconds = int((duration_seconds - int(duration_seconds)) * 1000)

        time_message = f"Temps d'execution := {duration_seconds} s = {hours} hr = {minutes} min ~= {minutes} min. {seconds} sec. {milliseconds} ms"

        with open(filename, 'w') as file:
            file.write(time_message)

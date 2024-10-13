import random
import math
import numpy as np
import time
import os 
from TwoThreshodscode import twoThreshodsPolicy
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas



def standardize_data(EC, Wbar, max_energy, max_delay):
    EC_standardized = EC / max_energy
    Wbar_standardized = Wbar / max_delay

    return EC_standardized, Wbar_standardized

# Exemple de fonction objective simplifiée 
def objective_function(params, ECmax, WbarMax, poid):
            lambda_val, N1, N2, mu1, mu2, K = params
            
            # Calcul des propriétés du système
            #Wbar, EC = compute_system_properties(K, N1, N2, mu1, mu2, lambda_val)
            EC,Wbar=twoThreshodsPolicy(K, N1, N2, mu1, mu2, lambda_val)
            # Standardisation des données
            EC_standardized, Wbar_standardized = standardize_data(EC, Wbar, ECmax, WbarMax)
            
            # Calcul de la fonction objective
            a1 = poid[0]  # Remplacez par la valeur appropriée
            a2 = poid[1] # Remplacez par la valeur appropriée
            F_s = a1 * Wbar_standardized + a2 * EC_standardized
            
            return EC,Wbar, EC_standardized, Wbar_standardized, F_s

def generer_solution_voisine(solution_actuelle, espaces_recherche, ecart_types):
    
    lambda_actuel, N1_actuel, N2_actuel, mu1_actuel, mu2_actuel, k_actuel = solution_actuelle
    
    lambda_min = espaces_recherche[0][0]
    lambda_mediane = (lambda_min + espaces_recherche[0][1]) / 2
    poids_lambda_actuel = 0.5   
    moyenne = poids_lambda_actuel * lambda_actuel + (1 - poids_lambda_actuel) * lambda_mediane
    lambda_nouveau = random.gauss(moyenne, ecart_types[0])
    lambda_nouveau = round(max(lambda_min, min(espaces_recherche[0][1], lambda_nouveau)) / espaces_recherche[0][2]) * espaces_recherche[0][2]
    lambda_nouveau = round(lambda_nouveau, 2)
    
    mu2_min = espaces_recherche[4][0]
    mu2_max = espaces_recherche[4][1]
    mu2_mediane = (mu2_min + mu2_max) / 2
    poids_mu2_actuel = 0.5 
    moyenne_mu2 = poids_mu2_actuel * mu2_actuel + (1 - poids_mu2_actuel) * mu2_mediane
    ecart_type_mu2 = ecart_types[4]  
    mu2_nouveau = random.gauss(moyenne_mu2, ecart_type_mu2)
    mu2_nouveau = round(max(mu2_min, min(mu2_max, mu2_nouveau))/ espaces_recherche[4][2])*espaces_recherche[4][2]
    mu2_nouveau = round(mu2_nouveau, 2)
 
    mu1_min = max(mu2_nouveau + 0.5, espaces_recherche[3][0])
    mu1_max = espaces_recherche[3][1]
    mu1_mediane = (mu1_min + mu1_max) / 2
    poids_mu1_actuel = 0.5
    moyenne_mu1 = poids_mu1_actuel * mu1_actuel + (1 - poids_mu1_actuel) * mu1_mediane
    mu1_nouveau = random.gauss(moyenne_mu1, ecart_types[3])
    mu1_nouveau = round(max(mu1_min, min(mu1_max, mu1_nouveau)) / espaces_recherche[3][2]) * espaces_recherche[3][2]
    mu1_nouveau = round(mu1_nouveau, 2)
    
    N2_min = espaces_recherche[2][0]
    N2_mediane = (N2_min + espaces_recherche[2][1]) / 2
    poids_N2_actuel = 0.5    
    moyenne_N2 = poids_N2_actuel * N2_actuel + (1 - poids_N2_actuel) * N2_mediane
    N2_nouveau = random.gauss(moyenne_N2, ecart_types[2])
    N2_nouveau = round(max(N2_min, min(espaces_recherche[2][1], N2_nouveau)))
    N2_nouveau = round(N2_nouveau) 
    
    N1_min = max(N2_nouveau + 1, espaces_recherche[1][0])
    N1_max = min(N2_nouveau + 10, espaces_recherche[1][1])
    N1_mediane = (N1_min + N1_max) / 2
    moyenne_N1 = 0.3 * N1_actuel + 0.7 * N1_mediane
    N1_nouveau = round(random.gauss(moyenne_N1, ecart_types[1]) / espaces_recherche[1][2]) * espaces_recherche[1][2]
    N1_nouveau = max(N1_min, min(N1_max, N1_nouveau))

    k_min = max(N1_nouveau + 1, espaces_recherche[5][0])
    k_max = min(N1_nouveau + 6, espaces_recherche[5][1])
    k_mediane = (k_min + k_max) / 2
    moyenne_k = 0.3 * k_actuel + 0.7 * k_mediane
    k_nouveau = round(random.gauss(moyenne_k, ecart_types[5]) / espaces_recherche[5][2]) * espaces_recherche[5][2]
    k_nouveau = max(k_min, min(k_max, k_nouveau))
   
    nouvelle_solution = [
        lambda_nouveau,
        N1_nouveau,
        N2_nouveau,
        mu1_nouveau,
        mu2_nouveau,
        k_nouveau
    ]
    
    return nouvelle_solution

def initialiser_solution_mediane(espaces_recherche):
    solution_initiale = []            
    for min_parametre, max_parametre, pas_parametre in espaces_recherche:
        mediane_parametre = calculer_mediane_parametre(min_parametre, max_parametre, pas_parametre)
        solution_initiale.append(mediane_parametre)

    return solution_initiale

def calculer_mediane_parametre(min_parametre, max_parametre, pas_parametre):
    # Calcul de la médiane en respectant le pas
    mediane = min_parametre + pas_parametre * math.ceil((max_parametre - min_parametre) / (2 * pas_parametre))
    mediane = round(mediane, 2)

    return mediane

def calculate_ecart_types(espaces_recherche):
    
    
    ecr_lambda = (espaces_recherche[0][1] - espaces_recherche[0][0]) / 4
    ecr_N1 = (espaces_recherche[1][1] - espaces_recherche[1][0]) / 4
    ecr_N2 = (espaces_recherche[2][1] - espaces_recherche[2][0]) / 4
    ecr_mu1 = (espaces_recherche[3][1] - espaces_recherche[3][0]) / 4
    ecr_mu2 = (espaces_recherche[4][1] - espaces_recherche[4][0]) / 4
    ecr_k = (espaces_recherche[5][1] - espaces_recherche[5][0]) / 4


    return [ecr_lambda, ecr_N1, ecr_N2, ecr_mu1, ecr_mu2, ecr_k]

def tabu_search(espaces_recherche, ECmax, WbarMax, poid, max_iterations,execution_time,file_pathBest,file_pathCurrent, initial_tabu_tenure, nombre_de_solutions_voisines, start_time_t):

    solution_courante = initialiser_solution_mediane(espaces_recherche)
    meilleure_solution = solution_courante[:]
    best_EC, best_Wbar, best_EC_standardized, best_Wbar_standardized, meilleure_valeur_objective = objective_function(meilleure_solution, ECmax, WbarMax, poid)
    ecart_types = calculate_ecart_types(espaces_recherche)
    
    liste_tabou = []
    start_time = start_time_t 

    elapsed_time = 0 
    iteration = 0

    update_excel_data(file_pathBest, elapsed_time, meilleure_solution, meilleure_valeur_objective, best_EC, best_Wbar, best_EC_standardized, best_Wbar_standardized)
    update_excel_data(file_pathCurrent, elapsed_time, solution_courante, meilleure_valeur_objective, best_EC, best_Wbar, best_EC_standardized, best_Wbar_standardized)
    
    while iteration < max_iterations and time.time() - start_time < execution_time:
    
        voisins = [generer_solution_voisine(solution_courante,espaces_recherche, ecart_types) for _ in range(nombre_de_solutions_voisines)]

        voisins_objective_values = [objective_function(voisin, ECmax, WbarMax, poid)[4] for voisin in voisins]

        # Créer une liste de tuples (voisin, voisins_objective_values)
        voisins_with_objective_values = list(zip(voisins, voisins_objective_values))

        # Trier les voisins par ordre de voisins_objective_value
        voisins_with_objective_values = sorted(voisins_with_objective_values, key=lambda x: x[1])

        meilleure_voisine, voisin_meilleure_objectif = voisins_with_objective_values[0]


        if meilleure_voisine not in [x[:-1] for x in liste_tabou]:
            solution_courante = meilleure_voisine[:]
            voisine_EC, voisine_Wbar, voisine_EC_standardized, voisine_Wbar_standardized, valeur_objective_meilleure_voisine = objective_function(meilleure_voisine, ECmax, WbarMax, poid)
            if valeur_objective_meilleure_voisine < meilleure_valeur_objective:
                meilleure_solution = meilleure_voisine[:]
                meilleure_valeur_objective = valeur_objective_meilleure_voisine
                best_EC = voisine_EC
                best_Wbar = voisine_Wbar
                best_EC_standardized = voisine_EC_standardized
                best_Wbar_standardized = voisine_Wbar_standardized
                elapsed_time = time.time() - start_time
                update_excel_data(file_pathBest, elapsed_time, meilleure_solution, meilleure_valeur_objective, best_EC, best_Wbar, best_EC_standardized, best_Wbar_standardized)
    
            liste_tabou.append(meilleure_voisine)
            liste_tabou[-1].append(initial_tabu_tenure)
            
        # Mettre à jour la durée tabou de chaque solution
        for i in range(len(liste_tabou)):
            liste_tabou[i][-1] -= 1
            if liste_tabou[i][-1] == 0:
                liste_tabou.pop(i)
                break

    
        iteration += 1

        # Mise à jour du temps écoulé
        elapsed_time = time.time() - start_time

        update_excel_data(file_pathCurrent, elapsed_time, solution_courante, valeur_objective_meilleure_voisine, voisine_EC, voisine_Wbar, voisine_EC_standardized, voisine_Wbar_standardized)

        
    return meilleure_solution, meilleure_valeur_objective, best_EC, best_Wbar

def update_excel_data(file_path, elapsed_time, state, objective_value, energy, delay, EC_standardized, Wbar_standardized):
    current_data = pd.DataFrame({
        "Time (s)": [elapsed_time],
        "lambda": [state[0]],
        "N1": [state[1]],
        "N2": [state[2]],
        "mu1": [state[3]],
        "mu2": [state[4]],
        "K": [state[5]],
        "energy" : [energy],
        "delay" : [delay],
        "energy_stand" : [EC_standardized],
        "delay_stand" :[Wbar_standardized],
        "Fitness": [objective_value],
    })

    # Vérifier si le fichier Excel existe déjà
    if os.path.isfile(file_path):
        df = pd.read_excel(file_path)
        # Ajouter les nouvelles données à la fin du DataFrame
        df = pd.concat([df, current_data], ignore_index=True)
    else:
        # Créer un nouveau DataFrame avec les nouvelles données
        df = current_data
    
    # Écrire le DataFrame dans le fichier Excel
    df.to_excel(file_path, index=False)


def plot_objective_function_over_time(file_path, file_path1):
    df = pd.read_excel(file_path)
    df1 = pd.read_excel(file_path1)
    
    elapsed_times = df['Time (s)']
    objective_values = df['energy']

    elapsed_times1 = df['Time (s)']
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
    
    # Save the figure as an image
    figure_canvas = FigureCanvas(fig)
    figure_canvas.print_figure("energy_delay.png", bbox_inches='tight')


    elapsed_times = df['Time (s)']
    objective_values = df['Fitness']
  
    elapsed_times1 = df1['Time (s)']
    objective_values1 = df1['Fitness']

    fig1, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 6))

    ax3.plot(elapsed_times, objective_values)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Best Objective Function Value')
    ax3.set_title('Best Objective Function Value over Time ')
    ax3.grid(True)

    ax4.plot(elapsed_times1, objective_values1)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Current Objective Function Value')
    ax4.set_title('Current Objective Function Value over Time ')
    ax4.grid(True)

    plt.tight_layout()

    figure_canvas = FigureCanvas(fig1)
    figure_canvas.print_figure("best_current.png", bbox_inches='tight')

    return "best_current.png","energy_delay.png"

def write_execution_time(duration_seconds, filename):
        # Convertir la durée en heures, minutes et secondes
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        milliseconds = int((duration_seconds - int(duration_seconds)) * 1000)

        # Créer le message de temps d'exécution
        time_message = f"Temps d'execution := {duration_seconds} s = {hours} hr = {minutes} min ~= {minutes} min. {seconds} sec. {milliseconds} ms"

        # Écrire le message dans le fichier
        with open(filename, 'w') as file:
            file.write(time_message)
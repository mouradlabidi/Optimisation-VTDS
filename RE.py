from TwoThreshodscode import twoThreshodsPolicy

def ecrire_parametre_fichier(nom_fichier, parametre):
    try:
        with open(nom_fichier, "a") as fichier:
            fichier.write("Execution : lambda={:.2f}, mu1={:.2f}, mu2={:.2f}, N1={}, N2={}, k={}, energy={:.6f}, delay={:.6f}\n".format(
                parametre["lambda"], parametre["mu1"], parametre["mu2"],
                parametre["N1"], parametre["N2"], parametre["k"],
                parametre["energy"], parametre["delay"]))
    except FileNotFoundError:
        print("Erreur lors de l'ouverture du fichier {}.".format(nom_fichier))


def readLinesFromFile(file_path):
    lines = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return lines


import re
def extract_parameters_from_line(line):
    pattern = r"Execution : lambda=([\d.]+), mu1=([\d.]+), mu2=([\d.]+), N1=(\d+), N2=(\d+), k=(\d+), energy=([\d.]+), delay=([\d.]+)"
    match = re.match(pattern, line)
    if match:
        lambda_val = float(match.group(1))
        mu1_val = float(match.group(2))
        mu2_val = float(match.group(3))
        N1_val = int(match.group(4))
        N2_val = int(match.group(5))
        k_val = int(match.group(6))
        energy_val = float(match.group(7))
        delay_val = float(match.group(8))
        return lambda_val, mu1_val, mu2_val, N1_val, N2_val, k_val, energy_val, delay_val
    else:
        print("La ligne ne correspond pas au modèle attendu.")
        return None

import pandas as pd
def TextToExcel(file_path):
    lines=readLinesFromFile(file_path)
    if lines:
        lambda_list=[]
        mu1_list=[]
        mu2_list=[]
        N1_list=[]
        N2_list=[]
        K_list=[]
        energy_list=[]
        delay_list=[]
        for line in lines:
                lambda_val, mu1_val, mu2_val, N1_val, N2_val, k_val, energy_val, delay_val = extract_parameters_from_line(line)
                lambda_list+= [lambda_val]
                mu1_list += [mu1_val]
                mu2_list += [mu2_val]
                N1_list += [N1_val]
                N2_list += [N2_val]
                K_list += [k_val]
                energy_list+=[energy_val]
                delay_list += [delay_val]
        
        dict = {'lambda': lambda_list, 'mu1': mu1_list, 'mu2': mu2_list, 'N1': N1_list, 'N2': N2_list, 'K': K_list, 'energy': energy_list, 'delay': delay_list}
        df = pd.DataFrame(dict)
 
        df.to_excel('Recherche.xlsx')
        import shutil
        import os
        result_directory = "resultRE"
        # Supprimer le dossier s'il existe déjà
        if os.path.exists(result_directory):
            if os.path.exists("resultRE\Recherche.xlsx"):
                os.remove("resultRE\Recherche.xlsx")
            shutil.rmtree(result_directory)
        os.makedirs(result_directory)
        os.remove(file_path)
        shutil.move('Recherche.xlsx', result_directory) 
    else:
        print("No lines read from the file.")
   

def RechercheExhaustive(K_D, K_F, K_P, N1_D, N1_F, N1_P, N2_D, N2_F, N2_P, mu1_D, mu1_F, mu1_P, mu2_D, mu2_F, mu2_P, Lambda_D, Lambda_F, Lambda_P):
    N2=N2_D
    while N2 <= N2_F:
        N1=N1_D
        while N1 <= N1_F:
            if(N2<N1):
                K= K_D
                while K <= K_F:
                    if(N1<K):
                        mu2=mu2_D
                        while mu2 <= mu2_F:
                            Lambda=Lambda_D
                            while Lambda<=Lambda_F:
                                if (mu2 < Lambda):
                                    mu1=mu1_D
                                    while mu1 <= mu1_F:
                                        if(Lambda<mu1):
                                            #Traitement
                                            #print(K,N1,N2,mu1,Lambda,mu2)
                                            EC,Wbar=twoThreshodsPolicy(K, N1, N2, mu1, mu2, Lambda)
                                            parametre = {
                                                "lambda": Lambda,
                                                "mu1": mu1,
                                                "mu2": mu2,
                                                "N1": N1,
                                                "N2": N2,
                                                "k": K,
                                                "energy": EC,
                                                "delay": Wbar
                                            }
                                            ecrire_parametre_fichier("Recherche.txt", parametre)   

                                        mu1 += mu1_P
                                Lambda+= Lambda_P
                            mu2 += mu2_P
                    K += K_P
            N1 += N1_P
        N2 += N2_P 
    TextToExcel("Recherche.txt")

#RechercheExhaustive(3,20,1,2,19,1,1,19,1,0.5,5,0.25,0.25,0.75,0.25,0.25,0.75,0.25)
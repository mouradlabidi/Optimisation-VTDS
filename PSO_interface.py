import customtkinter
#import numpy as np
import OptimisationResults
import matplotlib
from tkinter import messagebox
matplotlib.use('Agg')
from PSO import particle_swarm_optimization
from PSO import plot_objective_function_over_time
from PSO import write_execution_time
from TwoThreshodscode import twoThreshodsPolicy
import threading
import Prog_Interface
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class PSO_Meta(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.espaces_recherche = None
        self.best_position = None
        self.best_objective_value = None
        self.EC = None
        self.Wbar = None
        self.file_pathBest = None 
        self.file_pathCurrent = None
        self.NombrePt = None
        self.inertie = None
        self.nbr_iteration = None
        self.fact = None
        self.VMAX = None
        self.poid = None

        # configure window
        self.title("Optimisation par essaim de particule")
        # Set window dimensions and calculate center position
        window_width = 1100
        window_height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="OptiSense \nEnergy-Delay", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
       
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        #title
        self.Metaheuristic=customtkinter.CTkLabel(self, text="Métaheuristique: OEP", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Metaheuristic.grid(row=0, column=1, padx=20, pady=15)

        # Créer le bouton "Retour" et l'ajouter à l'onglet "Résultat"      
        self.return_button = customtkinter.CTkButton(self, text="Retour", command=self.return_to_main_interface)
        self.return_button.grid(row=0, column=1, padx=20, pady=0, sticky="e")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        first_tab="Espaces de recherche"
        second_tab="Les paramètres de l'optimisation par essaim de particule "
        self.tabview.add(first_tab)
        self.tabview.add(second_tab)
        self.tabview.tab(first_tab).grid_columnconfigure(0, weight=4)  # configure grid of individual tabs
        self.tabview.tab(second_tab).grid_columnconfigure(0, weight=4)
        
        #First Tab_________________________________________________________________________________________________________________________
        self.label_K = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du K", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_K.grid(row=0, column=0, padx=20, pady=20)
        self.debut_K = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_K.grid(row=0, column=1, padx=20, pady=20)
        self.fin_K = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_K.grid(row=0, column=2, padx=20, pady=20)
        self.pas_K = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_K.grid(row=0, column=3, padx=20, pady=20)

        self.label_N1 = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du N1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_N1.grid(row=1, column=0, padx=20, pady=20)
        self.debut_N1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_N1.grid(row=1, column=1, padx=20, pady=20)
        self.fin_N1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_N1.grid(row=1, column=2, padx=20, pady=20)
        self.pas_N1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_N1.grid(row=1, column=3, padx=20, pady=20)

        self.label_N2 = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du N2", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_N2.grid(row=2, column=0, padx=20, pady=20)
        self.debut_N2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_N2.grid(row=2, column=1, padx=20, pady=20)
        self.fin_N2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_N2.grid(row=2, column=2, padx=20, pady=20)
        self.pas_N2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_N2.grid(row=2, column=3, padx=20, pady=20)

        self.label_mu1 = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du Mu1", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_mu1.grid(row=3, column=0, padx=20, pady=20)
        self.debut_mu1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_mu1.grid(row=3, column=1, padx=20, pady=20)
        self.fin_mu1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_mu1.grid(row=3, column=2, padx=20, pady=20)
        self.pas_mu1 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_mu1.grid(row=3, column=3, padx=20, pady=20)

        self.label_mu2 = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du Mu2", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_mu2.grid(row=4, column=0, padx=20, pady=20)
        self.debut_mu2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_mu2.grid(row=4, column=1, padx=20, pady=20)
        self.fin_mu2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_mu2.grid(row=4, column=2, padx=20, pady=20)
        self.pas_mu2 = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_mu2.grid(row=4, column=3, padx=20, pady=20)

        self.label_lambda = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Espace de recherche du Lambda", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_lambda.grid(row=5, column=0, padx=20, pady=20)
        self.debut_lambda = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Début")
        self.debut_lambda.grid(row=5, column=1, padx=20, pady=20)
        self.fin_lambda = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Fin")
        self.fin_lambda.grid(row=5, column=2, padx=20, pady=20)
        self.pas_lambda = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Pas")
        self.pas_lambda.grid(row=5, column=3, padx=20, pady=20)

        #Second Tab_________________________________________________________________________________________________________________________
        self.label_NbrIteration = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Nombre d'Itération/Particules", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_NbrIteration.grid(row=0, column=0, padx=20, pady=20)
        self.NbrIteration = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="N")
        self.NbrIteration.grid(row=0, column=1, padx=20, pady=20)
        self.NombreP = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="M")
        self.NombreP.grid(row=0, column=2, padx=20, pady=20)
        

        self.label_inertie = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Poids d'inertie", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_inertie.grid(row=1, column=0, padx=20, pady=20)
        self.inertie = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="W")
        self.inertie.grid(row=1, column=1, padx=20, pady=20)

        self.label_VMAX = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Vitesse maximale", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_VMAX.grid(row=2, column=0, padx=20, pady=20)
        self.VMAX = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="Vmax")
        self.VMAX.grid(row=2, column=1, padx=20, pady=20)

        self.label_facteur = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Facteur cognitif/social", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_facteur.grid(row=3, column=0, padx=20, pady=20)
        self.debut_facteur = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="cognitif (C1)")
        self.debut_facteur.grid(row=3, column=1, padx=20, pady=20)
        self.fin_facteur = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="social (C2)")
        self.fin_facteur.grid(row=3, column=2, padx=20, pady=20)

        self.label_Poids = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Poids de la fonction objective", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_Poids.grid(row=4, column=0, padx=20, pady=20)
        self.PoidsEnergy = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="Energie")
        self.PoidsEnergy.grid(row=4, column=1, padx=20, pady=20)
        self.PoidsDelay = customtkinter.CTkEntry(self.tabview.tab(second_tab),placeholder_text="Délai")
        self.PoidsDelay.grid(row=4, column=2, padx=20, pady=20)

        self.ExecuteSA = customtkinter.CTkButton(self.tabview.tab(second_tab), text="Executer", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           command=self.optimisationEvent)
        self.ExecuteSA.grid(row=5, column=2, padx=20, pady=(10, 10))



    



        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
    
    def getParameters(self):
        try:
            K_D = int(self.debut_K.get())
            K_F = int(self.fin_K.get())
            K_P = int(self.pas_K.get())

            N1_D = int(self.debut_N1.get())
            N1_F = int(self.fin_N1.get())
            N1_P = int(self.pas_N1.get())

            N2_D = int(self.debut_N2.get())
            N2_F = int(self.fin_N2.get())
            N2_P = int(self.pas_N2.get())
            
            
            mu1_D = float(self.debut_mu1.get())
            mu1_F = float(self.fin_mu1.get())
            mu1_P = float(self.pas_mu1.get())

            mu2_D = float(self.debut_mu2.get())
            mu2_F = float(self.fin_mu2.get())
            mu2_P = float(self.pas_mu2.get())

            Lambda_D = float(self.debut_lambda.get())
            Lambda_F = float(self.fin_lambda.get())
            Lambda_P = float(self.pas_lambda.get())

            Facteur_social = float(self.debut_facteur.get())
            Facteur_cognitif = float(self.fin_facteur.get())

            self.NombrePt = int(self.NombreP.get())
            
            try:
                self.inertie = float(self.inertie.get())
            except AttributeError:
                self.inertie = float(self.inertie)

            
            try:
                self.VMAX = float(self.VMAX.get())
            except AttributeError:
                self.VMAX  = float(self.VMAX)


            self.nbr_iteration = int(self.NbrIteration.get())
            
            
            poidEnergy= float(self.PoidsEnergy.get())
            poidDelay= float(self.PoidsDelay.get())

        except ValueError:
            messagebox.showerror("Erreur", "Tous les entrées doivent être numériques")
            return False
        
        # Vérifications
        #Check K
        if K_D <= 0 or K_F<= 0 or K_P <= 0:
            messagebox.showerror("Erreur", "K doit être positif")
            return False 
        if K_F < K_D:
            messagebox.showerror("Erreur", "La fin de K doit être supérieure ou égale au début")
            return False
        if ((K_F-K_D+1) % K_P != 0) or K_P> (K_F-K_D+1):
            msg=f"Le pas de K doit être un diviseur de {(K_F-K_D+1)} et inférieur à {(K_F-K_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
        #Check N1
        if N1_D <= 0 or N1_F<= 0 or N1_P <= 0:
            messagebox.showerror("Erreur", "N1 doit être positif")
            return False 
        if N1_F < N1_D:
            messagebox.showerror("Erreur", "La fin de N1 doit être supérieure ou égale au début")
            return False
        if ((N1_F-N1_D+1) % N1_P != 0) or N1_P> (N1_F-N1_D+1):
            msg=f"Le pas de N1 doit être un diviseur de {(N1_F-N1_D+1)} et inférieur à {(N1_F-N1_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
        #Check between K and N1
        if K_D <= N1_D:
            messagebox.showerror("Erreur", "Le début de K doit être supérieur au début de N1")
            return False
        if K_F <= N1_F:
            messagebox.showerror("Erreur", "La fin de K doit être supérieure à la fin de N1")
            return False
        
        #Check N2
        if N2_D <= 0 or N2_F<= 0 or N2_P <= 0:
            messagebox.showerror("Erreur", "N2 doit être positif")
            return False 
        if N2_F < N2_D:
            messagebox.showerror("Erreur", "La fin de N2 doit être supérieure ou égale au début")
            return False
        if ((N2_F-N2_D+1) % N2_P != 0) or N2_P> (N2_F-N2_D+1):
            msg=f"Le pas de N2 doit être un diviseur de {(N2_F-N2_D+1)} et inférieur à {(N2_F-N2_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
        #Check between N1 and N2
        if N1_D <= N2_D:
            messagebox.showerror("Erreur", "Le début de N1 doit être supérieur au début de N2")
            return False
        if N1_F <= N2_F:
            messagebox.showerror("Erreur", "La fin de N1 doit être supérieure à la fin de N2")
            return False
        
        #Check mu1
        if mu1_D <= 0 or mu1_F<= 0 or mu1_P <= 0:
            messagebox.showerror("Erreur", "mu1 doit être positif")
            return False 
        if mu1_F < mu1_D:
            messagebox.showerror("Erreur", "La fin de mu1 doit être supérieure ou égale au début")
            return False
        if ((mu1_F-mu1_D+1) % mu1_P != 0) or mu1_P> (mu1_F-mu1_D+1):
            msg=f"Le pas de Mu1 doit être un diviseur de {(mu1_F-mu1_D+1)} et inférieur à {(mu1_F-mu1_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
        #Check Lambda 
        if Lambda_D <= 0 or Lambda_F <= 0 or Lambda_P <= 0:
            messagebox.showerror("Erreur", "Lambda doit être positif")
            return False
        if Lambda_F < Lambda_D:
            messagebox.showerror("Erreur", "La fin de Lambda doit être supérieure ou égale au début")
            return False
        if ((Lambda_F-Lambda_D+1) % Lambda_P != 0) or Lambda_P> (Lambda_F-Lambda_D+1):
            msg=f"Le pas de Lambda doit être un diviseur de {(Lambda_F-Lambda_D+1)} et inférieur à {(Lambda_F-Lambda_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
         #Check mu2        
        if mu2_D <= 0 or mu2_F<= 0 or mu2_P <= 0:
            messagebox.showerror("Erreur", "Mu2 doit être positif")
            return False 
        if mu2_F < mu2_D:
            messagebox.showerror("Erreur", "La fin de Mu2 doit être supérieure ou égale au début")
            return False
        if ((mu2_F-mu2_D+1) % mu2_P != 0) or mu2_P> (mu2_F-mu2_D+1):
            msg=f"Le pas de Mu2 doit être un diviseur de {(mu2_F-mu2_D+1)} et inférieur à {(mu2_F-mu2_D+1)}."
            messagebox.showerror("Erreur", msg)
            return False
        
        # Vérification de la contrainte mu1 > mu2
        if mu1_D <= mu2_D:
            messagebox.showerror("Erreur", "mu1 doit être strictement supérieur à mu2")
            return False
        
        ##################### à refaire ##########################
        
        if not (1.0 <= Facteur_social <= 2.5):
            messagebox.showerror("Erreur", "Le facteur social doit être compris entre 1.0 et 2.5.")
            return False

        if not (1.0 <= Facteur_cognitif <= 2.5):
            messagebox.showerror("Erreur", "Le facteur cognitif doit être compris entre 1.0 et 2.5.")
            return False

        if not (5 <= self.NombrePt <= 100):
            messagebox.showerror("Erreur", "Le nombre de particules doit être compris entre 10 et 100.")
            return False

        if not (0.4 <= self.inertie <= 1):
            messagebox.showerror("Erreur", "L'inertie doit être comprise entre 0.4 et 0.9.")
            return False
        
        if not (0.1 <= self.VMAX <= 2.0):
            messagebox.showerror("Erreur", " La vitesse maximale doit être compris entre 0.1 et 2.0.")
            return False

        if self.nbr_iteration <= 0:
            messagebox.showerror("Erreur", "Le nombre d'itérations doit être positif")
            return False

        if poidEnergy < 0 or poidEnergy > 1 or poidDelay < 0 or poidDelay > 1 or poidEnergy + poidDelay != 1:
            messagebox.showerror("Erreur", "Les poids d'énergie et de retard doivent être compris entre 0 et 1 et leur somme doit être égale à 1")
            return False

        # Définition des espaces de recherche pour chaque paramètre
        self.espaces_recherche = [
            (Lambda_D, Lambda_F, Lambda_P),  # Espace de recherche pour lambda: min, max, pas
            (N1_D, N1_F, N1_P),              # Espace de recherche pour N1: min, max, pas
            (N2_D, N2_F, N2_P),              # Espace de recherche pour N2: min, max, pas
            (mu1_D, mu1_F, mu1_P),           # Espace de recherche pour mu1: min, max, pas
            (mu2_D, mu2_F, mu2_P),           # Espace de recherche pour mu2: min, max, pas
            (K_D, K_F, K_P)                  # Espace de recherche pour K: min, max, pas
        ]
        self.fact = [Facteur_cognitif, Facteur_social] 
        self.poid = [poidEnergy, poidDelay] 

        return True
        

    def max_enrgy_delay(self, k, lambda_min):
        #Two thresholds working vacation policy
        ECI = 10.0 # consommation énergétique du mode idle
        ECSB = 25 # consommation énergétique du mode semi busy
        ECb = 500.0 # consommation énergétique du mode busy
        ECTx  =5.0 # consommation énergétique pour le maintien de chaque paquet présent dans le nœud capteur
        ECs = 300.0 # consommation énergétique de Switching entre les modes
        PI = 0.00000000000001
        PSB = 0.00000000000000
        Cbar = 1
        Qbar = k
        ECmax = (PSB * ECSB) + (PI * ECI) + (ECb * (1 - PSB - PI)) + (ECs / Cbar) + (Qbar * ECTx)
        print(ECmax)

        Wbar_max = Qbar / lambda_min

        return Wbar_max, ECmax

    def optimisationEvent(self):
            
            if not self.getParameters():
                return
            
            start_time = time.time()
            prog_window = Prog_Interface.ProgressInterface()

            # Fonction pour exécuter run_PSO
            def run_PSO_wrapper():
                self.run_PSO(prog_window, start_time)
                # Une fois que run_PSO est terminé, exécuter callback dans le thread principal
                prog_window.after(0, lambda: self.callback(start_time, prog_window))

            # Créer un Timer pour exécuter run_PSO après un court délai
            pso_timer = threading.Timer(0.1, run_PSO_wrapper)
            pso_timer.start()

            # Démarrer mainloop() dans le thread principal
            prog_window.mainloop()

    def callback(self, start_time, prog_window):
        # Enregistrer le temps de fin
        end_time = time.time()

        # Calculer la durée totale
        execution_time = end_time - start_time
        print("Le temps d'exécution est de", execution_time, "secondes.")
        filename = f"Time.txt"
        write_execution_time(execution_time, filename)

        self.image1, self.image=plot_objective_function_over_time(self.file_pathBest, self.file_pathCurrent)
        import os
        import shutil
        result_directory = "resultPSO"
        if os.path.exists(result_directory):
            shutil.rmtree(result_directory)
        os.makedirs(result_directory)
        
        prog_window.after(0, prog_window.destroy)
        
        self.show_results(self.best_position, self.best_objective_value, self.EC, self.Wbar, self.file_pathBest, self.file_pathCurrent, result_directory, filename)
            

    def run_PSO(self, prog_window, start_time):
 
        lambda_max = self.espaces_recherche[0][1]
        N1_max = self.espaces_recherche[1][1]
        N2_max = self.espaces_recherche[2][1]
        mu1_max = self.espaces_recherche[3][1]
        mu2_max = self.espaces_recherche[4][1]
        k_max = self.espaces_recherche[5][1]
 
        lambda_min = self.espaces_recherche[0][0]
        mu1_min = self.espaces_recherche[3][0]
        mu2_min = self.espaces_recherche[4][0]
        N1_min = self.espaces_recherche[1][0]
        N2_min = self.espaces_recherche[2][0]
        k_min = self.espaces_recherche[5][0]

    
        WbarMax, ECmax = self.max_enrgy_delay(k_max, lambda_min)
        
        num_iterations = self.nbr_iteration
        self.file_pathBest = "best.xlsx"
        self.file_pathCurrent = "current.xlsx"
        best_objective_value = float('inf') 

        Vmax= self.VMAX 
        Xmin =[lambda_min, N1_min, N2_min, mu1_min, mu2_min, k_min]
        Xmax = [lambda_max, N1_max, N2_max, mu1_max, mu2_max, k_max]

        try:
            print("start PSO")
            self.best_position, self.best_objective_value, self.EC, self.Wbar = particle_swarm_optimization(self.espaces_recherche, ECmax, WbarMax, self.poid, num_iterations, self.NombrePt, self.file_pathBest, self.file_pathCurrent, self.inertie, self.fact[0], self.fact[1], Vmax, Xmin, Xmax)
            print("end PSO")
            print("Meilleure position trouvée par PSO:", self.best_position)
            print("Value of the objective function:", self.best_objective_value) 
            print ("start plot") 
            
            
        except KeyboardInterrupt:
            print("Execution interrupted.")
            
            if self.best_position is not None:
                print("Meilleure position trouvée par PSO:", self.best_position)
                print("Value of the objective function for the best solution:", self.best_objective_value) 
                

    def show_results(self, best_position, best_objective_value, EC, Wbar, file_pathBest, file_pathCurrent, result_directory, filename):
            import os
            import tkinter as tk
            from tkinter import filedialog
            import shutil

            self.destroy()
            root = tk.Tk()
            root.withdraw()  # Cache la fenêtre principale de tkinter
            destination_directory = filedialog.askdirectory(title="Sélectionnez le répertoire pour enregistrer les résultats")
            
            if not destination_directory:
                print('annulé')
            else:
                def create_unique_subdirectory(directory):
                    base_dir = os.path.join(directory, "resultPSO")
                    counter = 1
                    new_dir = base_dir
                    while os.path.exists(new_dir):
                        new_dir = f"{base_dir}_{counter}"
                        counter += 1
                    os.makedirs(new_dir)
                    return new_dir

                files_to_copy = [file_pathBest, file_pathCurrent, filename, self.image1, self.image]
                files_exist = any(os.path.exists(os.path.join(destination_directory, os.path.basename(file))) for file in files_to_copy)
                
                if files_exist:
                    destination_directory = create_unique_subdirectory(destination_directory)

                for file in files_to_copy:
                    shutil.copy(file, destination_directory)

            result_window = OptimisationResults.OptimisationResult(best_position, best_objective_value, EC, Wbar, self.image, result_directory)
            
            shutil.move(file_pathBest, result_directory)
            shutil.move(file_pathCurrent, result_directory)
            shutil.move(filename, result_directory)
            shutil.move(self.image1, result_directory)
            shutil.move(self.image, result_directory)      
            result_window.mainloop()

    def return_to_main_interface(self):
            from App import App
            self.destroy() 
            app = App()
            app.mainloop()
            

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

        
if __name__ == "__main__":
    app = PSO_Meta()
    app.mainloop()


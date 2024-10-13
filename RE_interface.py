import customtkinter
from tkinter import messagebox
from RE import RechercheExhaustive
import threading
import Prog_Interface
class RE(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.espaces_recherche = None 

        # configure window
        self.title("Recherche Exhaustive")
        self.geometry(f"{1100}x{600}")
        self.minsize(1100, 600)

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
        self.Metaheuristic=customtkinter.CTkLabel(self, text="La Recherche Exhaustive", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Metaheuristic.grid(row=0, column=1, padx=20, pady=15)

        # Créer le bouton "Retour" et l'ajouter à l'onglet "Résultat"      
        self.return_button = customtkinter.CTkButton(self, text="Retour", command=self.return_to_main_interface)
        self.return_button.grid(row=0, column=1, padx=20, pady=0, sticky="e")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        first_tab="Espaces de recherche"
        self.tabview.add(first_tab)
        self.tabview.tab(first_tab).grid_columnconfigure(0, weight=4)  # configure grid of individual tabs

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

        self.ExecuteSA = customtkinter.CTkButton(self.tabview.tab(first_tab), text="Executer", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           command=self.Recherche_Event)
        self.ExecuteSA.grid(row=6, column=3, padx=20, pady=(10, 10))


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
        except ValueError:
            messagebox.showerror("Erreur", "Tous les entrées doivent être numériques\n  N1, N2 et K doivent être des entiers")
            return False
        
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
        if N1_F <= N2_D:
            messagebox.showerror("Erreur", "La fin de N1 doit être supérieur au début de N2")
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
         
        # Définition des espaces de recherche pour chaque paramètre
        self.espaces_recherche = [
            (Lambda_D, Lambda_F, Lambda_P),  # Espace de recherche pour lambda: min, max, pas
            (N1_D, N1_F, N1_P),              # Espace de recherche pour N1: min, max, pas
            (N2_D, N2_F, N2_P),              # Espace de recherche pour N2: min, max, pas
            (mu1_D, mu1_F, mu1_P),           # Espace de recherche pour mu1: min, max, pas
            (mu2_D, mu2_F, mu2_P),           # Espace de recherche pour mu2: min, max, pas
            (K_D, K_F, K_P)                  # Espace de recherche pour K: min, max, pas
        ]

        return True

    def Recherche_Event(self):
        if not self.getParameters():
            return
        
        prog_window = Prog_Interface.ProgressInterface()
        threading.Thread(target=self.run_recherche, args=(prog_window,), daemon=True).start()
        prog_window.mainloop()
    
    def run_recherche(self, prog_window):
        
         # Récupération des valeurs minimales 
        Lambda_D = self.espaces_recherche[0][0]
        mu1_D = self.espaces_recherche[3][0]
        mu2_D = self.espaces_recherche[4][0]
        N1_D = self.espaces_recherche[1][0]
        N2_D = self.espaces_recherche[2][0]
        K_D = self.espaces_recherche[5][0]
        
        # Récupération des valeurs maximales 
        Lambda_F = self.espaces_recherche[0][1]
        N1_F = self.espaces_recherche[1][1]
        N2_F = self.espaces_recherche[2][1]
        mu1_F = self.espaces_recherche[3][1]
        mu2_F = self.espaces_recherche[4][1]
        K_F = self.espaces_recherche[5][1]

        # Récupération des valeurs des pas 
        Lambda_P = self.espaces_recherche[0][2]
        mu1_P = self.espaces_recherche[3][2]
        mu2_P = self.espaces_recherche[4][2]
        N1_P = self.espaces_recherche[1][2]
        N2_P = self.espaces_recherche[2][2]
        K_P = self.espaces_recherche[5][2]

        RechercheExhaustive(K_D, K_F, K_P, N1_D, N1_F, N1_P, N2_D, N2_F, N2_P, mu1_D, mu1_F, mu1_P, mu2_D, mu2_F, mu2_P, Lambda_D, Lambda_F, Lambda_P)
        # Once complete, destroy the progress window and show results
        prog_window.after(0, prog_window.destroy)
        prog_window.after(0, lambda: self.show_results())
    
    def show_results(self):
        import Inter_RE_Result
        # Create and display the results window
        result_window = Inter_RE_Result.RE_Result()
        #print("show result")
        result_window.mainloop()
        
    def return_to_main_interface(self):
            from App import App
            self.destroy()  # Détruire la fenêtre des résultats
            app = App()
            app.mainloop()
        
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

        
if __name__ == "__main__":
    app = RE()
    app.mainloop()
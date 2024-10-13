from tkinter import messagebox
import customtkinter
import numpy as np
import threading
import Prog_Interface
from RE_interface import RE
from SA_interface import SA_Meta
from TS_interface import TS_Meta
from PSO_interface import PSO_Meta


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.K = None
        self.N1 = None
        self.N2 = None
        self.mu1 = None
        self.mu2 = None
        self.Lambda = None
        self.para = None

        # configure window
        self.title("L'optimisation dans les RCSF ")
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

        

        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        first_tab="Two threshreshods vacation policy"
        second_tab="Optimisation"
        self.tabview.add(first_tab)
        self.tabview.add(second_tab)
        self.tabview.tab(first_tab).grid_columnconfigure(0, weight=4)  # configure grid of individual tabs
        self.tabview.tab(second_tab).grid_columnconfigure(0, weight=4)

        #First Tab_________________________________________________________________________________________________________________________
    
        
        
        self.lambda_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner le taux d'arrivé Lambda :",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.lambda_label.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="e")
        self.lambda_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="Lambda")
        self.lambda_values.grid(row=1, column=1, padx=20, pady=(20, 10), sticky="e")


        self.N2_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner le seuil de l'état semi-occupé N2 :" ,font=customtkinter.CTkFont(size=15, weight="bold"))
        self.N2_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="e")
        self.N2_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="N2")                                      
        self.N2_values.grid(row=2, column=1, padx=20, pady=(20, 10), sticky="e")

        self.N1_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner le seuil de l'état occupé N1 :" ,font=customtkinter.CTkFont(size=15, weight="bold"))
        self.N1_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="e")
        self.N1_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="N1")
        self.N1_values.grid(row=3, column=1, padx=20, pady=(20, 10), sticky="e")

        self.K_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner la taille du buffer K :",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.K_label.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="e")
        self.K_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="K")
        self.K_values.grid(row=4, column=1, padx=20, pady=(20, 10), sticky="e")

        self.mu2_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner le taux de service de l'état semi-occupé Mu2 :",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.mu2_label.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="e")
        self.mu2_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="mu2")
        self.mu2_values.grid(row=5, column=1, padx=20, pady=(20, 10), sticky="e")

        self.mu1_label = customtkinter.CTkLabel(self.tabview.tab(first_tab), text="Sélectionner le taux de service de l'état occupé Mu1 :",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.mu1_label.grid(row=6, column=0, padx=20, pady=(20, 10), sticky="e")
        self.mu1_values = customtkinter.CTkEntry(self.tabview.tab(first_tab),placeholder_text="mu1")
        self.mu1_values.grid(row=6, column=1, padx=20, pady=(20, 10), sticky="e")


        self.string_input_button = customtkinter.CTkButton(self.tabview.tab(first_tab), text="Exécuter", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           command=self.twothreshodspolicyEvent)
        self.string_input_button.grid(row=8, column=2, padx=20, pady=(10, 10))

        # Second Tab_________________________________________________________________________________________________________________________

        # Méthode Exacte Section
        self.exact_method_frame = customtkinter.CTkFrame(self.tabview.tab(second_tab))
        self.exact_method_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.exact_method_frame.grid_columnconfigure(0, weight=1)  # Make column 0 expand to take extra space

        self.exact_method_label = customtkinter.CTkLabel(self.exact_method_frame, text="Méthode Exacte :", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.exact_method_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Section interne pour Recherche Exhaustive 
        self.RE_frame = customtkinter.CTkFrame(self.exact_method_frame)
        self.RE_frame.grid(row=1, column=0, padx=(60, 20), pady=10, sticky="nsew")
        self.RE_frame.grid_columnconfigure(1, weight=1)  # Allow the second column to expand

        self.RE_label = customtkinter.CTkLabel(self.RE_frame, text="Recherche Exhaustive", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.RE_label.grid(row=0, column=0, padx=60, pady=10, sticky="w")

        self.RE_colon = customtkinter.CTkLabel(self.RE_frame, text=" ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.RE_colon.grid(row=0, column=1, sticky="w", pady=5)

        self.RE_Button = customtkinter.CTkButton(self.RE_frame, text="Suivant", font=customtkinter.CTkFont(size=13, weight="bold"), command=self.goToRE_Event)
        self.RE_Button.grid(row=0, column=2, padx=20, pady=10, sticky="e")  # Place button in column 3

        # Méthode Approchée Section
        self.approx_method_frame = customtkinter.CTkFrame(self.tabview.tab(second_tab))
        self.approx_method_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.approx_method_frame.grid_columnconfigure(0, weight=1)  # Make column 0 expand to take extra space

        self.approx_method_label = customtkinter.CTkLabel(self.approx_method_frame, text="Méthodes Approchées :", font=customtkinter.CTkFont(size=18, weight="bold"))
        self.approx_method_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Solution Unique Section
        self.sol_unique_frame = customtkinter.CTkFrame(self.approx_method_frame)
        self.sol_unique_frame.grid(row=1, column=0, padx=(60, 20), pady=10, sticky="nsew")
        self.sol_unique_frame.grid_columnconfigure(1, weight=1)  # Allow the second column to expand

        self.SolUnique_label = customtkinter.CTkLabel(self.sol_unique_frame, text="Métaheuristiques à solution unique :", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.SolUnique_label.grid(row=0, column=0, padx=60, pady=10, sticky="w")

        # Recuit Simulé Section
        self.SA_label = customtkinter.CTkLabel(self.sol_unique_frame, text="Optimisation par Recuit Simulé", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.SA_label.grid(row=1, column=0, padx=60, pady=10, sticky="w")

        self.SA_colon = customtkinter.CTkLabel(self.sol_unique_frame, text=" ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.SA_colon.grid(row=1, column=1, sticky="w", pady=5)

        self.SA_Button = customtkinter.CTkButton(self.sol_unique_frame, text="Suivant", font=customtkinter.CTkFont(size=13, weight="bold"), command=self.goToSa_Event)
        self.SA_Button.grid(row=1, column=2, padx=20, pady=10, sticky="e")

        # Recherche Tabou Section
        self.TS_label = customtkinter.CTkLabel(self.sol_unique_frame, text="Optimisation par Recherche Tabou", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.TS_label.grid(row=2, column=0, padx=60, pady=10, sticky="w")

        self.TS_colon = customtkinter.CTkLabel(self.sol_unique_frame, text=" ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.TS_colon.grid(row=2, column=1, sticky="w", pady=5)

        self.TS_Button = customtkinter.CTkButton(self.sol_unique_frame, text="Suivant", font=customtkinter.CTkFont(size=13, weight="bold"), command=self.goToTS_Event)
        self.TS_Button.grid(row=2, column=2, padx=20, pady=10, sticky="e")

        # Population de Solution Section
        self.pop_sol_frame = customtkinter.CTkFrame(self.approx_method_frame)
        self.pop_sol_frame.grid(row=2, column=0, padx=(60, 20), pady=10, sticky="nsew")
        self.pop_sol_frame.grid_columnconfigure(1, weight=1)  # Allow the second column to expand

        self.PopSol_label = customtkinter.CTkLabel(self.pop_sol_frame, text="Métaheuristiques à population de solutions :", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.PopSol_label.grid(row=0, column=0, padx=60, pady=10, sticky="w")

        # Essaim de Particules Section
        self.PSO_label = customtkinter.CTkLabel(self.pop_sol_frame, text="Optimisation par Essaim de Particules", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.PSO_label.grid(row=1, column=0, padx=60, pady=10, sticky="w")

        self.PSO_colon = customtkinter.CTkLabel(self.pop_sol_frame, text=" ", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.PSO_colon.grid(row=1, column=1, sticky="w", pady=5)

        self.PSO_Button = customtkinter.CTkButton(self.pop_sol_frame, text="Suivant", font=customtkinter.CTkFont(size=13, weight="bold"), command=self.goToPSO_Event)
        self.PSO_Button.grid(row=1, column=2, padx=20, pady=10, sticky="e")

        # Configurer les lignes pour qu'elles s'étendent uniformément
        self.tabview.tab(second_tab).grid_rowconfigure(0, weight=1)
        self.tabview.tab(second_tab).grid_rowconfigure(1, weight=1)
     
        
        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        
    def getParameters(self):
        try:
            self.K = int(self.K_values.get())
            self.N1 = int(self.N1_values.get())
            self.N2 = int(self.N2_values.get())
            self.mu1 = float(self.mu1_values.get())
            self.mu2 = float(self.mu2_values.get())
            self.Lambda = float(self.lambda_values.get())
        except ValueError:
            messagebox.showerror("Erreur", "Tous les entrées doivent être numériques")
            return False

        if self.Lambda <= 0:
            messagebox.showerror("Erreur", "Lambda doit être positif")
            return False
        if self.N2 <= 0:
            messagebox.showerror("Erreur", "N2 doit être positif")
            return False        
        if self.N1 <= self.N2:
            messagebox.showerror("Erreur", "N1 doit être supérieur à N2")
            return False  
        if self.K <= self.N1:
            messagebox.showerror("Erreur", "K doit être supérieur à N1")
            return False
        if self.mu2 <= 0:
            messagebox.showerror("Erreur", "mu2 doit être positif")
            return False
        if self.mu1 <= self.mu2:
            messagebox.showerror("Erreur", "mu1 doit être supérieur à mu2")
            return False
        
        self.para=[self.K, self.N1, self.N2, self.mu1, self.mu2, self.Lambda]
        return True

    def twothreshodspolicyEvent(self):
        if not self.getParameters():
            return
        # Setup and display the progress window
        prog_window = Prog_Interface.ProgressInterface()
        threading.Thread(target=self.run_policy, args=(prog_window,), daemon=True).start()
        prog_window.mainloop()
        

    def run_policy(self, prog_window):
        
        # Execute the long-running task
        from TwoThreshodscode import twoThreshodsPolicy
        EC, Delay = twoThreshodsPolicy(self.K, self.N1, self.N2, self.mu1, self.mu2, self.Lambda)

        # Once complete, destroy the progress window and show results
        prog_window.after(0, prog_window.destroy)
        prog_window.after(0, lambda: self.show_results(self.para, EC, Delay))

    def show_results(self, para,EC, Delay):
        from Inter_twothreshod_Result import TT_Result
        # Format solution_valeur as a string
        param_labels = ["K", "N1", "N2", "mu1", "mu2", "λ"]  # Adjust labels according to your parameters
        solution_str = ', '.join(f"{label}={value}" for label, value in zip(param_labels, para))

        # Adding units to EC and Delay
        EC_str = f"{EC} joules"
        Delay_str = f"{Delay} secondes"

        # Create and display the results window
        result_window = TT_Result(solution_str, EC_str, Delay_str)
        #result_window = Inter_TwoThreshodsPolicyResult.TwothreshodsResult(self.para,EC, Delay)
        result_window.mainloop()

    
    def goToRE_Event(self):
        # Fermez la fenêtre de l'interface principale
        self.destroy()
        RE_window = RE()
        RE_window.mainloop()
        
    def goToSa_Event(self):
        # Fermez la fenêtre de l'interface principale
        self.destroy()
        SA_window = SA_Meta()
        SA_window.mainloop()
    
    def goToTS_Event(self):
        # Fermez la fenêtre de l'interface principale
        self.destroy()
        TS_window = TS_Meta()
        TS_window.mainloop()
    
    def goToPSO_Event(self):
        # Fermez la fenêtre de l'interface principale
        self.destroy()
        PSO_window = PSO_Meta()
        PSO_window.mainloop()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    
if __name__ == "__main__":
    app = App()
    app.mainloop()



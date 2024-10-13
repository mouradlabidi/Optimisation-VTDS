import customtkinter
from tkinter import *
#import numpy as np
from customtkinter import CTkLabel, CTkImage
from PIL import Image
#from SA_interface import SA_Meta

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class OptimisationResult(customtkinter.CTk):
        def __init__(self, best_solution, best_objective_value,EC,Wbar,image_path, result_directory):
            super().__init__()
            self.result_directory = result_directory
            
            # configure window
            self.title("Résultat")
            
            ###############################################
            # Récupérer la taille de l'écran
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            # Calculer la taille maximale pour la fenêtre tout en laissant un petit espace
            max_width = int(screen_width * 0.91)
            max_height = int(screen_height * 0.90)

            # Définir la géométrie de la fenêtre
            self.geometry(f"{max_width}x{max_height}")
            self.minsize(max_width, max_height)

            # Empêcher la fenêtre de se redimensionner
            #self.wm_resizable(False, False)
            ################################################
            #self.geometry(f"{1100}x{580}")

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
            second_tab="Résultat de la méta-heuristique"
            self.tabview.add(second_tab)  # configure grid of individual tabs
            
            
            #Second Tab_________________________________________________________________________________________________________________________
            
            # Créer le bouton "Retour" et l'ajouter à l'onglet "Résultat"
            
            self.return_button = customtkinter.CTkButton(self.tabview.tab(second_tab), text="Retour", command=self.return_to_main_interface)
            self.return_button.grid(row=0, column=8, padx=(0, 10), pady=0, sticky="e", ipadx=1, ipady=3)
            
            
            
            # Créer une étiquette pour afficher le titre de la solution
            solution_text = "Meilleure solution obtenue: "
            solution_label_title = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=solution_text, font=customtkinter.CTkFont(size=15, weight="bold"))
            solution_label_title.grid(row=1, column=1, padx=20, pady=(10, 5), sticky="w")  # Modifiez pady ici

            # Créer une étiquette pour afficher les détails de la solution
            solution_value_text = f"[K={int(best_solution[5])}, N2={int(best_solution[2])}, N1={int(best_solution[1])}, Lambda={best_solution[0]}, mu2={best_solution[4]}, mu1={best_solution[3]}]"
            self.solution_label_details = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=solution_value_text, font=customtkinter.CTkFont(size=15))
            self.solution_label_details.grid(row=1, column=2, columnspan=8, padx=20, pady=(10, 5), sticky="w")  # Modifiez pady ici

            objective_value_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Fonction Objective:", font=customtkinter.CTkFont(size=15, weight="bold"))
            objective_value_label.grid(row=2, column=1, padx=20, pady=(2, 2), sticky="w")  # Modifiez pady ici

            self.objective_value_input_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=best_objective_value, font=customtkinter.CTkFont(size=15))
            self.objective_value_input_label.grid(row=2, column=2, padx=20, pady=(2, 2), sticky="w")  # Modifiez pady ici

            # Créer une étiquette pour afficher l'énergie consommée
            energy_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Energie Consommée:", font=customtkinter.CTkFont(size=15, weight="bold"))
            energy_label.grid(row=3, column=1, padx=20, pady=(2, 2), sticky="w")  # Modifiez pady ici

            self.energy_input_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=EC, font=customtkinter.CTkFont(size=15))
            self.energy_input_label.grid(row=3, column=2, padx=20, pady=(2, 2), sticky="w")  # Modifiez pady ici

            # Créer une étiquette pour afficher le délai d'attente
            wait_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text="Délai d'Attente:", font=customtkinter.CTkFont(size=15, weight="bold"))
            wait_label.grid(row=4, column=1, padx=20, pady=(4, 2), sticky="w")  # Modifiez pady ici

            self.wait_input_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=Wbar, font=customtkinter.CTkFont(size=15))
            self.wait_input_label.grid(row=4, column=2, padx=20, pady=(4, 2), sticky="w")  # Modifiez pady ici

            self.empty_label = customtkinter.CTkLabel(self.tabview.tab(second_tab), text=' ')
            self.empty_label.grid(row=5, column=2, padx=2, pady=1, sticky="w")

            #image contenant les graphes
            self.image = None
            if image_path:
                # Inside your try block for loading the image
                try:
                    pil_image = Image.open(image_path)
                    fig = Figure(figsize=(8.5, 4))  # Taille initiale de la figure
                    ax = fig.add_subplot(111)
                    ax.imshow(pil_image)
                    ax.axis('off')
                    fig.tight_layout()  # Ajuster automatiquement les paramètres de la figure
                    canvas = FigureCanvasTkAgg(fig, master=self.tabview.tab(second_tab))
                    canvas.draw()
                    canvas.get_tk_widget().config(borderwidth=0, highlightthickness=0)
                    
                    # Placer le canevas dans la grille avec la nouvelle configuration
                    self.tabview.tab(second_tab).grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)  # Ajuster les colonnes pour qu'elles prennent la largeur
                    canvas.get_tk_widget().grid(row=6, column=1, padx=20, columnspan=8, sticky="nsew")  # Fusionner 4 colonnes
                
                except FileNotFoundError:
                    print(f"Error: Image file not found: {image_path}")
                except Exception as e:
                    print(f"Error loading image: {e}")
            
            # set default values
            self.appearance_mode_optionemenu.set("Dark")
            self.scaling_optionemenu.set("100%")

        
        def return_to_main_interface(self):
            from SA_interface import SA_Meta
            from TS_interface import TS_Meta
            from PSO_interface import PSO_Meta
            self.destroy()  # Détruire la fenêtre des résultats
            if(self.result_directory == "resultSA"):
                app = SA_Meta()  # Recréer l'interface principale
            elif(self.result_directory == "resultTS"):
                app = TS_Meta()
            elif(self.result_directory == "resultPSO"):
                app = PSO_Meta()
            app.mainloop()
        
        
        def change_appearance_mode_event(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)
        
        def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)

'''
if __name__ == "__main__":
    best_solution = [13, 12, 2, 7.5, 4.75, 0.25]
    best_objective_value = 0.029834904
    EC = 50.98663107
    Wbar = 2.222222222
    image = 'energy_delay.png'
    app = OptimisationResult(best_solution, best_objective_value, EC, Wbar, image, "resultSA")
    app.mainloop()
'''
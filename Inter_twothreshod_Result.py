import customtkinter
import os

class TT_Result(customtkinter.CTk):
    def __init__(self, solution_valeur, energie_valeur, delai_valeur):
        super().__init__()

        # Configure window
        self.title("Résultats de la Politique à Deux Seuils")
        self.geometry("450x200")  # Adjusted size for better layout
        self.resizable(False, False)  # Make window non-resizable

        # Calculate position to center the window
        screen_width = self.winfo_screenwidth()  # Get screen width
        screen_height = self.winfo_screenheight()  # Get screen height
        x = (screen_width - 450) // 2  # Calculate x position
        y = (screen_height - 200) // 2  # Calculate y position
        self.geometry(f"+{x}+{y}")  # Set the position of the window

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # New column for the colons
        self.grid_columnconfigure(2, weight=2)  # Make the third column wider
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Create and grid labels for the results
        self.solution_label = customtkinter.CTkLabel(self, text="Solution", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.solution_label.grid(row=0, column=0, sticky="w", padx=(60, 20), pady=5)
        self.solution_colon = customtkinter.CTkLabel(self, text=":", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.solution_colon.grid(row=0, column=1, sticky="w", pady=5)
        self.solution_value = customtkinter.CTkLabel(self, text=f"[{solution_valeur}]", font=customtkinter.CTkFont(size=12))
        self.solution_value.grid(row=0, column=2, sticky="w", padx=20, pady=5)

        self.energie_label = customtkinter.CTkLabel(self, text="Energie", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.energie_label.grid(row=1, column=0, sticky="w", padx=(60, 20), pady=5)
        self.energie_colon = customtkinter.CTkLabel(self, text=":", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.energie_colon.grid(row=1, column=1, sticky="w", pady=5)
        self.energie_value = customtkinter.CTkLabel(self, text=energie_valeur, font=customtkinter.CTkFont(size=12))
        self.energie_value.grid(row=1, column=2, sticky="w", padx=20, pady=5)

        self.delai_label = customtkinter.CTkLabel(self, text="Délai", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.delai_label.grid(row=2, column=0, sticky="w", padx=(60, 20), pady=5)
        self.delai_colon = customtkinter.CTkLabel(self, text=":", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.delai_colon.grid(row=2, column=1, sticky="w", pady=5)
        self.delai_value = customtkinter.CTkLabel(self, text=delai_valeur, font=customtkinter.CTkFont(size=12))
        self.delai_value.grid(row=2, column=2, sticky="w", padx=20, pady=5)

if __name__ == "__main__":
    solution_valeur = "10, 20, 16, 3, 4, 2.5" # Remplacez par la valeur réelle de la solution
    energie_valeur = "energie_valeur"      # Remplacez par la valeur réelle de l'énergie
    delai_valeur = "delai_valeur"          # Remplacez par la valeur réelle du délai
    
    app = TT_Result(solution_valeur, energie_valeur, delai_valeur)
    app.mainloop()
